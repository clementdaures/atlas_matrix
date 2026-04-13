# -*- coding: utf-8 -*-
"""
Atlas Matrix Parent Constraint Dialog
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

from atlas_matrix.ui.pyside_compat import (
    QtWidgets, QtCore, QtGui,
    QDoubleValidator,
    get_maya_main_window,
    PYSIDE_VERSION
)

import maya.cmds as cmds

from atlas_matrix.core.parent_con import ParentCon, AxisFilter, AxisWeights
from atlas_matrix.ui.parent_con.matrix_parent_con_ui import AtlasMatrixParentUi


# ---------- FUNCTIONS ----------


def _float01(text: str, fallback: float = 1.0) -> float:
    """
    Parse a float in [0, 1] from a string, with clamping and fallback.

    Args:
        text (str): Input text expected to represent a number.
        fallback (float): Value to return if parsing fails.

    Returns:
        float: The parsed number clamped to [0.0, 1.0], or `fallback` on error.
    """
    try:
        v = float(text)
        return max(0.0, min(1.0, v))
    except Exception:
        return fallback


def _wire_axis_group(all_cb, x_cb, y_cb, z_cb):
    """
    Wire an "All" checkbox to enable/disable per-axis checkboxes.

    When the "All" checkbox is checked, X/Y/Z are forced to True and disabled.
    When it's unchecked, X/Y/Z become user-editable.

    Args:
        all_cb (QCheckBox): Master "All" checkbox.
        x_cb (QCheckBox): X-axis checkbox.
        y_cb (QCheckBox): Y-axis checkbox.
        z_cb (QCheckBox): Z-axis checkbox.
    """
    def on_all_toggled(checked):
        x_cb.setEnabled(not checked)
        y_cb.setEnabled(not checked)
        z_cb.setEnabled(not checked)
        if checked:
            x_cb.setChecked(True)
            y_cb.setChecked(True)
            z_cb.setChecked(True)
    all_cb.toggled.connect(on_all_toggled)
    on_all_toggled(all_cb.isChecked())


def _wire_weight_pair(slider, lineedit):
    """
    Synchronize a slider (0–100) with a line edit (0.00–1.00).

    The slider represents a percentage (int 0..100). The line edit shows a
    normalized weight (float 0.00..1.00) with validation and clamping.

    Wiring:
        - Slider → LineEdit via `valueChanged`
        - LineEdit → Slider via `editingFinished`

    Args:
        slider (QSlider): Slider widget to configure and listen to.
        lineedit (QLineEdit): Line edit that displays the normalized value.

    Side Effects:
        - Sets a `QDoubleValidator(0.0, 1.0, 3)` on the line edit.
        - Initializes text to "1.00" if empty and syncs the slider.
    """
    slider.setRange(0, 100)
    lineedit.setValidator(QDoubleValidator(0.0, 1.0, 3, lineedit))

    def s_to_e(val):
        lineedit.setText(f"{val/100.0:.2f}")

    def e_to_s():
        slider.setValue(int(_float01(lineedit.text(), 1.0) * 100))

    slider.valueChanged.connect(s_to_e)
    lineedit.editingFinished.connect(e_to_s)

    if not lineedit.text():
        lineedit.setText("1.00")
    e_to_s()


def _ui_to_parentcon_kwargs(ui: AtlasMatrixParentUi):
    """
    Read UI state and convert it to keyword arguments for `ParentCon`.

    This collects axis filters (All vs X/Y/Z per group) and per-channel weights,
    as well as general flags (offset, keep_hold, envelope).

    Args:
        ui (AtlasMatrixParentUi): The instantiated UI containing all widgets.

    Returns:
        dict: Keyword arguments ready to be expanded into `ParentCon(...)`, with:
            - offset (bool)
            - keep_hold (bool)
            - envelope (bool)
            - translate_filter (AxisFilter)
            - rotate_filter (AxisFilter)
            - scale_filter (AxisFilter)
            - shear_filter (AxisFilter)
            - weights (AxisWeights)
    """
    t_all = ui.checkbox_parent_translate_all.isChecked()
    r_all = ui.checkbox_parent_rotate_all.isChecked()
    s_all = ui.checkbox_parent_scale_all.isChecked()
    sh_all = ui.checkbox_parent_shear_all.isChecked()

    translate_filter = AxisFilter(
        x=True if t_all else ui.checkbox_parent_translate_x.isChecked(),
        y=True if t_all else ui.checkbox_parent_translate_y.isChecked(),
        z=True if t_all else ui.checkbox_parent_translate_z.isChecked(),
    )
    rotate_filter = AxisFilter(
        x=True if r_all else ui.checkbox_parent_rotate_x.isChecked(),
        y=True if r_all else ui.checkbox_parent_rotate_y.isChecked(),
        z=True if r_all else ui.checkbox_parent_rotate_z.isChecked(),
    )
    scale_filter = AxisFilter(
        x=True if s_all else ui.checkbox_parent_scale_x.isChecked(),
        y=True if s_all else ui.checkbox_parent_scale_y.isChecked(),
        z=True if s_all else ui.checkbox_parent_scale_z.isChecked(),
    )
    shear_filter = AxisFilter(
        x=True if sh_all else ui.checkbox_parent_shear_x.isChecked(),
        y=True if sh_all else ui.checkbox_parent_shear_y.isChecked(),
        z=True if sh_all else ui.checkbox_parent_shear_z.isChecked(),
    )

    weights = AxisWeights(
        translate=_float01(ui.lineedit_parent_translate_weight.text() or "1"),
        rotate=_float01(ui.lineedit_parent_rotate_weight.text() or "1"),
        scale=_float01(ui.lineedit_parent_scale_weight.text() or "1"),
        shear=_float01(ui.lineedit_parent_scale_shear_weight.text() or "1"),
        all=_float01(ui.lineedit_parent_global_weight.text() or "1")
    )

    return dict(
        offset=ui.checkbox_parent_offset.isChecked(),
        keep_hold=ui.checkbox_parent_hold.isChecked(),
        envelope=ui.checkbox_parent_enveloppe.isChecked(),
        translate_filter=translate_filter,
        rotate_filter=rotate_filter,
        scale_filter=scale_filter,
        shear_filter=shear_filter,
        weights=weights,
    )


def _delete_existing(object_name: str):
    """
    Close and delete any existing widget with a given object name.

    Useful for ensuring a single instance of a dialog in Maya/Qt environments.

    Args:
        object_name (str): The `QObject.objectName()` to search for.

    Side Effects:
        - Closes matching widgets and schedules them for deletion.
    """
    for w in QtWidgets.QApplication.allWidgets():
        if w.objectName() == object_name:
            w.close()
            w.deleteLater()


class AtlasMatrixParentDlg(QtWidgets.QDialog):
    """
    Dialog controller for the Atlas Parent Matrix constraint tool.

    This dialog hosts the generated `AtlasMatrixParentUi`, wires UX helpers
    (axis groups, weight pairs, toggle guards), and triggers the construction
    of a matrix-based parent constraint via `ParentCon`.
    """

    OBJECT_NAME = "AtlasMatrixParentDlg"

    def __init__(self, parent=None):
        """
        Construct the dialog, build UI, and wire interactions.

        Args:
            parent (Optional[QWidget]): Optional Qt parent widget.
        """
        _delete_existing(self.OBJECT_NAME)
        super().__init__(parent)
        self.setObjectName(self.OBJECT_NAME)
        self.setWindowTitle("Atlas – Parent Matrix")

        # setup UI
        self.ui = AtlasMatrixParentUi()
        self.ui.setupUi(self)

        # wire helpers
        _wire_axis_group(self.ui.checkbox_parent_translate_all,
                         self.ui.checkbox_parent_translate_x,
                         self.ui.checkbox_parent_translate_y,
                         self.ui.checkbox_parent_translate_z)
        _wire_axis_group(self.ui.checkbox_parent_rotate_all,
                         self.ui.checkbox_parent_rotate_x,
                         self.ui.checkbox_parent_rotate_y,
                         self.ui.checkbox_parent_rotate_z)
        _wire_axis_group(self.ui.checkbox_parent_scale_all,
                         self.ui.checkbox_parent_scale_x,
                         self.ui.checkbox_parent_scale_y,
                         self.ui.checkbox_parent_scale_z)
        _wire_axis_group(self.ui.checkbox_parent_shear_all,
                         self.ui.checkbox_parent_shear_x,
                         self.ui.checkbox_parent_shear_y,
                         self.ui.checkbox_parent_shear_z)

        _wire_weight_pair(self.ui.horizontalslider_parent_translate_weight,
                          self.ui.lineedit_parent_translate_weight)
        _wire_weight_pair(self.ui.horizontalslider_parent_rotate_weight,
                          self.ui.lineedit_parent_rotate_weight)
        _wire_weight_pair(self.ui.horizontalslider_parent_scale_weight,
                          self.ui.lineedit_parent_scale_weight)
        _wire_weight_pair(self.ui.horizontalslider_parent_shear_weight,
                          self.ui.lineedit_parent_scale_shear_weight)
        _wire_weight_pair(self.ui.horizontalslider_parent_global_weight,
                          self.ui.lineedit_parent_global_weight)

        # Keep hold only if offset
        self.ui.checkbox_parent_offset.toggled.connect(self.ui.checkbox_parent_hold.setEnabled)
        self.ui.checkbox_parent_hold.setEnabled(self.ui.checkbox_parent_offset.isChecked())

        self.ui.button_parent_apply.clicked.connect(self._on_build)
        self.ui.button_parent_add.clicked.connect(self._add_button)
        self.ui.button_parent_close.clicked.connect(self.close)

    def _on_build(self):
        """Build the constraint using the current selection and UI options."""
        sel = cmds.ls(sl=True) or []
        if len(sel) < 2:
            cmds.warning("Select at least one driver and a driven (last selected).")
            return
        driven, drivers = sel[-1], sel[:-1]

        print("=" * 60)
        print(f"Building constraint:")
        print(f"  Driven: {driven}")
        print(f"  Drivers: {drivers}")

        # Check if objects actually exist
        for obj in [driven] + drivers:
            exists = cmds.objExists(obj)
            print(f"  Object '{obj}' exists: {exists}")
            if not exists:
                cmds.warning(f"Object does not exist in scene: {obj}")
                return

        kwargs = _ui_to_parentcon_kwargs(self.ui)
        print(f"  Offset: {kwargs['offset']}")
        print(f"  Keep Hold: {kwargs['keep_hold']}")
        print("=" * 60)

        try:
            print("Creating ParentCon object...")
            con = ParentCon(driven=driven, drivers=drivers, **kwargs)
            print("✓ ParentCon object created")

            print("Calling mount_system()...")
            con.mount_system()
            print("✓ mount_system() completed")

            cmds.inViewMessage(amg="<hl>Matrix Parent Constraint created</hl>", pos="midCenter", fade=True)
        except Exception as e:
            cmds.warning(f"ParentCon failed: {e}")
            import traceback
            print("\n" + "=" * 60)
            print("FULL ERROR TRACEBACK:")
            print("=" * 60)
            traceback.print_exc()
            print("=" * 60)


    def _add_button(self):
        self._on_build()
        self.close()


DIALOG_ATTR = "_atlasMatrixParentDlg"


def _install_dialog_ref(dlg):
    """Store the dialog on Maya's main window; clean up when destroyed."""
    main = get_maya_main_window()
    if not main:
        return
    # close an existing one if present
    old = getattr(main, DIALOG_ATTR, None)
    if old and old is not dlg:
        try:
            old.close()
            old.deleteLater()
        except RuntimeError:
            pass
    # store the new one
    setattr(main, DIALOG_ATTR, dlg)

    # when dlg is destroyed, clear the reference
    dlg.destroyed.connect(lambda *_: setattr(main, DIALOG_ATTR, None))


def _get_existing_dialog():
    main = get_maya_main_window()
    return getattr(main, DIALOG_ATTR, None) if main else None


def show():
    """Show the Atlas Matrix Parent dialog with error handling."""
    try:
        print("Starting show() function...")
        print(f"Pyside version: {PYSIDE_VERSION}")

        main = get_maya_main_window()
        print(f"Maya main window: {main}")

        # Reuse if it exists
        existing = _get_existing_dialog()
        if existing:
            print(f"Found existing dialog: {existing}")
            existing.show()
            existing.raise_()
            existing.activateWindow()
            return existing

        # Otherwise create a new one
        print("Creating new dialog...")
        dlg = AtlasMatrixParentDlg(parent=main)
        print(f"Dialog created: {dlg}")

        _install_dialog_ref(dlg)
        print("Dialog reference installed")

        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

        print("Dialog should be visible now!")
        return dlg

    except Exception as e:
        import traceback
        print(f"Error in show(): {e}")
        traceback.print_exc()
        return None