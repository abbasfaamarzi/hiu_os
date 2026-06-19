"""
System-level navigation and file operations using the cursor-based interface.

This module provides:
- Curser: Fluent filesystem navigator with CRUD operations.
- ShortCuts: Predefined paths.
- OperationsSystem: High-level access to application resources.
"""

import os
import logging
from typing import Optional, Any, Dict, List, Union

# ============================================================================
# Absolute imports from the package root
# ============================================================================
from hiu_os.__operations__.__file__.__base__.__formats__ import Formats, DictAttr
from hiu_os.__operations__.__file__.__base__.__keywords__ import OsKeywords, AppKeywords, SnakePascalName
from hiu_os.__operations__.__tasks__ import ToDo
from hiu_os.__operations__.__dir__ import Dir
from hiu_os.__operations__.__file__.__file__ import File
from hiu_os.__operations__.__file__.__json__ import JsonFile
from hiu_os.__operations__.__file__.__pickle__ import PickleFile
from hiu_os.__operations__.__path__ import Path

# Ensure OsKeywords has http_types (if not defined, add it)
if not hasattr(OsKeywords, 'http_types'):
    OsKeywords.http_types = ["create", "read", "update", "clear", "delete"]

logger = logging.getLogger(__name__)


class CurserInformation:
    """
    Holds basic path information extracted from a given base path.
    Used as a base class for `Curser` to avoid duplication of initialization logic.
    """

    def __init__(self, base_path: Optional[str] = None, parent: Optional['Curser'] = None,
                 save_log: bool = False) -> None:
        self.main_dir = Path.main_dir()
        self._path = base_path if base_path is not None else self.main_dir
        self.child_name = None
        self.path_split = Path.split(self._path)
        self.parent = parent if parent else (
            self.path_split[-2] if len(self.path_split) >= 2 else None
        )
        self.head_name = self.path_split[-1] if self.path_split else ""
        self.file_name, self.format_name = Formats.get_format_name(self.head_name)
        self.save_log = save_log


class Curser(CurserInformation):
    """
    A fluent interface for navigating the filesystem and performing operations.

    Usage:
        cursor = Curser()
        cursor.assets.default.settings_json.read()   # reads settings.json
    """

    files = {
        "file": File,
        "json": JsonFile,
        "pkl": PickleFile,
        "dir": Dir,
        "py": File,
        "js": File,
        "css": File,
        "html": File,
        "txt": File,
        "md": File,
        "log": File,
        "path": Path,
    }

    file_operator_message = {
        "json": "JSON file",
        "pkl": "Pickle file",
        "dir": "Directory",
        "file": "File",
        "log": "Log file",
    }

    http_map_pattern = {
        "rename": "update",
        "copy": "create",
        "move": "clear_and_update",
        "truncate": "clear",
        "append": "update",
        "save": "update",
        "list": "read",
        "mkdir": "create",
        "rmdir": "clear",
        "is_dir": "read",
        "chdir": "update",
    }

    # Global flag to control auto-creation (default: True for safety)
    AUTO_CREATE = True

    def __init__(self, base_path: Optional[str] = None, parent: Optional['Curser'] = None,
                 save_log: bool = False) -> None:
        super().__init__(base_path, parent, save_log)
        if not os.path.exists(self._path) and self.AUTO_CREATE:
            self.create(data={})

    @property
    def path_builder(self) -> str:
        if self.format_name == "dir":
            return os.path.join(self._path, self.file_name)
        else:
            base = SnakePascalName.to_snake_case(self.file_name)
            return os.path.join(self._path, f"{base}.{self.format_name}")

    def __getitem__(self, name: str) -> 'Curser':
        return self.__getattr__(name)

    def __getattr__(self, name: str) -> Any:
        # 1. Operation aliases
        if name in self.http_map_pattern:
            return getattr(self, self.http_map_pattern[name])

        # 2. Internal attributes and reserved keywords
        if name in self.__dict__:
            return self.__dict__[name]
        if name in OsKeywords.CURSERKEYWORDS:
            return super().__getattribute__(name)

        # 3. Navigation: parse file name and format
        file_name, format_name = Formats.get_format_name(name)
        if format_name not in self.files:
            format_name = "dir"
            file_name = name

        self.file_name = file_name
        self.format_name = format_name
        self.child_name = name

        new_path = self.path_builder
        new_node = Curser(new_path, parent=self, save_log=self.save_log)

        if not os.path.exists(new_node._path) and self.AUTO_CREATE:
            new_node.create(data={})

        return new_node

    def __call__(self, name: str) -> 'Curser':
        return self.__getattr__(name)

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f"Curser({self._path!r})"

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ('_path', 'parent', 'child_name', 'path_split', 'head_name',
                    'file_name', 'format_name', 'save_log', 'main_dir', 'AUTO_CREATE'):
            super().__setattr__(name, value)
        else:
            child = self.__getattr__(name)
            child.update(data=value)

    @property
    def tree(self) -> DictAttr:
        chain_list = DictAttr({})
        path_split = Path.path_cutter(Path.build_path_from_desktop(self._path))[:]
        dir_or_file_name = ""
        while dir_or_file_name != AppKeywords.name and path_split:
            dir_or_file_name = path_split[-1]
            dir_or_file_name = Formats.format_cuter(dir_or_file_name)
            full_path = Path.path_factory(self.main_dir, *path_split[1:]) if len(path_split) > 1 else self.main_dir
            key = dir_or_file_name if dir_or_file_name != "CitizenNW" and not dir_or_file_name.startswith('_') else "desktop"
            chain_list[key] = Path.build_path_from_desktop(full_path)
            path_split.pop()

        tree = {
            'path': Path.build_path_from_desktop(self._path),
            'file_name': self.file_name,
            'format_name': self.format_name,
            'tree': chain_list,
        }
        if self.format_name == "dir":
            try:
                tree['every_things'] = {
                    k: v for k, v in Dir.read(path=self._path).items()
                    if not k.startswith("_")
                }
            except Exception as e:
                logger.warning(f"Could not read directory contents: {e}")
                tree['every_things'] = {}

        return DictAttr(tree)

    def operator(self, http_type: str = "create", data: Optional[Any] = None) -> Any:
        if self.format_name not in self.files:
            raise ValueError(f"Unknown format: {self.format_name}")

        if hasattr(OsKeywords, 'http_types') and http_type not in OsKeywords.http_types:
            raise ValueError(f"Unknown operation: {http_type}")

        handler_class = self.files[self.format_name]
        method = getattr(handler_class, http_type)

        kwargs = {'path': self._path}
        if data is not None:
            kwargs['data'] = data
        if self.save_log:
            kwargs['log_curser'] = self

        try:
            result = method(**kwargs)
        except Exception as e:
            logger.error(f"Operation '{http_type}' failed on {self._path}: {e}")
            raise

        action_verb = http_type + ('ed' if http_type in ['create', 'clear', 'delete'] else '')
        msg = f"{self.file_operator_message.get(self.format_name, 'Resource')} {action_verb}: {self._path}"
        print(msg)
        logger.info(msg)

        if http_type == "read" and isinstance(result, dict):
            return DictAttr(result)
        return result

    def create(self, data: Optional[Any] = None) -> Any:
        return self.operator(http_type="create", data=data)

    @property
    def read(self) -> Any:
        return self.operator(http_type="read", data=None)

    @property
    def read_with_format(self) -> Any:
        return self.operator(http_type="read", data={"has_format": True})

    def update(self, data: Optional[Any] = None, **kwargs) -> Any:
        return self.operator(http_type="update", data=data)

    def clear(self) -> Any:
        return self.operator(http_type="clear", data=None)

    def delete(self) -> None:
        return self.operator(http_type="delete", data=None)

    @property
    def just_dirs(self) -> DictAttr:
        return self.operator(http_type="read", data={"just_dir": True})


class ShortCuts:
    """
    Predefined shortcut paths for commonly used directories and files.
    All paths are relative to the application's main directory.
    """
    main_dir = Path.main_dir()
    assets = os.path.join(main_dir, "assets")
    ledgers = os.path.join(assets, "ledgers")
    gallery = os.path.join(assets, "gallery")
    default = os.path.join(assets, "default")
    categories = os.path.join(default, "categories")
    fonts = os.path.join(assets, "fonts")
    app_font = os.path.join(fonts, "app_font.ttf")
    shop_font = os.path.join(fonts, "shop_font.ttf")
    sahel_bold = os.path.join(fonts, "sahel_bold.ttf")
    configs = os.path.join(assets, "configs")
    settings = os.path.join(configs, "settings.json")
    none_profile = os.path.join(default, "avatars", "none_profile.png")
    addressbanner = os.path.join(default, "banners", "address.png")
    food_delivered = os.path.join(default, "banners", "food_delivered.png")
    v_cake = os.path.join(default, "banners", "v_cake.jpg")


class OperationsSystem(ToDo):
    """
    High-level accessor for the application's resources using the Curser API.
    Attributes are instance-level to avoid early creation.
    """

    def __init__(self):
        super().__init__()
        self._desktop = Curser()

    @property
    def desktop(self) -> Curser:
        return self._desktop

    @property
    def assets(self) -> Curser:
        return self.desktop.assets

    @property
    def default(self) -> Curser:
        return self.assets.default

    @property
    def fonts(self) -> Curser:
        return self.assets.fonts

    @property
    def ledgers(self) -> Curser:
        return self.assets.ledgers

    @property
    def settings(self) -> Curser:
        return self.ledgers.settings_json

    @property
    def configs(self) -> Curser:
        return self.assets.configs

    @property
    def logs(self) -> Curser:
        return self.configs.logs_json

    @property
    def paths(self) -> Curser:
        return self.configs.paths_json

    @property
    def tree(self) -> DictAttr:
        cursers = {}
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            value = getattr(self, attr_name)
            if isinstance(value, Curser) and attr_name != 'desktop':
                cursers[attr_name] = value.tree
        return DictAttr(cursers)

    @property
    def root(self) -> DictAttr:
        cursers = {}
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            value = getattr(self, attr_name)
            if isinstance(value, Curser):
                cursers[attr_name] = value._path

        shortcuts = ShortCuts()
        for path_name, path_value in shortcuts.__dict__.items():
            if not path_name.startswith('_') and path_name not in cursers:
                cursers[path_name] = path_value
        return DictAttr(cursers)

    def save_tree(self):
        self.paths.update(data=self.tree)

    def on_genesis(self):
        pass


print(Path.main_dir())