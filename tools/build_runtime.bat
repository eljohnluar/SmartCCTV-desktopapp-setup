@echo off
setlocal
title SmartCCTV runtime builder
rem Builds the bundled Python runtime for the SmartCCTV installer into installer\runtime.
rem Needs internet; downloads ~600 MB of packages. Run once (or after each backend dependency change).

set "PYVER=3.14.3"
set "ROOT=%~dp0.."
set "RUNTIME=%ROOT%\installer\runtime"

if exist "%RUNTIME%\python.exe" (
  echo Runtime already exists at %RUNTIME% - delete the folder to rebuild it.
  pause
  exit /b 1
)

set "ZIP=%TEMP%\python-embed-%PYVER%-amd64.zip"
echo [1/4] Downloading Python %PYVER% embeddable distribution...
curl.exe -L -o "%ZIP%" "https://www.python.org/ftp/python/%PYVER%/python-%PYVER%-embed-amd64.zip"
if errorlevel 1 goto :fail

echo [2/4] Extracting to %RUNTIME%...
if not exist "%RUNTIME%" mkdir "%RUNTIME%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Path '%ZIP%' -DestinationPath '%RUNTIME%' -Force"
if errorlevel 1 goto :fail

rem Enable site-packages + pip in the embeddable distribution.
>"%RUNTIME%\python314._pth" (
  echo python314.zip
  echo Lib\site-packages
  echo .
  echo import site
)

echo [3/4] Installing pip...
curl.exe -L -o "%TEMP%\get-pip.py" "https://bootstrap.pypa.io/get-pip.py"
if errorlevel 1 goto :fail
"%RUNTIME%\python.exe" "%TEMP%\get-pip.py" --no-warn-script-location
if errorlevel 1 goto :fail

echo [4/4] Installing SmartCCTV dependencies - this takes a while...
rem Skipped packages:
rem  - opencv-python-headless pin targets Railway's Linux image; unpinned wheels are correct on Windows.
rem  - pygame has no Python 3.14 wheels and is only the non-Windows audio fallback
rem    (Windows announcements use built-in SAPI), so it is not needed in the desktop runtime.
type "%ROOT%\backend\requirements.txt" | findstr /v /c:"opencv-python-headless==" /c:"pygame>=" > "%TEMP%\smartcctv-reqs.txt"
"%RUNTIME%\python.exe" -m pip install -r "%TEMP%\smartcctv-reqs.txt" --no-warn-script-location
if errorlevel 1 goto :fail
"%RUNTIME%\python.exe" -m pip install opencv-python-headless --no-warn-script-location
if errorlevel 1 goto :fail

echo.
echo Runtime ready: %RUNTIME%
echo You can now compile installer\smartcctv.iss in Inno Setup.
pause
exit /b 0

:fail
echo.
echo BUILD FAILED - see the error above.
pause
exit /b 1
