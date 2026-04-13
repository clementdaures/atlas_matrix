# -*- coding: utf-8 -*-
""" Utilities functions that facilitates transform manipulation inside Maya

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

from atlas_matrix.core.utils import verification


# ---------- FUNCTIONS ----------


def idtransform(obj: str)-> None:
    """Reset the transformations of a Maya object to the identity values.

    This function sets the following attributes to default values:
        - translate: (0, 0, 0)
        - rotate: (0, 0, 0)
        - scale: (1, 1, 1)
    If the object is a joint, it also resets:
        - jointOrient: (0, 0, 0)

    Args:
        obj (str): The name of the Maya object to reset.
    """
    cmds.setAttr(f"{obj}.translate", 0, 0, 0)
    cmds.setAttr(f"{obj}.rotate", 0, 0, 0)
    cmds.setAttr(f"{obj}.scale", 1, 1, 1)

    if verification.is_joint(obj):
        cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)