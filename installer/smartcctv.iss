; SmartCCTV desktop installer (Inno Setup 6.3+)
;
; Expected layout relative to this script (the installer\ folder):
;   runtime\          bundled embedded Python - built by tools\build_runtime.bat
;   env\.env          OPTIONAL per-deploy config, installed to %ProgramData%\SmartCCTV\.env
;                     (skip this file and create the .env manually after install if you
;                      don't want secrets baked into the installer)
;   output\           where the finished Setup .exe lands
;
; Bump MyAppVersion for each release. Keep the AppId unchanged so upgrades
; install over the old version and preserve the existing ProgramData .env.

#define MyAppName "SmartCCTV"
#define MyAppVersion "2.6"
#define MyAppPublisher "SmartCCTV"

[Setup]
AppId={{9A3F5D7B-2C4E-4A8D-B1F6-7E8C3D5A9B2C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=SmartCCTV-Setup-{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
WizardStyle=modern
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Dirs]
Name: "{commonappdata}\{#MyAppName}"; Permissions: users-readexec

[Files]
; Bundled Python runtime (build first with tools\build_runtime.bat)
Source: "runtime\*"; DestDir: "{app}\runtime"; Flags: recursesubdirs createallsubdirs ignoreversion
; Backend (skip dev-only files; .env comes from ProgramData at runtime)
Source: "..\backend\*"; DestDir: "{app}\backend"; Flags: recursesubdirs createallsubdirs ignoreversion; Excludes: ".venv\*,__pycache__\*,*.pyc,.env"
; Built frontend
Source: "..\frontend\dist\*"; DestDir: "{app}\frontend\dist"; Flags: recursesubdirs createallsubdirs ignoreversion
; Desktop launcher
Source: "..\launcher.py"; DestDir: "{app}"; Flags: ignoreversion
; Optional per-deploy .env -> C:\ProgramData\SmartCCTV\.env
; Never overwritten on upgrade, never removed on uninstall.
Source: "env\.env"; DestDir: "{commonappdata}\{#MyAppName}"; Flags: onlyifdoesntexist uninsneveruninstall skipifsourcedoesntexist; Permissions: users-readexec

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\launcher.py"""; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\launcher.py"""; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\runtime\pythonw.exe"; Parameters: """{app}\launcher.py"""; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
