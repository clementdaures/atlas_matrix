# -*- coding: utf-8 -*-
""" DEP class to remove matrix constraints inside Maya

This module provides the `RemoveCon` class, which removes matrix-based constraints
created by ParentCon and restores original transformations. It inherits from the
Matrix class.

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


from typing import Optional, List
import maya.cmds as cmds
from atlas_matrix.core.matrix import Matrix
from atlas_matrix.core.utils import transform


# ---------- MAIN CLASS ----------


class RemoveCon(Matrix):
    """Class to remove matrix-based constraints in Maya created by ParentCon."""

    def __init__(
            self,
            driven: Optional[str] = None,
            constraint_type: Optional[str] = None
    ):
        """Initialize the RemoveCon constraint removal.

        Args:
            driven (Optional[str]): The name of the driven object.
                If None, uses the current Maya selection.
            constraint_type (Optional[str]): Type of constraint ("parent" or "aim").
                If None, will attempt to detect automatically.
        """
        user_sel = cmds.ls(selection=True) or []
        self.driven = driven or (user_sel[0] if user_sel else None)

        if not self.driven:
            raise ValueError("Provide a driven object or select one.")

        self.drivers = []
        self.constraint_type = constraint_type or self._detect_constraint_type()

        if not self.constraint_type:
            raise ValueError(
                f"Could not detect constraint type on '{self.driven}'. "
                "Please specify 'parent' or 'aim'."
            )


    # ---------- PROPERTIES ----------


    @property
    def constraining_name(self) -> str:
        """Naming token used by ParentCon / AimCon when creating nodes.

        Returns:
            str: e.g. "pconstrainedby" for parent, "aconstrainedby" for aim.
        """
        return {
            "parent": "pconstrainedby",
            "aim":    "aconstrainedby",
        }.get(self.constraint_type, "")


    # ---------- DETECTION ----------


    def _detect_constraint_type(self) -> Optional[str]:
        """Detect the type of constraint applied to the driven object.

        Checks offsetParentMatrix connections, upstream history node names,
        then W0/W1... weight attributes as a final fallback.

        Returns:
            Optional[str]: "parent" or "aim" if detected, None otherwise.
        """
        opm_attr = f"{self.driven}.offsetParentMatrix"

        if cmds.attributeQuery("offsetParentMatrix", node=self.driven, exists=True):
            for node in cmds.listConnections(opm_attr, source=True, destination=False, plugs=False) or []:
                if "pconstrainedby" in node:
                    return "parent"
                if "aconstrainedby" in node:
                    return "aim"
                if cmds.nodeType(node) == "blendMatrix" and self.driven in node:
                    return "parent"

        for node in cmds.listHistory(self.driven, pruneDagObjects=True) or []:
            if "pconstrainedby" in node:
                return "parent"
            if "aconstrainedby" in node:
                return "aim"

        user_attrs = cmds.listAttr(self.driven, userDefined=True) or []
        if any(attr.startswith("W") and attr[1:].isdigit() for attr in user_attrs):
            return "parent"

        return None


    # ---------- NODE COLLECTION ----------


    def _is_constraint_node(self, node: str) -> bool:
        """Return True if the node was created by a constraint.

        Args:
            node (str): The node name to check.

        Returns:
            bool: True if the node belongs to the constraint graph.
        """
        matrix_types = {"multMatrix", "blendMatrix", "decomposeMatrix",
                        "composeMatrix", "holdMatrix", "fourByFourMatrix"}
        if self.constraining_name and self.constraining_name in node:
            return True
        if self.driven in node:
            return cmds.nodeType(node) in matrix_types
        return False


    def _get_constraint_nodes(self) -> List[str]:
        """Collect every node belonging to the constraint graph.

        Crawls upstream from offsetParentMatrix and full history,
        matching nodes by naming token or driven name + matrix type.

        Returns:
            List[str]: Deduplicated list of constraint node names.
        """
        found = set()
        queue = []

        opm_attr = f"{self.driven}.offsetParentMatrix"
        if cmds.attributeQuery("offsetParentMatrix", node=self.driven, exists=True):
            queue += cmds.listConnections(opm_attr, source=True, destination=False, plugs=False) or []

        queue += cmds.listHistory(self.driven, pruneDagObjects=True) or []

        while queue:
            node = queue.pop()
            if node in found or not cmds.objExists(node):
                continue
            if not self._is_constraint_node(node):
                continue
            found.add(node)
            queue += cmds.listConnections(node, source=True, destination=False, plugs=False) or []

        return list(found)


    # ---------- RESTORATION ----------


    def _get_blend_node(self) -> Optional[str]:
        """Return the blendMatrix node created by ParentCon, if it exists.

        ParentCon always names it ``blendMatrix_{driven}_space_shifter``.

        Returns:
            Optional[str]: Node name, or None if no blendMatrix was created.
        """
        candidate = f"blendMatrix_{self.driven}_space_shifter"
        return candidate if cmds.objExists(candidate) else None


    def _restore_offset_parent_matrix(self) -> None:
        """Restore offsetParentMatrix to its pre-constraint state.

        With blendMatrix, reads ``blendMatrix.inputMatrix`` (the base slot where
        ParentCon stored the previous offsetParentMatrix state).
        Without blendMatrix, reads ``initialMatrix`` stored by preserve_initial_matrix().
        In both cases: reconnects the source plug if one existed, or get/sets the value.
        Must be called before any node deletion.
        """
        opm_attr = f"{self.driven}.offsetParentMatrix"
        blend_node = self._get_blend_node()

        if blend_node:
            source_attr = f"{blend_node}.inputMatrix"
        elif cmds.attributeQuery("initialMatrix", node=self.driven, exists=True):
            source_attr = f"{self.driven}.initialMatrix"
        else:
            return

        src_plugs = cmds.listConnections(source_attr, source=True, destination=False, plugs=True) or []

        if src_plugs:
            try:
                cmds.connectAttr(src_plugs[0], opm_attr, force=True)
            except Exception as exc:
                cmds.warning(f"Could not reconnect {src_plugs[0]} -> {opm_attr}: {exc}")
        else:
            try:
                self.get_set_attr(source_attr, opm_attr)
            except Exception as exc:
                cmds.warning(f"Could not restore {opm_attr} from {source_attr}: {exc}")


    def _disconnect_offset_parent_matrix(self) -> None:
        """Sever constraint-graph connections on offsetParentMatrix.

        Leaves any pre-existing connection restored by _restore_offset_parent_matrix untouched.
        """
        if not cmds.attributeQuery("offsetParentMatrix", node=self.driven, exists=True):
            return

        opm_attr = f"{self.driven}.offsetParentMatrix"
        constraint_nodes = set(self._get_constraint_nodes())

        for src in cmds.listConnections(opm_attr, source=True, destination=False, plugs=True) or []:
            if src.split(".")[0] in constraint_nodes:
                try:
                    cmds.disconnectAttr(src, opm_attr)
                except Exception as exc:
                    cmds.warning(f"Could not disconnect {src} -> {opm_attr}: {exc}")


    def _remove_weight_attributes(self) -> None:
        """Delete W0/W1... weight attributes and initialMatrix from the driven object."""
        for attr in cmds.listAttr(self.driven, userDefined=True) or []:
            if (attr.startswith("W") and attr[1:].isdigit()) or attr == "initialMatrix":
                full_attr = f"{self.driven}.{attr}"
                try:
                    if cmds.objExists(full_attr):
                        cmds.deleteAttr(full_attr)
                except Exception as exc:
                    cmds.warning(f"Could not delete attribute {full_attr}: {exc}")


    # ---------- PUBLIC API ----------


    def remove(self) -> None:
        """Remove the ParentCon constraint and restore the driven object."""
        with self.undo_chunk(name="remove"):
            constraint_nodes = self._get_constraint_nodes()

            if not constraint_nodes:
                cmds.warning(
                    f"No constraint nodes found for '{self.driven}' "
                    f"(type: '{self.constraint_type}'). Nothing to remove."
                )
                return

            self._restore_offset_parent_matrix()
            self._disconnect_offset_parent_matrix()

            for node in constraint_nodes:
                try:
                    if cmds.objExists(node):
                        cmds.delete(node)
                except Exception as exc:
                    cmds.warning(f"Could not delete node '{node}': {exc}")

            self._remove_weight_attributes()
            transform.idtransform(self.driven)

            print(f"Successfully removed '{self.constraint_type}' constraint from '{self.driven}'.")


# ---------- CONVENIENCE FUNCTION ----------


def remove_constraint(
        driven: Optional[str] = None,
        constraint_type: Optional[str] = None
) -> None:
    """Convenience function to remove a ParentCon matrix constraint.

    Args:
        driven (Optional[str]): The driven object name. Uses selection if None.
        constraint_type (Optional[str]): "parent" or "aim". Auto-detected when None.

    Examples:
        remove_constraint("pCube1", "parent")
        remove_constraint()
    """
    remover = RemoveCon(driven=driven, constraint_type=constraint_type)
    remover.remove()