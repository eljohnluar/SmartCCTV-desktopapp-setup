"""
OBS Virtual Camera -> SmartCCTV backend WebRTC bridge (Option 1).

Runs on the same computer as OBS Studio. It grabs the OBS Virtual Camera with
OpenCV, encodes it as VP8, and pushes it to the SmartCCTV backend (e.g. on
Railway) over a WebRTC peer connection.

Requirements (install once):
    pip install aiortc websockets opencv-python numpy

Usage:
    python obs_webrtc_bridge.py --backend wss://your-backend.up.railway.app --token YOUR_JWT

    In OBS Studio: Tools -> Start Virtual Camera, then run this script.

Signaling protocol (backend must implement a WebSocket endpoint at /ws/bridge):
    Client -> Server:
        {"type": "hello", "source": "obs", "token": "<JWT>"}
        {"type": "offer", "sdp": "<session description>"}
        {"type": "ice", "candidate": "<candidate line>", "sdp_mid": "...", "sdp_mline_index": 0}
    Server -> Client:
        {"type": "ready"}
        {"type": "answer", "sdp": "<session description>"}
        {"type": "ice", "candidate": "...", "sdp_mid": "...", "sdp_mline_index": 0}

The backend receives the media track and feeds it into the normal camera
pipeline (face recognition, MJPEG delivery, attendance marking).
"""

import argparse
import asyncio
import json
import logging
import sys
import time

import cv2
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("obs-bridge")

try:
    import websockets
except ImportError:
    log.error("Missing dependency 'websockets'. Install with: pip install websockets aiortc opencv-python numpy")
    sys.exit(1)

try:
    from aiortc import (
        RTCPeerConnection,
        RTCSessionDescription,
        VideoStreamTrack,
    )
    from aiortc.sdp import candidate_from_sdp
    from aiortc.contrib.media import MediaRelay
    import av
except ImportError:
    log.error("Missing dependency 'aiortc'. Install with: pip install aiortc websockets opencv-python numpy")
    sys.exit(1)


class OpenCVCaptureTrack(VideoStreamTrack):
    """VideoStreamTrack fed by OpenCV frames from the OBS Virtual Camera."""

    kind = "video"

    def __init__(self, capture, fps: int = 20):
        super().__init__()
        self.capture = capture
        self._timestamp = 0
        self._fps = fps
        self._interval = 1.0 / fps
        self._next_frame_time = time.monotonic()

    async def recv(self):
        # Pace frames so encoding does not outrun the camera
        now = time.monotonic()
        if now < self._next_frame_time:
            await asyncio.sleep(self._next_frame_time - now)
        self._next_frame_time += self._interval

        pts = self._timestamp
        self._timestamp += self._interval

        ok, frame = self.capture.read()
        if not ok or frame is None:
            # Camera not ready yet: send a black frame so the track stays alive
            frame = np.zeros((720, 1280, 3), dtype=np.uint8)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
        video_frame.pts = round(pts * 90000)
        video_frame.time_base = "1/90000"
        return video_frame


async def run(backend_url: str, token: str, camera_index: int, fps: int) -> None:
    while True:
        capture = None
        try:
            log.info("Opening camera index %d (OBS Virtual Camera)...", camera_index)
            capture = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            if not capture.isOpened():
                # Some Windows setups need CAP_MSMF instead of DSHOW
                capture.release()
                capture = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)
            if not capture.isOpened():
                log.error(
                    "Could not open camera index %d. Make sure OBS is running and "
                    "'Start Virtual Camera' is enabled.",
                    camera_index,
                )
                await asyncio.sleep(5)
                continue

            ws_url = backend_url.replace("http", "ws", 1).rstrip("/") + "/ws/bridge"
            log.info("Connecting to signaling server %s", ws_url)
            async with websockets.connect(
                ws_url,
                max_size=2 ** 24,
                open_timeout=20,
                ping_interval=20,
            ) as websocket:
                await websocket.send(json.dumps({
                    "type": "hello",
                    "source": "obs",
                    "token": token,
                }))

                pc = RTCPeerConnection()
                relay = MediaRelay()
                track = OpenCVCaptureTrack(capture, fps=fps)
                pc.addTrack(relay.subscribe(track))

                @pc.on("icecandidate")
                async def on_ice_candidate(candidate):
                    if candidate is None:
                        return
                    await websocket.send(json.dumps({
                        "type": "ice",
                        "candidate": candidate.candidate,
                        "sdp_mid": candidate.sdpMid,
                        "sdp_mline_index": candidate.sdpMLineIndex,
                    }))

                @pc.on("connectionstatechange")
                async def on_conn_state():
                    log.info("Peer connection state: %s", pc.connectionState)

                sent_offer = False
                width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
                height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
                log.info("Streaming %dx%d @ %d fps from camera index %d", width, height, fps, camera_index)

                # Single consumer loop for all signaling messages
                async for raw in websocket:
                    try:
                        message = json.loads(raw)
                    except json.JSONDecodeError:
                        continue

                    msg_type = message.get("type")

                    if msg_type == "ready" and not sent_offer:
                        offer = await pc.createOffer()
                        await pc.setLocalDescription(offer)
                        await websocket.send(json.dumps({
                            "type": "offer",
                            "sdp": pc.localDescription.sdp,
                        }))
                        sent_offer = True
                        log.info("Sent WebRTC offer")

                    elif msg_type == "answer":
                        await pc.setRemoteDescription(
                            RTCSessionDescription(sdp=message["sdp"], type="answer")
                        )
                        log.info("Received answer; WebRTC session established")

                    elif msg_type == "ice" and message.get("candidate"):
                        candidate = candidate_from_sdp(message["candidate"])
                        candidate.sdpMid = message.get("sdp_mid")
                        candidate.sdpMLineIndex = message.get("sdp_mline_index", 0)
                        await pc.addIceCandidate(candidate)

                    if pc.connectionState in ("failed", "closed"):
                        break

                await pc.close()
                log.warning("Connection ended; reconnecting in 3 seconds...")
        except asyncio.CancelledError:
            raise
        except Exception as error:
            log.error("Bridge error: %s", error)
            log.info("Retrying in 3 seconds...")
        finally:
            if capture is not None:
                capture.release()

        await asyncio.sleep(3)


def main() -> None:
    parser = argparse.ArgumentParser(description="OBS Virtual Camera WebRTC bridge for SmartCCTV")
    parser.add_argument("--backend", default="https://smartcctv-backend-production.up.railway.app",
                        help="Backend base URL, e.g. https://smartcctv-backend-production.up.railway.app")
    parser.add_argument("--token", default="",
                        help="JWT from the SmartCCTV app (localStorage 'access_token')")
    parser.add_argument("--camera-index", type=int, default=1,
                        help="OpenCV device index for the OBS Virtual Camera (default 1)")
    parser.add_argument("--fps", type=int, default=20,
                        help="Frames per second to send (default 20)")
    args = parser.parse_args()

    try:
        asyncio.run(run(args.backend, args.token, args.camera_index, args.fps))
    except KeyboardInterrupt:
        log.info("Stopped by user")


if __name__ == "__main__":
    main()
