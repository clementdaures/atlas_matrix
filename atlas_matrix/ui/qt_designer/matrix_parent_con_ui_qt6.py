# -*- coding: utf-8 -*-
"""
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
################################################################################
## Form generated from reading UI file 'atlas_matrix_parent.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QVBoxLayout, QWidget)

class AtlasMatrixParentUi(object):
    def setupUi(self, atlas_matrix_parent):
        if not atlas_matrix_parent.objectName():
            atlas_matrix_parent.setObjectName(u"atlas_matrix_parent")
        atlas_matrix_parent.resize(650, 472)
        self.verticalLayout = QVBoxLayout(atlas_matrix_parent)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontallayout_parent_stick_checkbox = QHBoxLayout()
        self.horizontallayout_parent_stick_checkbox.setSpacing(0)
        self.horizontallayout_parent_stick_checkbox.setObjectName(u"horizontallayout_parent_stick_checkbox")
        self.vertical_spacer_parent_stick_checkbox = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.horizontallayout_parent_stick_checkbox.addItem(self.vertical_spacer_parent_stick_checkbox)

        self.horizontallayout_parent_checkbox = QHBoxLayout()
        self.horizontallayout_parent_checkbox.setSpacing(6)
        self.horizontallayout_parent_checkbox.setObjectName(u"horizontallayout_parent_checkbox")
        self.horizontallayout_parent_offset = QHBoxLayout()
        self.horizontallayout_parent_offset.setObjectName(u"horizontallayout_parent_offset")
        self.label_parent_offset = QLabel(atlas_matrix_parent)
        self.label_parent_offset.setObjectName(u"label_parent_offset")

        self.horizontallayout_parent_offset.addWidget(self.label_parent_offset)

        self.checkbox_parent_offset = QCheckBox(atlas_matrix_parent)
        self.checkbox_parent_offset.setObjectName(u"checkbox_parent_offset")
        self.checkbox_parent_offset.setChecked(False)

        self.horizontallayout_parent_offset.addWidget(self.checkbox_parent_offset)


        self.horizontallayout_parent_checkbox.addLayout(self.horizontallayout_parent_offset)

        self.horizontallayout_parent_hold = QHBoxLayout()
        self.horizontallayout_parent_hold.setObjectName(u"horizontallayout_parent_hold")
        self.label_parent_hold = QLabel(atlas_matrix_parent)
        self.label_parent_hold.setObjectName(u"label_parent_hold")

        self.horizontallayout_parent_hold.addWidget(self.label_parent_hold)

        self.checkbox_parent_hold = QCheckBox(atlas_matrix_parent)
        self.checkbox_parent_hold.setObjectName(u"checkbox_parent_hold")
        self.checkbox_parent_hold.setEnabled(False)
        self.checkbox_parent_hold.setChecked(False)

        self.horizontallayout_parent_hold.addWidget(self.checkbox_parent_hold)


        self.horizontallayout_parent_checkbox.addLayout(self.horizontallayout_parent_hold)

        self.horizontallayout_parent_enveloppe = QHBoxLayout()
        self.horizontallayout_parent_enveloppe.setObjectName(u"horizontallayout_parent_enveloppe")
        self.label_parent_enveloppe = QLabel(atlas_matrix_parent)
        self.label_parent_enveloppe.setObjectName(u"label_parent_enveloppe")

        self.horizontallayout_parent_enveloppe.addWidget(self.label_parent_enveloppe)

        self.checkbox_parent_enveloppe = QCheckBox(atlas_matrix_parent)
        self.checkbox_parent_enveloppe.setObjectName(u"checkbox_parent_enveloppe")
        self.checkbox_parent_enveloppe.setChecked(True)

        self.horizontallayout_parent_enveloppe.addWidget(self.checkbox_parent_enveloppe)


        self.horizontallayout_parent_checkbox.addLayout(self.horizontallayout_parent_enveloppe)


        self.horizontallayout_parent_stick_checkbox.addLayout(self.horizontallayout_parent_checkbox)

        self.horizontallayout_parent_stick_checkbox.setStretch(1, 80)

        self.verticalLayout.addLayout(self.horizontallayout_parent_stick_checkbox)

        self.group_parent_constraint_axis = QGroupBox(atlas_matrix_parent)
        self.group_parent_constraint_axis.setObjectName(u"group_parent_constraint_axis")
        self.formLayout_2 = QFormLayout(self.group_parent_constraint_axis)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.form_parent_constraint_axis = QFormLayout()
        self.form_parent_constraint_axis.setObjectName(u"form_parent_constraint_axis")
        self.label_parent_translate_axis = QLabel(self.group_parent_constraint_axis)
        self.label_parent_translate_axis.setObjectName(u"label_parent_translate_axis")

        self.form_parent_constraint_axis.setWidget(0, QFormLayout.LabelRole, self.label_parent_translate_axis)

        self.horizontallayout_parent_translate_axis = QHBoxLayout()
        self.horizontallayout_parent_translate_axis.setObjectName(u"horizontallayout_parent_translate_axis")
        self.checkbox_parent_translate_all = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_translate_all.setObjectName(u"checkbox_parent_translate_all")
        self.checkbox_parent_translate_all.setChecked(True)

        self.horizontallayout_parent_translate_axis.addWidget(self.checkbox_parent_translate_all)

        self.separator_parent_axis_translate = QFrame(self.group_parent_constraint_axis)
        self.separator_parent_axis_translate.setObjectName(u"separator_parent_axis_translate")
        self.separator_parent_axis_translate.setFrameShape(QFrame.Shape.VLine)
        self.separator_parent_axis_translate.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontallayout_parent_translate_axis.addWidget(self.separator_parent_axis_translate)

        self.checkbox_parent_translate_x = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_translate_x.setObjectName(u"checkbox_parent_translate_x")
        self.checkbox_parent_translate_x.setEnabled(False)
        self.checkbox_parent_translate_x.setChecked(True)

        self.horizontallayout_parent_translate_axis.addWidget(self.checkbox_parent_translate_x)

        self.checkbox_parent_translate_y = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_translate_y.setObjectName(u"checkbox_parent_translate_y")
        self.checkbox_parent_translate_y.setEnabled(False)
        self.checkbox_parent_translate_y.setChecked(True)

        self.horizontallayout_parent_translate_axis.addWidget(self.checkbox_parent_translate_y)

        self.checkbox_parent_translate_z = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_translate_z.setObjectName(u"checkbox_parent_translate_z")
        self.checkbox_parent_translate_z.setEnabled(False)
        self.checkbox_parent_translate_z.setChecked(True)

        self.horizontallayout_parent_translate_axis.addWidget(self.checkbox_parent_translate_z)


        self.form_parent_constraint_axis.setLayout(0, QFormLayout.FieldRole, self.horizontallayout_parent_translate_axis)

        self.label_parent_translate_weight = QLabel(self.group_parent_constraint_axis)
        self.label_parent_translate_weight.setObjectName(u"label_parent_translate_weight")

        self.form_parent_constraint_axis.setWidget(1, QFormLayout.LabelRole, self.label_parent_translate_weight)

        self.horizontallayout_parent_translate_weight = QHBoxLayout()
        self.horizontallayout_parent_translate_weight.setObjectName(u"horizontallayout_parent_translate_weight")
        self.lineedit_parent_translate_weight = QLineEdit(self.group_parent_constraint_axis)
        self.lineedit_parent_translate_weight.setObjectName(u"lineedit_parent_translate_weight")
        self.lineedit_parent_translate_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_translate_weight.addWidget(self.lineedit_parent_translate_weight)

        self.horizontalslider_parent_translate_weight = QSlider(self.group_parent_constraint_axis)
        self.horizontalslider_parent_translate_weight.setObjectName(u"horizontalslider_parent_translate_weight")
        self.horizontalslider_parent_translate_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_translate_weight.addWidget(self.horizontalslider_parent_translate_weight)

        self.horizontallayout_parent_translate_weight.setStretch(0, 1)
        self.horizontallayout_parent_translate_weight.setStretch(1, 3)

        self.form_parent_constraint_axis.setLayout(1, QFormLayout.FieldRole, self.horizontallayout_parent_translate_weight)

        self.label_parent_rotates_axis = QLabel(self.group_parent_constraint_axis)
        self.label_parent_rotates_axis.setObjectName(u"label_parent_rotates_axis")

        self.form_parent_constraint_axis.setWidget(2, QFormLayout.LabelRole, self.label_parent_rotates_axis)

        self.horizontallayout_parent_rotate_axis = QHBoxLayout()
        self.horizontallayout_parent_rotate_axis.setObjectName(u"horizontallayout_parent_rotate_axis")
        self.checkbox_parent_rotate_all = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_rotate_all.setObjectName(u"checkbox_parent_rotate_all")
        self.checkbox_parent_rotate_all.setChecked(True)

        self.horizontallayout_parent_rotate_axis.addWidget(self.checkbox_parent_rotate_all)

        self.separator_parent_axis_rotate = QFrame(self.group_parent_constraint_axis)
        self.separator_parent_axis_rotate.setObjectName(u"separator_parent_axis_rotate")
        self.separator_parent_axis_rotate.setFrameShape(QFrame.Shape.VLine)
        self.separator_parent_axis_rotate.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontallayout_parent_rotate_axis.addWidget(self.separator_parent_axis_rotate)

        self.checkbox_parent_rotate_x = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_rotate_x.setObjectName(u"checkbox_parent_rotate_x")
        self.checkbox_parent_rotate_x.setEnabled(False)
        self.checkbox_parent_rotate_x.setCheckable(True)
        self.checkbox_parent_rotate_x.setChecked(True)

        self.horizontallayout_parent_rotate_axis.addWidget(self.checkbox_parent_rotate_x)

        self.checkbox_parent_rotate_y = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_rotate_y.setObjectName(u"checkbox_parent_rotate_y")
        self.checkbox_parent_rotate_y.setEnabled(False)
        self.checkbox_parent_rotate_y.setChecked(True)

        self.horizontallayout_parent_rotate_axis.addWidget(self.checkbox_parent_rotate_y)

        self.checkbox_parent_rotate_z = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_rotate_z.setObjectName(u"checkbox_parent_rotate_z")
        self.checkbox_parent_rotate_z.setEnabled(False)
        self.checkbox_parent_rotate_z.setChecked(True)

        self.horizontallayout_parent_rotate_axis.addWidget(self.checkbox_parent_rotate_z)


        self.form_parent_constraint_axis.setLayout(2, QFormLayout.FieldRole, self.horizontallayout_parent_rotate_axis)

        self.label_parent_rotate_weight = QLabel(self.group_parent_constraint_axis)
        self.label_parent_rotate_weight.setObjectName(u"label_parent_rotate_weight")

        self.form_parent_constraint_axis.setWidget(3, QFormLayout.LabelRole, self.label_parent_rotate_weight)

        self.horizontallayout_parent_rotate_weight = QHBoxLayout()
        self.horizontallayout_parent_rotate_weight.setObjectName(u"horizontallayout_parent_rotate_weight")
        self.lineedit_parent_rotate_weight = QLineEdit(self.group_parent_constraint_axis)
        self.lineedit_parent_rotate_weight.setObjectName(u"lineedit_parent_rotate_weight")
        self.lineedit_parent_rotate_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_rotate_weight.addWidget(self.lineedit_parent_rotate_weight)

        self.horizontalslider_parent_rotate_weight = QSlider(self.group_parent_constraint_axis)
        self.horizontalslider_parent_rotate_weight.setObjectName(u"horizontalslider_parent_rotate_weight")
        self.horizontalslider_parent_rotate_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_rotate_weight.addWidget(self.horizontalslider_parent_rotate_weight)

        self.horizontallayout_parent_rotate_weight.setStretch(0, 1)
        self.horizontallayout_parent_rotate_weight.setStretch(1, 3)

        self.form_parent_constraint_axis.setLayout(3, QFormLayout.FieldRole, self.horizontallayout_parent_rotate_weight)

        self.label_parent_scale_axis = QLabel(self.group_parent_constraint_axis)
        self.label_parent_scale_axis.setObjectName(u"label_parent_scale_axis")

        self.form_parent_constraint_axis.setWidget(4, QFormLayout.LabelRole, self.label_parent_scale_axis)

        self.checkbox_parent_scale_axis = QHBoxLayout()
        self.checkbox_parent_scale_axis.setObjectName(u"checkbox_parent_scale_axis")
        self.checkbox_parent_scale_all = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_scale_all.setObjectName(u"checkbox_parent_scale_all")
        self.checkbox_parent_scale_all.setChecked(True)

        self.checkbox_parent_scale_axis.addWidget(self.checkbox_parent_scale_all)

        self.separator_parent_axis_scale = QFrame(self.group_parent_constraint_axis)
        self.separator_parent_axis_scale.setObjectName(u"separator_parent_axis_scale")
        self.separator_parent_axis_scale.setFrameShape(QFrame.Shape.VLine)
        self.separator_parent_axis_scale.setFrameShadow(QFrame.Shadow.Sunken)

        self.checkbox_parent_scale_axis.addWidget(self.separator_parent_axis_scale)

        self.checkbox_parent_scale_x = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_scale_x.setObjectName(u"checkbox_parent_scale_x")
        self.checkbox_parent_scale_x.setEnabled(False)
        self.checkbox_parent_scale_x.setChecked(True)

        self.checkbox_parent_scale_axis.addWidget(self.checkbox_parent_scale_x)

        self.checkbox_parent_scale_y = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_scale_y.setObjectName(u"checkbox_parent_scale_y")
        self.checkbox_parent_scale_y.setEnabled(False)
        self.checkbox_parent_scale_y.setChecked(True)

        self.checkbox_parent_scale_axis.addWidget(self.checkbox_parent_scale_y)

        self.checkbox_parent_scale_z = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_scale_z.setObjectName(u"checkbox_parent_scale_z")
        self.checkbox_parent_scale_z.setEnabled(False)
        self.checkbox_parent_scale_z.setChecked(True)

        self.checkbox_parent_scale_axis.addWidget(self.checkbox_parent_scale_z)


        self.form_parent_constraint_axis.setLayout(4, QFormLayout.FieldRole, self.checkbox_parent_scale_axis)

        self.label_parent_scale_weight = QLabel(self.group_parent_constraint_axis)
        self.label_parent_scale_weight.setObjectName(u"label_parent_scale_weight")

        self.form_parent_constraint_axis.setWidget(5, QFormLayout.LabelRole, self.label_parent_scale_weight)

        self.horizontallayout_parent_scale_weight = QHBoxLayout()
        self.horizontallayout_parent_scale_weight.setObjectName(u"horizontallayout_parent_scale_weight")
        self.lineedit_parent_scale_weight = QLineEdit(self.group_parent_constraint_axis)
        self.lineedit_parent_scale_weight.setObjectName(u"lineedit_parent_scale_weight")
        self.lineedit_parent_scale_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_scale_weight.addWidget(self.lineedit_parent_scale_weight)

        self.horizontalslider_parent_scale_weight = QSlider(self.group_parent_constraint_axis)
        self.horizontalslider_parent_scale_weight.setObjectName(u"horizontalslider_parent_scale_weight")
        self.horizontalslider_parent_scale_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_scale_weight.addWidget(self.horizontalslider_parent_scale_weight)

        self.horizontallayout_parent_scale_weight.setStretch(0, 1)
        self.horizontallayout_parent_scale_weight.setStretch(1, 3)

        self.form_parent_constraint_axis.setLayout(5, QFormLayout.FieldRole, self.horizontallayout_parent_scale_weight)

        self.label_parent_shear_axis = QLabel(self.group_parent_constraint_axis)
        self.label_parent_shear_axis.setObjectName(u"label_parent_shear_axis")

        self.form_parent_constraint_axis.setWidget(6, QFormLayout.LabelRole, self.label_parent_shear_axis)

        self.checkbox_parent_shear_axis = QHBoxLayout()
        self.checkbox_parent_shear_axis.setObjectName(u"checkbox_parent_shear_axis")
        self.checkbox_parent_shear_all = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_shear_all.setObjectName(u"checkbox_parent_shear_all")
        self.checkbox_parent_shear_all.setChecked(True)

        self.checkbox_parent_shear_axis.addWidget(self.checkbox_parent_shear_all)

        self.separator_parent_axis_shear = QFrame(self.group_parent_constraint_axis)
        self.separator_parent_axis_shear.setObjectName(u"separator_parent_axis_shear")
        self.separator_parent_axis_shear.setFrameShape(QFrame.Shape.VLine)
        self.separator_parent_axis_shear.setFrameShadow(QFrame.Shadow.Sunken)

        self.checkbox_parent_shear_axis.addWidget(self.separator_parent_axis_shear)

        self.checkbox_parent_shear_x = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_shear_x.setObjectName(u"checkbox_parent_shear_x")
        self.checkbox_parent_shear_x.setEnabled(False)
        self.checkbox_parent_shear_x.setChecked(True)

        self.checkbox_parent_shear_axis.addWidget(self.checkbox_parent_shear_x)

        self.checkbox_parent_shear_y = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_shear_y.setObjectName(u"checkbox_parent_shear_y")
        self.checkbox_parent_shear_y.setEnabled(False)
        self.checkbox_parent_shear_y.setChecked(True)

        self.checkbox_parent_shear_axis.addWidget(self.checkbox_parent_shear_y)

        self.checkbox_parent_shear_z = QCheckBox(self.group_parent_constraint_axis)
        self.checkbox_parent_shear_z.setObjectName(u"checkbox_parent_shear_z")
        self.checkbox_parent_shear_z.setEnabled(False)
        self.checkbox_parent_shear_z.setChecked(True)

        self.checkbox_parent_shear_axis.addWidget(self.checkbox_parent_shear_z)


        self.form_parent_constraint_axis.setLayout(6, QFormLayout.FieldRole, self.checkbox_parent_shear_axis)

        self.label_parent_shear_weight = QLabel(self.group_parent_constraint_axis)
        self.label_parent_shear_weight.setObjectName(u"label_parent_shear_weight")

        self.form_parent_constraint_axis.setWidget(7, QFormLayout.LabelRole, self.label_parent_shear_weight)

        self.horizontallayout_parent_shear_weight = QHBoxLayout()
        self.horizontallayout_parent_shear_weight.setObjectName(u"horizontallayout_parent_shear_weight")
        self.lineedit_parent_scale_shear_weight = QLineEdit(self.group_parent_constraint_axis)
        self.lineedit_parent_scale_shear_weight.setObjectName(u"lineedit_parent_scale_shear_weight")
        self.lineedit_parent_scale_shear_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_shear_weight.addWidget(self.lineedit_parent_scale_shear_weight)

        self.horizontalslider_parent_shear_weight = QSlider(self.group_parent_constraint_axis)
        self.horizontalslider_parent_shear_weight.setObjectName(u"horizontalslider_parent_shear_weight")
        self.horizontalslider_parent_shear_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_shear_weight.addWidget(self.horizontalslider_parent_shear_weight)

        self.horizontallayout_parent_shear_weight.setStretch(0, 1)
        self.horizontallayout_parent_shear_weight.setStretch(1, 3)

        self.form_parent_constraint_axis.setLayout(7, QFormLayout.FieldRole, self.horizontallayout_parent_shear_weight)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.form_parent_constraint_axis)


        self.verticalLayout.addWidget(self.group_parent_constraint_axis)

        self.group_parent_global_weight = QGroupBox(atlas_matrix_parent)
        self.group_parent_global_weight.setObjectName(u"group_parent_global_weight")
        self.verticalLayout_2 = QVBoxLayout(self.group_parent_global_weight)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontallayout_parent_global_weight = QHBoxLayout()
        self.horizontallayout_parent_global_weight.setObjectName(u"horizontallayout_parent_global_weight")
        self.lineedit_parent_global_weight = QLineEdit(self.group_parent_global_weight)
        self.lineedit_parent_global_weight.setObjectName(u"lineedit_parent_global_weight")
        self.lineedit_parent_global_weight.setAlignment(Qt.AlignCenter)

        self.horizontallayout_parent_global_weight.addWidget(self.lineedit_parent_global_weight)

        self.horizontalslider_parent_global_weight = QSlider(self.group_parent_global_weight)
        self.horizontalslider_parent_global_weight.setObjectName(u"horizontalslider_parent_global_weight")
        self.horizontalslider_parent_global_weight.setOrientation(Qt.Horizontal)

        self.horizontallayout_parent_global_weight.addWidget(self.horizontalslider_parent_global_weight)

        self.horizontallayout_parent_global_weight.setStretch(0, 1)
        self.horizontallayout_parent_global_weight.setStretch(1, 3)

        self.verticalLayout_2.addLayout(self.horizontallayout_parent_global_weight)


        self.verticalLayout.addWidget(self.group_parent_global_weight)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.button_parent_add = QPushButton(atlas_matrix_parent)
        self.button_parent_add.setObjectName(u"button_parent_add")

        self.horizontalLayout_6.addWidget(self.button_parent_add)

        self.button_parent_apply = QPushButton(atlas_matrix_parent)
        self.button_parent_apply.setObjectName(u"button_parent_apply")

        self.horizontalLayout_6.addWidget(self.button_parent_apply)

        self.button_parent_close = QPushButton(atlas_matrix_parent)
        self.button_parent_close.setObjectName(u"button_parent_close")

        self.horizontalLayout_6.addWidget(self.button_parent_close)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.retranslateUi(atlas_matrix_parent)

        QMetaObject.connectSlotsByName(atlas_matrix_parent)
    # setupUi

    def retranslateUi(self, atlas_matrix_parent):
        atlas_matrix_parent.setWindowTitle(QCoreApplication.translate("atlas_matrix_parent", u"Matrix Parent Constraint Options - Atlas Matrix 1.0.0", None))
        self.label_parent_offset.setText(QCoreApplication.translate("atlas_matrix_parent", u"Maintain offset:", None))
        self.checkbox_parent_offset.setText("")
        self.label_parent_hold.setText(QCoreApplication.translate("atlas_matrix_parent", u"Keep hold:", None))
        self.checkbox_parent_hold.setText("")
        self.label_parent_enveloppe.setText(QCoreApplication.translate("atlas_matrix_parent", u"Enveloppe:", None))
        self.checkbox_parent_enveloppe.setText("")
        self.group_parent_constraint_axis.setTitle(QCoreApplication.translate("atlas_matrix_parent", u"Constraint axes:", None))
        self.label_parent_translate_axis.setText(QCoreApplication.translate("atlas_matrix_parent", u"Translate:", None))
        self.checkbox_parent_translate_all.setText(QCoreApplication.translate("atlas_matrix_parent", u"All", None))
        self.checkbox_parent_translate_x.setText(QCoreApplication.translate("atlas_matrix_parent", u"X", None))
        self.checkbox_parent_translate_y.setText(QCoreApplication.translate("atlas_matrix_parent", u"Y", None))
        self.checkbox_parent_translate_z.setText(QCoreApplication.translate("atlas_matrix_parent", u"Z", None))
        self.label_parent_translate_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"Weight:", None))
        self.lineedit_parent_translate_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"1.000", None))
        self.label_parent_rotates_axis.setText(QCoreApplication.translate("atlas_matrix_parent", u"Rotate:", None))
        self.checkbox_parent_rotate_all.setText(QCoreApplication.translate("atlas_matrix_parent", u"All", None))
        self.checkbox_parent_rotate_x.setText(QCoreApplication.translate("atlas_matrix_parent", u"X", None))
        self.checkbox_parent_rotate_y.setText(QCoreApplication.translate("atlas_matrix_parent", u"Y", None))
        self.checkbox_parent_rotate_z.setText(QCoreApplication.translate("atlas_matrix_parent", u"Z", None))
        self.label_parent_rotate_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"Weight:", None))
        self.lineedit_parent_rotate_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"1.000", None))
        self.label_parent_scale_axis.setText(QCoreApplication.translate("atlas_matrix_parent", u"Scale:", None))
        self.checkbox_parent_scale_all.setText(QCoreApplication.translate("atlas_matrix_parent", u"All", None))
        self.checkbox_parent_scale_x.setText(QCoreApplication.translate("atlas_matrix_parent", u"X", None))
        self.checkbox_parent_scale_y.setText(QCoreApplication.translate("atlas_matrix_parent", u"Y", None))
        self.checkbox_parent_scale_z.setText(QCoreApplication.translate("atlas_matrix_parent", u"Z", None))
        self.label_parent_scale_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"Weight:", None))
        self.lineedit_parent_scale_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"1.000", None))
        self.label_parent_shear_axis.setText(QCoreApplication.translate("atlas_matrix_parent", u"Shear:", None))
        self.checkbox_parent_shear_all.setText(QCoreApplication.translate("atlas_matrix_parent", u"All", None))
        self.checkbox_parent_shear_x.setText(QCoreApplication.translate("atlas_matrix_parent", u"X", None))
        self.checkbox_parent_shear_y.setText(QCoreApplication.translate("atlas_matrix_parent", u"Y", None))
        self.checkbox_parent_shear_z.setText(QCoreApplication.translate("atlas_matrix_parent", u"Z", None))
        self.label_parent_shear_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"Weight:", None))
        self.lineedit_parent_scale_shear_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"1.000", None))
        self.group_parent_global_weight.setTitle(QCoreApplication.translate("atlas_matrix_parent", u"Global weight", None))
        self.lineedit_parent_global_weight.setText(QCoreApplication.translate("atlas_matrix_parent", u"1.000", None))
        self.button_parent_add.setText(QCoreApplication.translate("atlas_matrix_parent", u"Add", None))
        self.button_parent_apply.setText(QCoreApplication.translate("atlas_matrix_parent", u"Apply", None))
        self.button_parent_close.setText(QCoreApplication.translate("atlas_matrix_parent", u"Close", None))
    # retranslateUi
