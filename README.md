# Atlas Matrix – Open Source Maya Constraint Tool

**Author**: Clement Daures
**Version**: 1.0.0  
**Compatible with**: Autodesk Maya 2020+ (PySide5)
**State**: Still in development
**License**: Apache 2.0

---

## About  

**Atlas Matrix** is a powerful and user-friendly tool designed to simplify and streamline the process of creating and managing matrix-based constraints in Maya.

It features a clean, tabbed interface that supports:
- Parent constraints with fine control over axes and weights
- Aim constraints with full vector and up-vector configuration (placeholder for future development)
- Remove constraints
- Manager panel (placeholder for future development)

Atlas Matrix is fully built with **PySide6** and supports Maya 2025’s native Qt6 backend. 
Code is adapted to run on **PySide2**
---

## Installation

1. Open Maya (2020+).
2. Drag and drop the file `atlas_matrix/install.py` directly into your Maya viewport.
3. Restart Maya.
4. You’ll now see a new shelf named **AtlasMatrix** in your Maya shelf bar.

*That’s it! You’re ready to use Atlas Matrix.*

FOR MANUAL INSTALLATION, PLEASE REFER TO `docs/01_getting_started/b_installation.md`

---

## Features

### Matrix Parent Constraint
- Maintain offset
- Hold state toggle
- Axis control (Translate, Rotate, Scale)
- Axis weight sliders (LineEdit + Slider linked)
- Axis selection control (X, Y, Z)

### Matrix Aim Constraint
- Aim & Up vector configuration
- Target vectors with XYZ inputs
- World up type selection
- Hold and offset toggles

### Matrix Constraint Remover
- Delete constraint on selected object

### Matrix Constraint Manager
- Placeholder for future constraint management tools

---

## How to use

- Refer to `docs/02_user_guide/`

---

## Development Notes

- Built using **Qt Designer** and compiled via `pyside6-uic`
- Uses `wrapInstance()` and `OpenMayaUI` for clean integration with Maya main window
- Avoids global variables through class-based singleton window handling

---

## Compatibility

| Maya Version | Qt Version    | Compatible  |
|--------------|---------------|-------------|
| 2025+        | PySide6 / Qt6 |     Yes     |
| 2020 - 2024  | PySide2 / Qt5 |     Yes     |

---

## Contact

**Author**: Clement Daures  
Email: [clementdaures.contact@gmail.com](mailto:clementdaures.contact@gmail.com)  
IG: [@theriggingatlas](https://instagram.com/theriggingatlas) or [@clementdaures](https://instagram.com/clementdaures)

---

## License

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
