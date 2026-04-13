# -*- coding: utf-8 -*-
"""
Atlas Matrix Installer
Compatible with Maya 2020+ (PySide2 and PySide6)

Author: Clement Daures
Website: clementdaures.com
Created: 2025

# ---------- LICENSE ----------

Copyright 2025 Clement Daures

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# ---------- IMPORT ----------

import os
import sys
import shutil
import platform
import traceback
from typing import Optional

import maya.cmds as cmds
import maya.mel as mel

# ---------- CONSTANTS ----------

MEL_COMMENT = "// "
PY_COMMENT = "# "
SCRIPT_MARKER = "ATLAS_MATRIX_SCRIPT_PATH"
ICON_MARKER = "ATLAS_MATRIX_ICON_PATH"
END_MARKER = "END_ATLAS_MATRIX"


# ---------- FUNCTIONS ----------


def _norm(p: str) -> str:
    """
    Normalize a file path to use forward slashes and absolute form.

    Args:
        p (str): The path to normalize.

    Returns:
        str: Normalized absolute path with forward slashes.
    """
    return os.path.abspath(p).replace("\\", "/")


def get_os() -> str:
    """
    Get the current operating system name.

    Returns:
        str: 'Windows', 'Darwin' (macOS), or 'Linux'.
    """
    return platform.system()


def get_maya_version() -> str:
    """
    Get the current Maya version.

    Returns:
        str: Maya version string (e.g., '2024', '2025').
    """
    return cmds.about(version=True)


def get_maya_prefs_dir(maya_version: str, user_platform: str) -> str:
    """
    Get Maya preferences directory based on platform and version.

    Args:
        maya_version (str): Maya version string (e.g., '2024').
        user_platform (str): Operating system name ('Windows', 'Darwin', 'Linux').

    Returns:
        str: Path to Maya preferences directory.
    """
    if user_platform == "Windows":
        user_profile = os.environ.get("USERPROFILE", "")

        onedrive_path = os.path.join(user_profile, "OneDrive", "Documents", "maya", maya_version)
        local_path = os.path.join(user_profile, "Documents", "maya", maya_version)

        if os.path.exists(onedrive_path):
            return onedrive_path
        else:
            return local_path
    elif user_platform == "Darwin":  # Mac
        return os.path.expanduser(f"~/Library/Preferences/Autodesk/maya/{maya_version}")
    else:  # Linux
        return os.path.expanduser(f"~/maya/{maya_version}")


def _remove_existing_block(filepath: str, start_marker: str, end_marker: str) -> str:
    """
    Remove existing marked block from a file and return cleaned content.

    Args:
        filepath (str): Path to the file to clean.
        start_marker (str): Starting marker line to identify block.
        end_marker (str): Ending marker line to identify block.

    Returns:
        str: File content with marked block removed, or empty string if file doesn't exist.
    """
    if not os.path.exists(filepath):
        return ""

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    skip_mode = False

    for line in lines:
        if start_marker in line:
            skip_mode = True
            continue
        if skip_mode and end_marker in line:
            skip_mode = False
            continue
        if not skip_mode:
            new_lines.append(line)

    return "".join(new_lines)


def _append_block(filepath: str, start_marker: str, end_marker: str, content: str) -> None:
    """
    Remove any existing marked block, then append new block to file.

    Args:
        filepath (str): Path to the file to modify.
        start_marker (str): Starting marker for the block.
        end_marker (str): Ending marker for the block.
        content (str): Content to append (should include markers).
    """
    # Remove existing block first
    existing = _remove_existing_block(filepath, start_marker, end_marker)

    # Write cleaned content plus new block
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(existing)
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write("\n" + content)

    print(f"Updated {os.path.basename(filepath)} with new block")


def write_usersetup_blocks(tools_dir: str, maya_scripts_dir: str) -> None:
    """
    Write userSetup blocks for script and icon paths.

    Removes any existing Atlas Matrix blocks first to prevent duplicates,
    then appends fresh configuration.

    Args:
        tools_dir (str): Path to the atlas_matrix directory.
        maya_scripts_dir (str): Path to Maya's scripts directory.
    """
    atlas_dir = _norm(tools_dir)
    parent_dir = _norm(os.path.dirname(atlas_dir))
    icon_dir = _norm(os.path.join(atlas_dir, "setup", "icons"))

    user_py = os.path.join(maya_scripts_dir, "userSetup.py")
    user_mel = os.path.join(maya_scripts_dir, "userSetup.mel")

    # Python blocks
    py_block = (
        f"{PY_COMMENT}{SCRIPT_MARKER}\n"
        f"import sys\n"
        f"atlas_parent = r\"{parent_dir}\"\n"
        f"if atlas_parent not in sys.path:\n"
        f"    sys.path.append(atlas_parent)\n"
        f"{PY_COMMENT}{END_MARKER}\n"
    )

    icon_py_block = (
        f"{PY_COMMENT}{ICON_MARKER}\n"
        f"import maya.mel as mel\n"
        f"icon_path = r\"{icon_dir}\"\n"
        f"current_xbm = mel.eval('getenv \"XBMLANGPATH\"')\n"
        f"if icon_path not in current_xbm:\n"
        f"    mel.eval(f'putenv \"XBMLANGPATH\" \"{{current_xbm}}:/{{icon_path}}\"')\n"
        f"{PY_COMMENT}{END_MARKER}\n"
    )

    # MEL blocks
    mel_separator = ";" if get_os() == "Windows" else ":"
    mel_block = (
        f"{MEL_COMMENT}{SCRIPT_MARKER}\n"
        f"putenv(\"MAYA_SCRIPT_PATH\", `getenv \"MAYA_SCRIPT_PATH\"` + \"{mel_separator}{parent_dir}\");\n"
        f"{MEL_COMMENT}{END_MARKER}\n"
    )

    icon_mel_block = (
        f"{MEL_COMMENT}{ICON_MARKER}\n"
        f"putenv(\"XBMLANGPATH\", `getenv \"XBMLANGPATH\"` + \":/{icon_dir}\");\n"
        f"{MEL_COMMENT}{END_MARKER}\n"
    )

    os.makedirs(maya_scripts_dir, exist_ok=True)

    # Write blocks (removes existing ones first)
    _append_block(user_py, SCRIPT_MARKER, END_MARKER, py_block)
    _append_block(user_py, ICON_MARKER, END_MARKER, icon_py_block)
    _append_block(user_mel, SCRIPT_MARKER, END_MARKER, mel_block)
    _append_block(user_mel, ICON_MARKER, END_MARKER, icon_mel_block)


def install_shelf(tools_dir: str, maya_prefs_dir: str) -> bool:
    """
    Copy shelf files from atlas_matrix/setup/shelves to Maya prefs.

    Args:
        tools_dir (str): Path to the atlas_matrix directory.
        maya_prefs_dir (str): Path to Maya preferences directory.

    Returns:
        bool: True if shelf installation succeeded, False otherwise.
    """
    source_shelf_dir = os.path.join(tools_dir, "setup", "shelves")
    dest_shelf_dir = os.path.join(maya_prefs_dir, "prefs", "shelves")

    source_shelf_dir = _norm(source_shelf_dir)
    dest_shelf_dir = _norm(dest_shelf_dir)

    if not os.path.exists(source_shelf_dir):
        print(f"Shelf source not found: {source_shelf_dir}")
        return False

    os.makedirs(dest_shelf_dir, exist_ok=True)

    shelf_files = [f for f in os.listdir(source_shelf_dir) if f.startswith("shelf_")]
    if not shelf_files:
        print(f"No shelf files found in {source_shelf_dir}")
        return False

    for shelf_file in shelf_files:
        src = os.path.join(source_shelf_dir, shelf_file)
        dst = os.path.join(dest_shelf_dir, shelf_file)
        try:
            shutil.copy2(src, dst)
            print(f"Copied shelf: {shelf_file}")
        except Exception as e:
            print(f"Failed to copy {shelf_file}: {e}")
            return False

    return True


def install_icons(atlas_dir: str, maya_prefs_dir: str) -> bool:
    """
    Copy icon files from atlas_matrix/setup/icons to Maya prefs/icons.

    Args:
        atlas_dir (str): Path to the atlas_matrix directory.
        maya_prefs_dir (str): Path to Maya preferences directory.

    Returns:
        bool: True if at least one icon was copied, False otherwise.
    """
    src = _norm(os.path.join(atlas_dir, "setup", "icons"))
    dst = _norm(os.path.join(maya_prefs_dir, "prefs", "icons"))
    folder_name = "atlas_matrix_icons"

    if not os.path.isdir(src):
        print(f"Icons source not found: {src}")
        return False

    os.makedirs(dst, exist_ok=True)
    copied = 0

    try:
        shutil.copytree(os.path.join(src, folder_name), os.path.join(dst, folder_name))
        copied += 1
    except Exception as e:
        print(f"Failed to copy icon folder {folder_name}: {e}")

    if copied > 0:
        print(f"Copied {copied} icon(s) to {dst}")
        return True
    else:
        print(f"No icons found to copy from {src}")
        return False


def _inject_runtime_paths_now(tools_dir: str) -> None:
    """
    Make the current Maya session ready immediately without restart.

    Adds script and icon paths to the current session's environment.

    Args:
        tools_dir (str): Path to the atlas_matrix directory.
    """
    atlas_dir = _norm(tools_dir)
    parent_dir = _norm(os.path.dirname(atlas_dir))
    icon_dir = _norm(os.path.join(atlas_dir, "setup", "icons"))

    # Python import path
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
        print(f"Added to sys.path (runtime): {parent_dir}")

    # MEL script path
    sep = ";" if get_os() == "Windows" else ":"
    ms_path = os.environ.get("MAYA_SCRIPT_PATH", "")
    if parent_dir not in ms_path.split(sep):
        os.environ["MAYA_SCRIPT_PATH"] = (ms_path + (sep if ms_path else "") + parent_dir)
        print(f"Added to MAYA_SCRIPT_PATH (runtime)")

    # XBMLANGPATH (icons)
    try:
        current_xbm = mel.eval('getenv "XBMLANGPATH"')
        if icon_dir not in current_xbm:
            mel.eval(f'putenv "XBMLANGPATH" "{current_xbm}:/{icon_dir}"')
            print(f"Added icon path to current session")
    except Exception:
        print("Could not update XBMLANGPATH in current session")
        traceback.print_exc()


def _load_shelf_now(shelf_name: str = "AtlasMatrix") -> None:
    """
    Load the shelf into the current session immediately.

    Expects a file named shelf_<shelf_name>.mel in prefs/shelves.

    Args:
        shelf_name (str): Name of the shelf to load (default: 'AtlasMatrix').
    """
    try:
        mel.eval(f'loadNewShelf "shelf_{shelf_name}"')
        mel.eval('global string $gShelfTopLevel;')
        mel.eval(f'shelfTabLayout -e -selectTab "{shelf_name}" $gShelfTopLevel;')
        print(f"Shelf '{shelf_name}' loaded in current session")
    except Exception:
        print("Could not load shelf immediately (it will appear on next launch)")
        traceback.print_exc()


# ---------- INSTALLATION ----------


def install() -> None:
    """
    Main installation function for Atlas Matrix.

    Performs the following steps:
    1. Configures userSetup.py and userSetup.mel with script/icon paths
    2. Injects paths into current Maya session
    3. Copies shelf files to Maya prefs
    4. Copies icon files to Maya prefs
    5. Loads shelf in current session
    """
    this_file = _norm(__file__)
    atlas_dir = _norm(os.path.dirname(this_file))
    parent_dir = _norm(os.path.dirname(atlas_dir))
    user_platform = get_os()
    maya_version = get_maya_version()

    maya_prefs_dir = _norm(get_maya_prefs_dir(maya_version, user_platform))
    maya_scripts_dir = _norm(os.path.join(maya_prefs_dir, "scripts"))

    os.makedirs(maya_scripts_dir, exist_ok=True)

    print("=" * 60)
    print("ATLAS MATRIX INSTALLATION")
    print("=" * 60)

    # Write idempotent userSetup blocks
    write_usersetup_blocks(atlas_dir, maya_scripts_dir)

    # Apply paths to the current session (no restart required)
    _inject_runtime_paths_now(atlas_dir)

    # Install shelf files
    shelf_ok = install_shelf(atlas_dir, maya_prefs_dir)

    # Install icons
    icons_ok = install_icons(atlas_dir, maya_prefs_dir)

    # Try to load the shelf right now
    if shelf_ok:
        _load_shelf_now("AtlasMatrix")

    # Final dialog
    parts = [
        "Atlas Matrix installed successfully!",
        f"\nMaya Version: {maya_version}",
        f"Scripts path: {maya_scripts_dir}",
        f"Package dir (import root): {parent_dir}",
        "\n✓ Script path configured",
        "✓ Icon path configured",
    ]

    if shelf_ok:
        parts.append("✓ Shelf files copied & loaded")
    else:
        parts.append("⚠ Shelf installation had issues (check Script Editor)")

    if icons_ok:
        parts.append("✓ Icon files copied")
    else:
        parts.append("⚠ Icon installation had issues (check Script Editor)")

    print("\n" + "\n".join(parts))
    print("=" * 60)

    cmds.confirmDialog(title="Installation Complete", message="\n".join(parts), button=["OK"])


def onMayaDroppedPythonFile(*args, **kwargs) -> None:
    """
    Entry point for Maya drag-and-drop installation.

    This function is automatically called by Maya when the script is dropped
    into the viewport.

    Args:
        *args: Variable positional arguments (unused).
        **kwargs: Variable keyword arguments (unused).
    """
    install()


if __name__ == "__main__":
    install()