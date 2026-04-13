# -*- coding: utf-8 -*-
"""
Atlas Matrix Uninstaller
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
import shutil
import platform
from typing import List

import maya.cmds as cmds

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


def remove_marked_block(filepath: str, start_marker: str, end_marker: str) -> bool:
    """
    Remove marked block from a userSetup file.

    Removes all lines between start_marker and end_marker (inclusive).

    Args:
        filepath (str): Path to the file to modify.
        start_marker (str): Starting marker to identify block.
        end_marker (str): Ending marker to identify block.

    Returns:
        bool: True if block was found and removed, False otherwise.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return True  # Nothing to remove, consider it success

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        skip_mode = False
        found_marker = False

        for line in lines:
            if start_marker in line:
                skip_mode = True
                found_marker = True
                continue
            if skip_mode and end_marker in line:
                skip_mode = False
                continue
            if not skip_mode:
                new_lines.append(line)

        if found_marker:
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"Removed Atlas Matrix block from {os.path.basename(filepath)}")
            return True
        else:
            print(f"No Atlas Matrix block found in {os.path.basename(filepath)}")
            return True

    except Exception as e:
        print(f"Failed to process {filepath}: {e}")
        return False


def remove_shelf(maya_prefs_dir: str) -> bool:
    """
    Remove the Atlas Matrix shelf from UI and disk.

    Deletes the shelf from the current Maya session and removes
    shelf files from the prefs/shelves directory.

    Args:
        maya_prefs_dir (str): Path to Maya preferences directory.

    Returns:
        bool: True if removal succeeded or nothing to remove, False on error.
    """
    dest_shelf_dir = os.path.join(maya_prefs_dir, "prefs", "shelves")

    print(f"Checking shelf directory: {dest_shelf_dir}")

    # Remove from UI first
    shelf_ui_names = ["AtlasMatrix", "Atlas"]
    for shelf_ui in shelf_ui_names:
        if cmds.shelfLayout(shelf_ui, exists=True):
            try:
                cmds.deleteUI(shelf_ui, layout=True)
                print(f"Shelf UI '{shelf_ui}' deleted from Maya session")
            except Exception as e:
                print(f"Failed to delete shelf UI '{shelf_ui}': {e}")

    # Remove files from disk
    if not os.path.exists(dest_shelf_dir):
        print(f"Shelf directory not found: {dest_shelf_dir}")
        return True

    shelf_files = os.listdir(dest_shelf_dir)
    shelf_prefixes = ["shelf_AtlasMatrix", "shelf_Atlas"]
    valid_extensions = [".mel", ".json"]
    removed_count = 0

    for shelf_file in shelf_files:
        if any(shelf_file.startswith(prefix) and shelf_file.endswith(ext)
               for prefix in shelf_prefixes for ext in valid_extensions):
            shelf_path = os.path.join(dest_shelf_dir, shelf_file)
            try:
                os.remove(shelf_path)
                print(f"Removed shelf file: {shelf_file}")
                removed_count += 1
            except Exception as e:
                print(f"Failed to remove {shelf_file}: {e}")

    if removed_count == 0:
        print("No matching Atlas Matrix shelf files found to remove")

    return True


def remove_icons(maya_prefs_dir: str) -> bool:
    """
    Remove Atlas Matrix icon files from Maya prefs/icons directory.

    Attempts to identify and remove icon files that were installed by
    Atlas Matrix. Only removes files with Atlas-related prefixes.

    Args:
        maya_prefs_dir (str): Path to Maya preferences directory.

    Returns:
        bool: True if removal succeeded or nothing to remove, False on error.
    """
    icons_dir = os.path.join(maya_prefs_dir, "prefs", "icons")
    folder_name = "atlas_matrix_icons"

    if not os.path.exists(icons_dir):
        print(f"Icons directory not found: {icons_dir}")
        return True

    removed_count = 0

    try:
        icon_path = os.path.join(icons_dir, folder_name)
        try:
            shutil.rmtree(icon_path)
            print(f"Removed icon: {folder_name}")
            removed_count += 1
        except Exception as e:
            print(f"Failed to remove icon {folder_name}: {e}")

        if removed_count == 0:
            print("No Atlas Matrix icons found to remove")
        else:
            print(f"Removed {removed_count} icon file(s)")

        return True

    except Exception as e:
        print(f"Error processing icons directory: {e}")
        return False


def uninstall() -> None:
    """
    Main uninstallation function for Atlas Matrix.

    Performs the following steps:
    1. Removes script path blocks from userSetup files
    2. Removes icon path blocks from userSetup files
    3. Removes shelf files and UI elements
    4. Removes icon files from Maya prefs
    """
    user_platform = get_os()
    maya_version = get_maya_version()

    maya_prefs_dir = _norm(get_maya_prefs_dir(maya_version, user_platform))
    maya_scripts_dir = _norm(os.path.join(maya_prefs_dir, "scripts"))

    print("=" * 60)
    print("ATLAS MATRIX UNINSTALLATION")
    print("=" * 60)

    success_list: List[bool] = []

    # Remove script path blocks from userSetup files
    mel_file = os.path.join(maya_scripts_dir, "userSetup.mel")
    py_file = os.path.join(maya_scripts_dir, "userSetup.py")

    success_list.append(remove_marked_block(mel_file, f"{MEL_COMMENT}{SCRIPT_MARKER}", f"{MEL_COMMENT}{END_MARKER}"))
    success_list.append(remove_marked_block(py_file, f"{PY_COMMENT}{SCRIPT_MARKER}", f"{PY_COMMENT}{END_MARKER}"))

    # Remove icon path blocks from userSetup files
    success_list.append(remove_marked_block(mel_file, f"{MEL_COMMENT}{ICON_MARKER}", f"{MEL_COMMENT}{END_MARKER}"))
    success_list.append(remove_marked_block(py_file, f"{PY_COMMENT}{ICON_MARKER}", f"{PY_COMMENT}{END_MARKER}"))

    # Remove shelf
    success_list.append(remove_shelf(maya_prefs_dir))

    # Remove icons
    success_list.append(remove_icons(maya_prefs_dir))

    # Build result message
    all_success = all(success_list)

    message_parts = [
        f"Atlas Matrix Uninstallation Complete!",
        f"\nMaya Version: {maya_version}",
        f"Script directory: {maya_scripts_dir}",
    ]

    if all_success:
        message_parts.append("\n✓ Script paths removed from userSetup files")
        message_parts.append("✓ Icon paths removed from userSetup files")
        message_parts.append("✓ Shelf files removed")
        message_parts.append("✓ Icon files removed")
        message_parts.append("\n⚠ Please restart Maya to complete uninstallation.")
        message_parts.append("\nNote: The Atlas Matrix tool files themselves were not deleted.")
        message_parts.append("You can safely delete the atlas_matrix folder manually if desired.")
    else:
        message_parts.append("\n⚠ Some steps encountered issues (check Script Editor for details)")

    print("\n" + "\n".join(message_parts))
    print("=" * 60)

    cmds.confirmDialog(
        title="Uninstallation Complete",
        message="\n".join(message_parts),
        button=["OK"]
    )


def onMayaDroppedPythonFile(*args, **kwargs) -> None:
    """
    Entry point for Maya drag-and-drop uninstallation.

    This function is automatically called by Maya when the script is dropped
    into the viewport.

    Args:
        *args: Variable positional arguments (unused).
        **kwargs: Variable keyword arguments (unused).
    """
    uninstall()


if __name__ == "__main__":
    uninstall()