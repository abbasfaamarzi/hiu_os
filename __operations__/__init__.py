"""
System-level navigation and file operations using the cursor-based interface.
"""

import os
import logging
from typing import Optional, Any

# ============================================================================
# Direct imports from submodules (no reliance on __operations__.__init__)
# ============================================================================
from hiu_os.__operations__.__file__.__base__.__formats__ import Formats, DictAttr
from hiu_os.__operations__.__file__.__base__.__keywords__ import OsKeywords, AppKeywords, SnakePascalName
from hiu_os.__operations__.__tasks__ import ToDo
from hiu_os.__operations__.__dir__ import Dir
from hiu_os.__operations__.__file__.__file__ import File
from hiu_os.__operations__.__file__.__json__ import JsonFile
from hiu_os.__operations__.__file__.__pickle__ import PickleFile
from hiu_os.__operations__.__path__ import Path

# (Optional) Add http_types if not defined
if not hasattr(OsKeywords, 'http_types'):
    OsKeywords.http_types = ["create", "read", "update", "clear", "delete"]

logger = logging.getLogger(__name__)

# ============================================================================
# The rest of your classes (CurserInformation, Curser, ShortCuts, OperationsSystem)
# ============================================================================
