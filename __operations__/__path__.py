"""
Path handling utilities for the operating system.
Provides enhanced path splitting, joining, and a cursor-based navigation system.
"""

import os
import logging
from hiu_os.__operations__.__file__.__base__.__keywords__ import OsKeywords, AppKeywords
from hiu_os.__operations__.__file__.__base__.__formats__ import Formats

logger = logging.getLogger(__name__)


class Path:
    """
    Enhanced path handling class with path splitting, joining, and navigation.
    This class provides static methods to manipulate filesystem paths in a
    platform-aware manner, with support for both string and bytes representations.
    """

    @staticmethod
    def split(path, sep=None):
        """
        Split a path string into its components using the specified separator.
        If no separator is given, uses the default OS separator.

        Args:
            path (str or bytes): The path to split.
            sep (str or bytes, optional): The separator to use.

        Returns:
            list: A list of path components (non-empty strings/bytes).
        """
        sep = sep if sep else OsKeywords.sep
        logger.debug(f"Splitting path: {path} with separator: {sep}")
        parts = [part for part in path.split(sep) if part != '']
        logger.debug(f"Split result: {parts}")
        return parts

    @staticmethod
    def path_cutter(path=None):
        """
        Split a path into its components using the most appropriate separator
        (supports both string and bytes paths).

        Args:
            path (str or bytes, optional): The path to split. Defaults to __file__.

        Returns:
            list: List of path components.
        """
        path = path if path else __file__
        logger.debug(f"path_cutter called with: {path} (type: {type(path)})")

        if isinstance(path, bytes):
            if OsKeywords.sep_b in path:
                return Path.split(path, OsKeywords.sep_b)
            elif OsKeywords.seps_b in path:
                return Path.split(path, OsKeywords.seps_b)
            elif OsKeywords.colon_b in path:
                return Path.split(path, OsKeywords.colon_b)
        else:
            if OsKeywords.sep in path:
                return Path.split(path)
            elif OsKeywords.seps in path:
                return Path.split(path, OsKeywords.seps)
            elif OsKeywords.colon in path:
                return Path.split(path, OsKeywords.colon)

        logger.warning("No known separator found in path, returning empty list.")
        return []

    @staticmethod
    def join(*parts) -> str:
        """
        Join path components intelligently using os.path.join, with a fix for
        Windows drive letters (e.g., 'C:').

        Args:
            *parts: Variable number of path components.

        Returns:
            str: The joined path.
        """
        logger.debug(f"Joining parts: {parts}")
        path = os.path.join(*parts)
        # Fix for Windows drive letter: ensure a separator after the drive
        if len(parts) > 0 and parts[0].endswith(":") and not path.startswith(parts[0] + os.sep):
            path = parts[0] + os.sep + os.path.join(*parts[1:])
        logger.debug(f"Joined path: {path}")
        return path

    @staticmethod
    def location_dir_path(path):
        """
        Get the directory name of a given path.

        Args:
            path (str): The file or directory path.

        Returns:
            str: The parent directory path.
        """
        dirname = os.path.dirname(path)
        logger.debug(f"location_dir_path({path}) -> {dirname}")
        return dirname

    @staticmethod
    def main_dir(dir_name = None):
        """
        Determine the main application directory by locating the application
        name (version_name) in the path components of the current file.

        Returns:
            str: The main directory path.
        """
        dirname = Path.location_dir_path(__file__)
        parts = Path.path_cutter(dirname)
        try:
            app_name_index = parts.index(dir_name if dir_name else AppKeywords.version_name)
            main_dir = parts[:app_name_index + 1]
            joined = Path.join(*main_dir)
            logger.info(f"Main directory detected: {joined}")
            return joined
        except ValueError:
            logger.warning(f"App name '{AppKeywords.version_name}' not found in path, returning dirname.")
            return dirname
        except Exception as e:
            logger.error(f"Error finding main directory: {e}")
            return dirname

    @staticmethod
    def path_factory(main_dir, *args):
        """
        Construct a path by joining a base directory with additional components.

        Args:
            main_dir (str): The base directory.
            *args: Additional path components.

        Returns:
            str: The complete path.
        """
        result = os.path.join(main_dir, *args)
        logger.debug(f"path_factory({main_dir}, {args}) -> {result}")
        return result

    @staticmethod
    def path_builder(*args):
        """
        Build a path relative to the main application directory.

        Args:
            *args: Additional path components.

        Returns:
            str: The absolute path inside the main directory.
        """
        return Path.path_factory(Path.main_dir(), *args)

    @staticmethod
    def build_path_from_desktop(path):
        """
        Extract a subpath starting from the application name (AppKeywords.name)
        within the given path. Useful for desktop shortcuts or absolute paths.

        Args:
            path (str): The full path.

        Returns:
            str: The subpath starting from the application name, or the directory
                 of the input path if the application name is not found.
        """
        dirname = Path.location_dir_path(path)
        parts = path.split(OsKeywords.sep)
        try:
            app_name_index = parts.index(AppKeywords.name)
            main_dir = parts[app_name_index:]
            joined = Path.join(*main_dir)
            logger.debug(f"build_path_from_desktop({path}) -> {joined}")
            return joined
        except ValueError:
            logger.warning(f"App name '{AppKeywords.name}' not found in path, returning dirname.")
            return dirname
        except Exception as e:
            logger.error(f"Error building path from desktop: {e}")
            return dirname


class AppCurser:
    """
    A cursor-based navigator for traversing file system paths with a fluent interface.
    It supports chaining via attribute access or method calls, and handles file extensions.

    Attributes:
        _path (str): The current path.
        parent (AppCurser or None): The parent cursor.
        child_name (str or None): The name of the child component.
        file (bool): Indicates whether the current path points to a file (set when extension is known).
    """

    KNOWN_EXTENSIONS = OsKeywords.KNOWN_EXTENSIONS

    def __init__(self, base_path, parent=None):
        """
        Initialize an AppCurser instance.

        Args:
            base_path (str): The starting path.
            parent (AppCurser, optional): The parent cursor.
        """
        self._path = base_path
        self.parent = parent
        self.child_name = None
        self.file = False  # Initialize file flag; will be set if an extension is detected
        logger.debug(f"AppCurser initialized with path: {base_path}")

    def getattrs(self, name):
        """
        Traverse to a child path component. If the name is a known extension,
        it treats the current path as a file and appends the extension.

        Args:
            name (str): The child name or extension.

        Returns:
            AppCurser: A new cursor for the resolved path.
        """
        logger.debug(f"AppCurser.getattrs({name}) on path: {self._path}")

        # Determine new path based on whether name is an extension or a directory
        if name in AppCurser.KNOWN_EXTENSIONS:
            # If current path does not have a dot, treat as file with extension
            if "." not in self._path:
                new_file_path = f"{self._path}.{name}"
                new_node = AppCurser(new_file_path, parent=self)
                new_node.file = True
            else:
                # Already has extension; just create a copy
                new_node = AppCurser(self._path, parent=self)
                new_node.file = True
        else:
            # Treat as directory
            new_path = f"{self._path}\\{name}"  # Using backslash; may need platform independence
            new_node = AppCurser(new_path, parent=self)
            new_node.file = False

        self.child_name = name
        logger.debug(f"Created new AppCurser with path: {new_node._path}")
        return new_node

    def __getattr__(self, name):
        """
        Allow attribute-style navigation (e.g., cursor.subdir).

        Args:
            name (str): The child name.

        Returns:
            AppCurser: The child cursor.
        """
        return self.getattrs(name)

    def __call__(self, name):
        """
        Allow call-style navigation (e.g., cursor('subdir')).

        Args:
            name (str): The child name.

        Returns:
            AppCurser: The child cursor.
        """
        return self.getattrs(name)

    def __str__(self):
        """Return the current path as a string."""
        return self._path

    def __repr__(self):
        """Return a developer-friendly representation."""
        return f"AppCurser({self._path!r})"