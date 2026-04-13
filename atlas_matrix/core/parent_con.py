# -*- coding: utf-8 -*-
""" DEP class to use constraint parent matrix inside Maya

This module provides the `ParentCon` class, which allows precise matrix-based constraint
over objects using matrix nodes in Maya. It inherits from Matrix class.

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


from typing import Optional, List, Union, Tuple, Callable
from dataclasses import dataclass

import maya.cmds as cmds

from atlas_matrix.core.matrix import Matrix
from atlas_matrix.core.utils import transform


# ---------- DATA CLASS ----------


@dataclass
class AxisFilter:
    x: bool = True
    y: bool = True
    z: bool = True


@dataclass
class AxisWeights:
    translate: float = 1.0
    rotate: float = 1.0
    scale: float = 1.0
    shear: float = 1.0
    all: float = 1.0


# ---------- MAIN CLASS ----------


class ParentCon(Matrix):
    """
    Class to create a matrix-based parent constraint in Maya.

    This constraint system uses multMatrix, decomposeMatrix, and optionally
    pickMatrix, holdMatrix, and blendMatrix nodes for precise control over
    transformations.
    """
    def __init__(
            self,
            driven: Optional[str] = None,
            drivers: Optional[List[str]] = None,
            *,
            offset: bool = False,
            keep_hold: bool = False,
            envelope: bool = False,
            translate_filter: AxisFilter = AxisFilter(),
            rotate_filter: AxisFilter = AxisFilter(),
            scale_filter: AxisFilter = AxisFilter(),
            shear_filter: AxisFilter = AxisFilter(),
            weights: AxisWeights = AxisWeights()
    ):
        """
        Initialize the ParentCon constraint setup.

        Args:
            driven (Optional[str]): The name of the driven object.
            drivers (Optional[List[str]]): A list of driver object names.
        """
        super().__init__(driven, drivers)
        self.constraint_type="parent"
        self.offset = offset
        self.keep_hold = keep_hold
        self.envelope = envelope

        self.translate_filter = translate_filter or AxisFilter()
        self.rotate_filter = rotate_filter or AxisFilter()
        self.scale_filter = scale_filter or AxisFilter()
        self.shear_filter = shear_filter or AxisFilter()
        self.weights = weights or AxisWeights()


    def _all_translate(self):
        """
        Indicate if all translate are checked or not
        """
        return self.translate_filter.x and self.translate_filter.y and self.translate_filter.z


    def _all_rotate(self):
        """
        Indicate if all rotate are checked or not
        """
        return self.rotate_filter.x and self.rotate_filter.y and self.rotate_filter.z


    def _all_scale(self):
        """
        Indicate if all scale are checked or not
        """
        return self.scale_filter.x and self.scale_filter.y and self.scale_filter.z


    def _all_shear(self):
        """
        Indicate if all shear are checked or not
        """
        return self.shear_filter.x and self.shear_filter.y and self.shear_filter.z


    def _mount_offset(self, driver: str):
        """
        Mount the necessary setup for the offset system

        Args:
            driver (str): The name of the driver object
        """
        # Create temporary mult to get the value of the offset
        mult_tmp_node, mult_tmp_in, mult_tmp_out = self.con_mult_matrix(f"tmp_{driver}")

        self.connect_attr(self.get_world_matrix(self.driven), mult_tmp_in(0))
        self.connect_attr(self.get_inverse_world_matrix(driver), mult_tmp_in(1))

        return mult_tmp_node, mult_tmp_in, mult_tmp_out


    def create_offset(self, driver: str, mult_in: Callable[[int], str]):
        """
        Create the wanted offset type

        Args:
            driver(str): The name of the driver object name
            mult_in(str): The in attribute of the multMatrix with great index.
        """
        if self.offset:
            mult_tmp_node, mult_tmp_in, mult_tmp_out = self._mount_offset(driver)
            if self.keep_hold:
                hold_node, hold_in, hold_out = self.con_hold_matrix(driver)
                self.get_set_attr(mult_tmp_out, hold_in)
                self.connect_attr(hold_out, mult_in(0))
            else:
                self.get_set_attr(mult_tmp_out, mult_in(0))
            cmds.delete(mult_tmp_node)
        else:
            pass


    def create_attr(self, index: int, blend_weight: Callable[[int], str]) -> str:
        """
        Create the attribute on self.driven

        Args:
            index (int) : The index value
            blend_weight(str): The input of the blend

        Returns:
            str : Created attribute
        """
        attr_name = f"W{index}"
        created_attr = f"{self.driven}.{attr_name}"
        cmds.addAttr(
            self.driven,
            longName=attr_name,
            shortName=attr_name,
            attributeType="float",
            multi=False,
            minValue=0.0,
            maxValue=1.0,
            defaultValue=1.0,
            keyable=True
        )

        self.connect_attr(created_attr, blend_weight(index))

        return created_attr


    def create_axis_filter(self, driver: str):
        """
        Create a composeMatrix if needed

        Args:
            driver (str): The name of the driver node.
        """
        decompose_node, decompose_in, decompose_out_translate, decompose_out_rotate, decompose_out_scale, decompose_out_shear = self.con_decompose_matrix(driver)
        compose_node, compose_in_translate, compose_in_rotate, compose_in_scale, compose_in_shear, compose_out = self.con_compose_matrix(driver)

        for axis, enabled in zip("xyz", [self.translate_filter.x, self.translate_filter.y, self.translate_filter.z]):
            if enabled:
                self.connect_attr(decompose_out_translate(axis), compose_in_translate(axis))

        for axis, enabled in zip("xyz", [self.rotate_filter.x, self.rotate_filter.y, self.rotate_filter.z]):
            if enabled:
                self.connect_attr(decompose_out_rotate(axis), compose_in_rotate(axis))

        for axis, enabled in zip("xyz", [self.scale_filter.x, self.scale_filter.y, self.scale_filter.z]):
            if enabled:
                self.connect_attr(decompose_out_scale(axis), compose_in_scale(axis))

        for axis, enabled in zip("xyz", [self.shear_filter.x, self.shear_filter.y, self.shear_filter.z]):
            if enabled:
                self.connect_attr(decompose_out_shear(axis), compose_in_shear(axis))

        return decompose_in, compose_out

    def mount_system(self):
        """
        Internal setup to create the constraint chain and connect it.
        """
        with self.undo_chunk(name="create"):
            parent_result = self.get_parent_driven()

            # Handle case where object has no parent (is at world root)
            if parent_result and len(parent_result) > 0:
                parent_node = parent_result[0]
                parent_inverse = self.get_inverse_world_matrix(parent_node)
            else:
                # No parent found, use identity matrix
                identity_node = self.identity_matrix()
                parent_inverse = self.get_out_matrix(identity_node)

            all_translate = self._all_translate()
            all_rotate = self._all_rotate()
            all_scale = self._all_scale()
            all_shear = self._all_shear()

            mult_outs = []

            # Setup of the mult system
            for index, driver in enumerate(self.drivers):
                mult_node, mult_in, mult_out = self.con_mult_matrix(driver)

                if all_translate and all_rotate and all_scale and all_shear:
                    self.connect_attr(self.get_world_matrix(driver), mult_in(1))
                else:
                    # Generate axis filter
                    decompose_in, compose_out = self.create_axis_filter(driver)
                    self.connect_attr(self.get_world_matrix(driver), decompose_in)
                    self.connect_attr(compose_out, mult_in(1))

                self.connect_attr(parent_inverse, mult_in(2))

                # Generate offset
                self.create_offset(driver, mult_in)

                mult_outs.append(mult_out)

            # Setup of the blend system
            if len(self.drivers) > 1 or self.envelope:
                blend_node, blend_input, blend_in, blend_out, blend_in_weight = self.con_blend_matrix()
                if self.envelope:
                    input_connection = self.get_offset_parent_matrix_source()

                    if input_connection:
                        self.connect_attr(input_connection, blend_input)
                    else:
                        self.get_set_attr(self.get_matrix(self.driven), blend_input)

                for index, mult_out in enumerate(mult_outs):
                    self.connect_attr(mult_outs[index], blend_in(index))
                    created_attr = self.create_attr(index, blend_in_weight)
                    if index > 0:
                        cmds.setAttr(created_attr, self.weights.all)
                self.connect_attr(blend_out, self.get_offset_parent_matrix(self.driven))
            # End connection if no blend created
            else:
                self.connect_attr(mult_outs[0], self.get_offset_parent_matrix(self.driven))

            transform.idtransform(self.driven)