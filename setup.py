from cx_Freeze import setup, Executable
import os
import sys

# Application information
APP_NAME = "NeuraAI"
VERSION = "1.0"
DESCRIPTION = "Neura AI Personal Assistant"
AUTHOR = "Tanishq"

# Get absolute paths
base_dir = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(base_dir, 'assets')
www_path = os.path.join(base_dir, 'www')

# Include files
include_files = [
    (www_path, 'www'),
    (assets_path, 'assets')
]

# Dependencies
build_exe_options = {
    "packages": [
        "os", "sys", "eel", "speech_recognition", "pyttsx3",
        "google.generativeai", "datetime", "webbrowser",
        "googleapiclient", "re", "selenium", "time", "json"
    ],
    "include_files": include_files,
    "excludes": ["tkinter"],
    "optimize": 2,
    "include_msvcr": True
}

# Executable configuration
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "backend.py",
        base=base,
        target_name=APP_NAME,
        icon=os.path.join(assets_path, 'icon.ico'),
        shortcut_name="Neura AI",
        shortcut_dir="DesktopFolder"
    )
]

setup(
    name=APP_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": {
            "upgrade_code": "{E5B8D92C-5A5F-4F19-9B22-5D5F1F57D3A7}",
            "add_to_path": False,
            "initial_target_dir": r"[ProgramFilesFolder]\%s" % APP_NAME
        }
    },
    executables=executables
)