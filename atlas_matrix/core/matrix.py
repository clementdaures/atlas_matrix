# -*- coding: utf-8 -*-
""" DEP class to use matrix inside Maya

This module provides the `Matrix` class, which allows precise control
over object transformations using matrix nodes in Maya. It can create
and manage nodes such as multMatrix, decomposeMatrix, composeMatrix,
holdMatrix, and blendMatrix, enabling matrix-based parent and aim
constraints without relying on standard Maya constraint nodes.

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
from contextlib import contextmanager

import maya.cmds as cmds
from atlas_matrix.core.utils import nodes
from atlas_matrix.core.utils import attributes
from atlas_matrix.core.utils import verification


# ---------- MAIN CLASS ----------


class Matrix:
    """
    Class to create matrix utilities to matrix-based constraint in Maya.

    This constraint system uses multMatrix, decomposeMatrix, and optionally
    pickMatrix, holdMatrix, and blendMatrix nodes for precise control over
    transformations.
    """
    def __init__(self, driven: Optional[str] = None, drivers: Optional[List[str]] = None) -> None:
        """Initialize the Matrix constraint builder.

        Args:
            driven (Optional[str]): The name of the driven object.
            drivers (Optional[List[str]]): A list of driver object names.

        Raises:
            ValueError: If neither `driven` nor `drivers` are provided.
        """
        user_sel = cmds.ls(selection=True) or []
        self.driven = driven or (user_sel[-1] if user_sel else None)
        self.drivers = drivers or (user_sel[:-1] if user_sel else [])
        self.constraint_type = ""
        if not self.driven or not self.drivers:
            raise ValueError("Provide driven and at least one driver.")


    @contextmanager
    def undo_chunk(self, name="Operation"):
        """Context manager for wrapping operations in a single undo chunk"""
        chunk_name = f"{self.constraint_type}_{name}_{self.driven}"
        cmds.undoInfo(openChunk=True, chunkName=chunk_name)
        try:
            yield
        except Exception as e:
            cmds.undoInfo(cancelChunk=True)
            raise e
        finally:
            cmds.undoInfo(closeChunk=True)


    @property
    def constraining_name(self) -> str:
        """Get the type name used for constraint node naming.

        Returns:
            str: The constraint type identifier (e.g., "pconstrainedby" or "aconstrainedby").
        """
        return {
            "parent": "pconstrainedby",
            "aim": "aconstrainedby"
        }.get(self.constraint_type, "")


    @staticmethod
    def _attribute_validation(attribute_list: List[str]) -> None:
        """Validate that all submitted strings are valid Maya attributes.

        Args:
            attribute_list (List[str]): A list of attribute strings to validate.

        Raises:
            ValueError: If one or more attributes are invalid.
        """
        invalid = [attr for attr in attribute_list if not verification.is_attribute(attr)]
        if invalid:
            raise ValueError(f"Invalid attributes detected: {invalid}")


    def _attribute_have_same_datatype(self, attribute_a: str, attribute_b: str) -> bool:
        """
        Compare whether two attributes share the same data type (shape + element type).

        Args:
            attribute_a (str): The first attribute path in the form "nodeA.attr".
            attribute_b (str): The second attribute path in the form "nodeB.attr".

        Returns:
            bool: True if both attributes have identical type signatures (including
                arrays and compound structures), otherwise False.
        """
        attributes = [attribute_a, attribute_b]
        self._attribute_validation(attributes)

        datatype_a = cmds.getAttr(attribute_a, type=True)
        datatype_b = cmds.getAttr(attribute_b, type=True)

        return datatype_a == datatype_b


    @staticmethod
    def _index_validation(matrix_node: str, index: Optional[int] = None) -> None:
        """Validate that an index is provided for a matrix node connection.

        Args:
            matrix_node (str): The name of the matrix node.
            index (Optional[int]): The index value to validate.

        Raises:
            ValueError: If `index` is None.
        """
        if index is None:
            raise ValueError(f"Index required for node {matrix_node}")


    @staticmethod
    def _driver_name(driver: Union[str, List[str]]) -> str:
        """Get a formatted driver name for node naming.

        Args:
            driver (str | list[str]): The driver name or list of name parts.

        Returns:
            str: A single driver name string.
        """
        return driver if isinstance(driver, str) else "_".join(driver)


    def _create_matrix_node(self, node_type: str, driver: str) -> str:
        """Create a Maya matrix-related node for the given driver.

        Args:
            node_type (str): The Maya node type to create (e.g., "multMatrix").
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created matrix node.
        """
        node_name = f"{node_type.lower()}_{self.driven}_{self.constraining_name}_{self._driver_name(driver)}"
        node = cmds.createNode(node_type, name=node_name)
        return node


    def mult_matrix(self, driver: str) -> str:
        """Create a multMatrix node for the given driver.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created multMatrix node.
        """
        return self._create_matrix_node("multMatrix", driver)


    def hold_matrix(self, driver: str) -> str:
        """Create a holdMatrix node for the given driver.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created holdMatrix node.
        """
        return self._create_matrix_node("holdMatrix", driver)


    def blend_matrix(self) -> str:
        """Create a blendMatrix node for the given driver.

        Returns:
            str: The name of the created blendMatrix node.
        """
        name = f"blendMatrix_{self.driven}_space_shifter"
        return cmds.createNode("blendMatrix", name=name)


    def decompose_matrix(self, driver: str) -> str:
        """Create a decomposeMatrix node for the given driver.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created decomposeMatrix node.
        """
        return self._create_matrix_node("decomposeMatrix", driver)


    def compose_matrix(self, driver: str) -> str:
        """Create a composeMatrix node for the given driver.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created composeMatrix node.
        """
        return self._create_matrix_node("composeMatrix", driver)


    def identity_matrix(self) -> str:
        """Create a identityMatrix node for the given driver.

        Returns:
            str: The name of the created identityMatrix node.
        """
        node_name = f"composematrix_{self.driven}_identity_parent"
        node = cmds.createNode("composeMatrix", name=node_name)
        return node


    @staticmethod
    def get_out_matrix(matrix_node: str) -> str:
        """Get the output matrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full output attribute path (e.g., "multMatrix1.matrixSum").

        Raises:
            ValueError: If the provided node is not a valid matrix node.
        """
        # Get the node type
        node_type = nodes.get_node_type(matrix_node)

        # Check if it's a matrix-related node (lowercase the type for comparison)
        if "matrix" in node_type.lower():

            if verification.is_inversematrix(matrix_node) or verification.is_holdmatrix(matrix_node):
                return f"{matrix_node}.outMatrix"

            elif verification.is_multmatrix(matrix_node) or verification.is_addmatrix(
                    matrix_node) or verification.is_wtaddmatrix(matrix_node):
                return f"{matrix_node}.matrixSum"

            else:
                return f"{matrix_node}.outputMatrix"

        else:
            raise ValueError(f"Invalid matrix node: {matrix_node}")

    @staticmethod
    def get_in_matrix(matrix_node: str) -> str:
        """Get the input matrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full input attribute path (e.g., "decomposeMatrix1.inputMatrix").

        Raises:
            ValueError: If the node is invalid.
        """
        # Get the node type (don't lowercase the node name!)
        node_type = nodes.get_node_type(matrix_node)

        # Check if it's a matrix-related node (lowercase the type for comparison)
        if "matrix" in node_type.lower():

            if verification.is_holdmatrix(matrix_node):
                return f"{matrix_node}.inMatrix"

            else:
                return f"{matrix_node}.inputMatrix"

        else:
            raise ValueError(f"Invalid matrix node: {matrix_node}")


    @staticmethod
    def get_matrix(matrix_node: str) -> str:
        """
        Get the matrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full matrix attribute path (e.g., "cube1.matrix").

        Raises:
            ValueError: If the matrix attribute is missing.
        """
        if not cmds.attributeQuery('matrix', node=matrix_node, exists=True):
            raise ValueError(f"Submitted node {matrix_node} does not contain a matrix attribute")

        return f"{matrix_node}.matrix"


    @staticmethod
    def get_world_matrix(matrix_node: str) -> str:
        """
        Get the worldMatrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full worldMatrix attribute path (e.g., "cube1.worldMatrix[0]").

        Raises:
            ValueError: If the worldMatrix attribute is missing.
        """
        if not cmds.attributeQuery('worldMatrix', node=matrix_node, exists=True):
            raise ValueError(f"Submitted node {matrix_node} does not contain a worldMatrix attribute")

        return f"{matrix_node}.worldMatrix[0]"


    @staticmethod
    def get_inverse_world_matrix(matrix_node: str) -> str:
        """
        Get the worldInverseMatrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full worldInverseMatrix attribute path (e.g., "cube1.worldMatrix[0]").

        Raises:
            ValueError: If the worldInverseMatrix attribute is missing.
        """
        if not cmds.attributeQuery('worldInverseMatrix', node=matrix_node, exists=True):
            raise ValueError(f"Submitted node {matrix_node} does not contain a worldInverseMatrix attribute")

        return f"{matrix_node}.worldInverseMatrix[0]"


    @staticmethod
    def get_offset_parent_matrix(matrix_node: str) -> str:
        """
        Get the offsetParentMatrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full offsetParentMatrix attribute path (e.g., "cube1.offsetParentMatrix").

        Raises:
            ValueError: If the offsetParentMatrix attribute is missing.
        """
        if not cmds.attributeQuery('offsetParentMatrix', node=matrix_node, exists=True):
            raise ValueError(f"Submitted node {matrix_node} does not contain a offsetParentMatrix attribute")

        return f"{matrix_node}.offsetParentMatrix"


    def get_offset_parent_matrix_source(self):
        """
        Get the source plug connected to the node's offsetParentMatrix attribute.

        Args:
            self.driven (str): The name of the driven object to check.

        Returns:
            str or None: The full plug name of the source connection
                         (e.g. "node01.worldMatrix[0]"), or None if no connection exists.
        """

        connections = cmds.listConnections(
            f"{self.driven}.offsetParentMatrix",
            source=True,
            destination=False,
            plugs=True
        )

        return connections[0] if connections else None


    def connect_matrix(self, source: str, target: str) -> None:
        """Connect one matrix attribute to another.

        Args:
            source (str): The source attribute (e.g., "multMatrix.matrixSum").
            target (str): The target attribute (e.g., "object.offsetParentMatrix").

        Raises:
            ValueError: If either attribute is invalid.
        """
        self._attribute_validation([source, target])

        cmds.connectAttr(source, target)


    def disconnect_matrix(self, source: str, target: str) -> None:
        """Disconnect one matrix attribute from another.

        Args:
            source (str): The source attribute (e.g., "multMatrix.matrixSum").
            target (str): The target attribute (e.g., "object.offsetParentMatrix").

        Raises:
            ValueError: If either attribute is invalid.
        """
        self._attribute_validation([source, target])

        cmds.disconnectAttr(source, target)


    def con_hold_matrix(self, driver: str) -> Tuple[str, str, str]:
        """
        Create a hold matrix node to maintain offset between objects.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: Hold matrix name.
        """
        node_hold = self.hold_matrix(driver)

        in_hold = self.get_in_matrix(node_hold)
        out_hold = self.get_out_matrix(node_hold)

        return node_hold, in_hold, out_hold


    def con_mult_matrix(self, driver: str) -> Tuple[str, Callable[[int], str], str]:
        """
        Create a mult matrix node to constrain object.

        Args:
            driver (str): The name of the driver node.

        Returns:
            Tuple[str, Callable[[int], str], str]: mult matrix name.
        """
        node_mult = self.mult_matrix(driver)

        def in_mult(i: int) -> str:
            return f"{node_mult}.matrixIn[{i}]"

        out_mult = self.get_out_matrix(node_mult)

        return node_mult, in_mult, out_mult


    def con_blend_matrix(self) -> Tuple[str, str, Callable[[int], str], str, Callable[[int], str]]:
        """
        Create a blend matrix node to blend constrained objects.

        Returns:
            Tuple[str, str, Callable[[int], str], str]: blend matrix name.
        """
        node_blend = self.blend_matrix()
        input_blend = f"{node_blend}.inputMatrix"
        def in_blend(i: int) -> str:
            return f"{node_blend}.target[{i}].targetMatrix"
        out_blend = self.get_out_matrix(node_blend)
        def in_weight(i: int) -> str:
            return f"{node_blend}.target[{i}].weight"

        return node_blend, input_blend, in_blend, out_blend, in_weight


    def con_compose_matrix(self, driver: str) -> Tuple[str, Callable[[str], str], Callable[[str], str], Callable[[str], str], Callable[[str], str], str]:
        """
        Create a compose matrix node to compose constrained objects.

        Args:
            driver (str): The name of the driver node.
        """
        node_compose = self.compose_matrix(driver)

        def in_translate(axis: str) -> str:
            return f"{node_compose}.inputTranslate{axis.upper()}"
        def in_rotate(axis: str) -> str:
            return f"{node_compose}.inputRotate{axis.upper()}"
        def in_scale(axis: str) -> str:
            return f"{node_compose}.inputScale{axis.upper()}"
        def in_shear(axis: str) -> str:
            return f"{node_compose}.inputShear{axis.upper()}"

        out_compose = self.get_out_matrix(node_compose)

        return node_compose, in_translate, in_rotate, in_scale, in_shear, out_compose


    def con_decompose_matrix(self, driver: str) -> Tuple[str, str, Callable[[str], str], Callable[[str], str], Callable[[str], str], Callable[[str], str]]:
        """
        Create a decompose matrix node to decompose constrained objects.

        Args:
            driver (str): The name of the driver node.
        """
        node_decompose = self.decompose_matrix(driver)

        in_decompose = self.get_in_matrix(node_decompose)

        def out_translate(axis: str) -> str:
            return f"{node_decompose}.outputTranslate{axis.upper()}"
        def out_rotate(axis: str) -> str:
            return f"{node_decompose}.outputRotate{axis.upper()}"
        def out_scale(axis: str) -> str:
            return f"{node_decompose}.outputScale{axis.upper()}"
        def out_shear(axis: str) -> str:
            return f"{node_decompose}.outputShear{axis.upper()}"

        return node_decompose, in_decompose, out_translate, out_rotate, out_scale, out_shear


    def get_set_attr(self, get_attribute: str, set_attribute: str) -> None:
        """
        Get the value of a given attribute and set it to the given set_attribute

        Args:
            get_attribute(str): the attribute to get the value from
            set_attribute(str): the attribute to set the value to
        """
        value_type = cmds.getAttr(get_attribute, type=True)

        if value_type == "matrix":
            values = cmds.getAttr(get_attribute)
            cmds.setAttr(set_attribute, *values, type="matrix")
        else:
            value = cmds.getAttr(get_attribute)
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            if isinstance(value, (tuple, list)):
                cmds.setAttr(set_attribute, *value)
            else:
                cmds.setAttr(set_attribute, value)


    def get_parent_driven(self):
        """
        Get the parent of the driven node

        Returns:
            str: parent of the self.driven node
        """
        return cmds.listRelatives(self.driven, parent=True)


    def connect_attr(self, source_attribute: str, target_attribute: str) -> str:
        """
        Connect a source attribute to a target attribute

        Args:
            source_attribute(str): the attribute with the source connection
            target_attribute(str): the attribute with the target connection

        """
        if not cmds.objExists(source_attribute):
            raise ValueError(f"Source attribute does not exist: {source_attribute}")
        if not cmds.objExists(target_attribute):
            raise ValueError(f"Target attribute does not exist: {target_attribute}")

        try:
            cmds.connectAttr(source_attribute, target_attribute, force=True)
        except Exception as e:
            raise RuntimeError(f"Failed to connect {source_attribute} -> {target_attribute}: {e}")


    def preserve_initial_transform(self):
        """
        Preserve initial transform attribute values and reconnect existing inputs.

        Creates a compound attribute 'initialTransform' on the driven object with children for
        translate, rotate, scale, and shear. Any existing incoming connections to
        these attributes are automatically redirected to the new initial attributes.
        """
        if not cmds.attributeQuery('initialTransform', node=self.driven, exists=True):
            cmds.addAttr(self.driven, ln='initialTransform', at='compound', nc=12, h=True)

            for axis in ['X', 'Y', 'Z']:
                if not cmds.attributeQuery(f'initialTranslate{axis}', node=self.driven, exists=True):
                    cmds.addAttr(self.driven, ln=f'initialTranslate{axis}', at='doubleLinear', p='initialTransform',
                                 k=True, h=True)

            for axis in ['X', 'Y', 'Z']:
                if not cmds.attributeQuery(f'initialRotate{axis}', node=self.driven, exists=True):
                    cmds.addAttr(self.driven, ln=f'initialRotate{axis}', at='doubleAngle', p='initialTransform', k=True, h=True)

            for axis in ['X', 'Y', 'Z']:
                if not cmds.attributeQuery(f'initialScale{axis}', node=self.driven, exists=True):
                    cmds.addAttr(self.driven, ln=f'initialScale{axis}', at='double', dv=1.0, p='initialTransform',
                                 k=True, h=True)

            for axis in ['XY', 'XZ', 'YZ']:  # correct shear names
                if not cmds.attributeQuery(f'initialShear{axis}', node=self.driven, exists=True):
                    cmds.addAttr(self.driven, ln=f'initialShear{axis}', at='double', dv=0.0, p='initialTransform',
                                 k=True, h=True)

        for axis in ['X', 'Y', 'Z']:
            v = cmds.getAttr(f"{self.driven}.translate{axis}")
            cmds.setAttr(f"{self.driven}.initialTranslate{axis}", v)

        for axis in ['X', 'Y', 'Z']:
            v = cmds.getAttr(f"{self.driven}.rotate{axis}")
            cmds.setAttr(f"{self.driven}.initialRotate{axis}", v)

        for axis in ['X', 'Y', 'Z']:
            v = cmds.getAttr(f"{self.driven}.scale{axis}")
            cmds.setAttr(f"{self.driven}.initialScale{axis}", v)

            # shear uses XY/XZ/YZ
        for axis in ['XY', 'XZ', 'YZ']:
            v = cmds.getAttr(f"{self.driven}.shear{axis}")
            cmds.setAttr(f"{self.driven}.initialShear{axis}", v)


    def preserve_initial_matrix(self):
        """
        Preserve original offsetParentMatrix value and reconnect existing input.

        Creates a matrix attribute 'initial_matrix' on the driven object. Any existing
        incoming connection to offsetParentMatrix is automatically redirected to
        the new initial_matrix attribute.
        """
        if not cmds.attributeQuery('initialMatrix', node=self.driven, exists=True):
            cmds.addAttr(self.driven, ln='initialMatrix', at='matrix', k=False, h=True)

        opm_attr = f"{self.driven}.offsetParentMatrix"
        init_attr = f"{self.driven}.initialMatrix"

        vals = cmds.getAttr(opm_attr)
        # normalize: [(16 floats)] -> (16 floats)
        if isinstance(vals, (list, tuple)) and len(vals) == 1 and isinstance(vals[0], (list, tuple)):
            vals = vals[0]
        cmds.setAttr(init_attr, *vals, type='matrix')