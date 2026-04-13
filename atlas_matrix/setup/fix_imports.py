#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to fix imports in atlas_matrix package
Converts relative imports to absolute package imports

Usage:
    python fix_imports.py

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

import os
import re
from pathlib import Path


def fix_imports_in_file(filepath: Path, package_name: str = "atlas_matrix") -> bool:
    """
    Fix imports in a single Python file.

    Args:
        filepath: Path to the Python file
        package_name: Root package name (default: "atlas_matrix")

    Returns:
        True if file was modified, False otherwise
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Patterns to fix:
    # from core.something import X  ->  from atlas_matrix.core.something import X
    # from ui.something import X    ->  from atlas_matrix.ui.something import X
    # import core.something         ->  import atlas_matrix.core.something

    patterns = [
        # Pattern 1: from core. / from ui. / etc.
        (r'^from (core|ui|setup)\.', rf'from {package_name}.\1.'),

        # Pattern 2: import core. / import ui. / etc.
        (r'^import (core|ui|setup)\.', rf'import {package_name}.\1.'),

        # Pattern 3: from core import / from ui import
        (r'^from (core|ui|setup) import', rf'from {package_name}.\1 import'),
    ]

    # Apply each pattern
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # Check if anything changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def find_python_files(root_dir: Path, exclude_dirs: set = None) -> list:
    """
    Find all Python files in directory tree.

    Args:
        root_dir: Root directory to search
        exclude_dirs: Set of directory names to exclude

    Returns:
        List of Path objects for Python files
    """
    if exclude_dirs is None:
        exclude_dirs = {'__pycache__', '.git', '.idea', 'venv', 'env'}

    python_files = []

    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories from search
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)

    return python_files


def main():
    """Main execution function"""
    # Get script directory
    script_dir = Path(__file__).parent.absolute()

    # Assume atlas_matrix is the parent directory of this script
    # Adjust if your structure is different
    atlas_matrix_dir = script_dir.parent if script_dir.name == "setup" else script_dir

    print("=" * 60)
    print("Atlas Matrix Import Fixer")
    print("=" * 60)
    print(f"Scanning directory: {atlas_matrix_dir}")
    print()

    # Find all Python files
    python_files = find_python_files(atlas_matrix_dir)

    if not python_files:
        print("No Python files found!")
        return

    print(f"Found {len(python_files)} Python files")
    print()

    # Process each file
    modified_count = 0
    modified_files = []

    for filepath in python_files:
        relative_path = filepath.relative_to(atlas_matrix_dir)

        if fix_imports_in_file(filepath):
            modified_count += 1
            modified_files.append(relative_path)
            print(f"✓ Fixed: {relative_path}")

    # Summary
    print()
    print("=" * 60)
    print(f"Summary: {modified_count} file(s) modified")
    print("=" * 60)

    if modified_files:
        print("\nModified files:")
        for file in modified_files:
            print(f"  • {file}")
    else:
        print("\nAll imports are already correct")


if __name__ == "__main__":
    main()