# -*- coding: utf-8 -*-
""" Utilities functions that facilitates node manipulation inside Maya

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

import maya.cmds as cmds
import maya.api.OpenMaya as om


# ---------- FUNCTIONS ----------


def get_node_type(name:str)-> str:
    """Return the type of Maya node given its name.

    This function uses the OpenMaya API to query the dependency node
    corresponding to the provided name and retrieves its type.

    Args:
        name (str): The name of the Maya node.

    Returns:
        str: The type of the node (e.g., "transform", "joint", "multMatrix").

    Raises:
        RuntimeError: If the node does not exist in the scene.
    """
    selection_list = om.MSelectionList()
    selection_list.add(name)
    node_obj = selection_list.getDependNode(0)

    dependency_node = om.MFnDependencyNode(node_obj)

    node_type = dependency_node.typeName
    return node_type