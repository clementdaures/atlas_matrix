""" Utilities functions that facilitates attributes manipulation inside Maya

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

from atlas_matrix.core.utils import verification


# ---------- FUNCTIONS ----------


def get_world_matrix(obj: str)-> str:
    return f"{obj}.worldMatrix[0]"


def get_world_inverse_matrix(obj: str)-> str:
    return f"{obj}.worldInverseMatrix[0]"


def get_offset_parent_matrix(obj: str)-> str:
    return f"{obj}.offsetParentMatrix"