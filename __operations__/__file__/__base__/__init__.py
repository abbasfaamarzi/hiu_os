"""
Base utilities for file operations.

This module exports core helper classes used throughout the file operations
package:
- Formats: file format detection and naming utilities.
- DictAttr: dictionary with attribute-style access.
- OsKeywords: system constants and keyword sets.
- AppKeywords: application configuration constants.
- SnakePascalName: naming convention conversions.
- LifeCycleLog: lifecycle event logging.
- SerializersClear: helper to remove 'path' from data.
- Vars: base class for extracting class attributes.
"""

from .__formats__ import Formats, DictAttr
from .__keywords__ import OsKeywords, AppKeywords, SnakePascalName
from .__log__ import LifeCycleLog
from .__serializers__ import SerializersClear, Vars

__all__ = [
    'Formats',
    'DictAttr',
    'OsKeywords',
    'AppKeywords',
    'SnakePascalName',
    'LifeCycleLog',
    'SerializersClear',
    'Vars',
]