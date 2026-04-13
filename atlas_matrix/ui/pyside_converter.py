# -*- coding: utf-8 -*-
"""
Script to convert PySide6 UI files to work with both PySide2 and PySide6
Run this to update your atlas_matrix_parent_ui.py file

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

import re
import os


# ---------- FUNCTIONS ----------

def convert_ui_file(input_file: str, output_file: str):
    """
    Convert a PySide6 UI file to be compatible with both PySide2 and PySide6.

    Args:
        input_file (str): Path to the original PySide6 UI file
        output_file (str): Path where the compatible UI file will be saved
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"   Error: Input file not found: {input_file}")
        print(f"   Current working directory: {os.getcwd()}")
        print(f"   Looking for: {os.path.abspath(input_file)}")
        return False

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # New imports section
    new_imports = '''# -*- coding: utf-8 -*-
"""
Auto-generated UI file - Compatible with PySide2 and PySide6
"""

from ui.pyside_compat import QtCore, QtGui, QtWidgets

# For backwards compatibility
QCoreApplication = QtCore.QCoreApplication
QMetaObject = QtCore.QMetaObject

'''

    # Find everything from the first import to the last import before the class
    import_pattern = r'# -\*- coding: utf-8 -\*-.*?(?=class\s+\w+\s*\(object\):)'
    content = re.sub(import_pattern, '', content, flags=re.DOTALL)

    # Add the new imports at the top
    content = new_imports + content

    # List of QtWidgets classes that need to be prefixed
    qtwidgets_classes = [
        'QApplication', 'QWidget', 'QMainWindow', 'QDialog', 'QPushButton',
        'QLabel', 'QLineEdit', 'QTextEdit', 'QCheckBox', 'QRadioButton',
        'QComboBox', 'QSpinBox', 'QDoubleSpinBox', 'QSlider', 'QProgressBar',
        'QGroupBox', 'QTabWidget', 'QTableWidget', 'QTreeWidget', 'QListWidget',
        'QVBoxLayout', 'QHBoxLayout', 'QGridLayout', 'QFormLayout', 'QStackedLayout',
        'QSplitter', 'QScrollArea', 'QFrame', 'QSizePolicy', 'QSpacerItem',
        'QMenuBar', 'QMenu', 'QToolBar', 'QStatusBar', 'QAction',
        'QFileDialog', 'QColorDialog', 'QFontDialog', 'QMessageBox',
        'QInputDialog', 'QGraphicsView', 'QGraphicsScene', 'QDockWidget'
    ]

    for widget_class in qtwidgets_classes:
        content = re.sub(
            rf'\b(?<!QtWidgets\.)({widget_class})\b',
            rf'QtWidgets.\1',
            content
        )

    # QSizePolicy.Policy.Minimum -> QSizePolicy.Minimum
    content = re.sub(r'QtWidgets\.QSizePolicy\.Policy\.(\w+)', r'QtWidgets.QSizePolicy.\1', content)

    # QFrame.Shape.VLine -> QFrame.VLine
    content = re.sub(r'QtWidgets\.QFrame\.Shape\.(\w+)', r'QtWidgets.QFrame.\1', content)

    # QFrame.Shadow.Sunken -> QFrame.Sunken
    content = re.sub(r'QtWidgets\.QFrame\.Shadow\.(\w+)', r'QtWidgets.QFrame.\1', content)

    # Qt.AlignmentFlag.AlignCenter -> Qt.AlignCenter
    content = re.sub(r'Qt\.AlignmentFlag\.(\w+)', r'QtCore.Qt.\1', content)

    # Qt.Orientation.Horizontal -> Qt.Horizontal
    content = re.sub(r'Qt\.Orientation\.(\w+)', r'QtCore.Qt.\1', content)

    # Fix standalone Qt. references to QtCore.Qt.
    content = re.sub(r'\bQt\.(\w+)', r'QtCore.Qt.\1', content)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Converted {input_file} -> {output_file}")
    print(f"File is now compatible with both PySide2 (Maya 2020-2024) and PySide6 (Maya 2025+)")
    return True


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    input_file = os.path.join(script_dir, "qt_designer", "matrix_parent_con_ui_qt6.py")
    output_file = os.path.join(script_dir, "parent_con", "matrix_parent_con_ui.py")

    convert_ui_file(input_file, output_file)