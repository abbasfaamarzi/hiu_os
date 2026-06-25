import os
import shutil
import logging
from typing import Optional, Union, List, Dict, Any
from hiu_os.__operations__.__file__.__structure__ import HttpOperatorRequest
from hiu_os.__operations__.__file__.__base__.__formats__ import Formats


class Dir(HttpOperatorRequest):
    """
    Operations on directories.
    Uses logging to record events.
    """
    _logger = logging.getLogger(__name__)

    @staticmethod
    def create(path: str, data: Optional[Union[List, Dict, str]] = None, log_curser: object = None) -> Any:
        logger = log_curser or Dir._logger
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created: {path}")
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            raise

    @staticmethod
    def dirslist(path, as_type=None, has_format=False):
        """List directory contents (no logging for this helper)."""
        dirs = os.listdir(path)
        if as_type is None or as_type is list or isinstance(as_type, list):
            return [os.path.join(path, dirname) for dirname in dirs]
        elif as_type is dict or isinstance(as_type, dict):
            result = {}
            for dirname in dirs:
                key = dirname if has_format else Formats.format_cuter(dirname)
                result[key] = os.path.join(path, dirname)
            return result
        return None

    @staticmethod
    def read(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> Any:
        logger = log_curser or Dir._logger
        try:
            result = Dir.dirslist(path=path, as_type=dict)
            logger.info(f"Directory read successfully: {path} (found {len(result)} items)")
            return result
        except FileNotFoundError:
            logger.warning(f"Directory not found: {path}")
            return {}
        except Exception as e:
            logger.error(f"Failed to read directory {path}: {e}")
            raise

    @staticmethod
    def update(path: str, new_name: str = None, data: Optional[Union[List, Dict]] = None, log_curser=None):
        logger = log_curser or Dir._logger
        try:
            if new_name is None:
                logger.error("new_name not provided for rename")
                raise ValueError("For renaming a directory, new_name must be provided")
            parent = os.path.dirname(path)
            new_path = os.path.join(parent, new_name)
            if os.path.exists(new_path):
                logger.error(f"Destination already exists: {new_path}")
                raise FileExistsError(f"Destination {new_path} already exists.")
            os.rename(path, new_path)
            logger.info(f"Directory renamed: {path} -> {new_path}")
            return new_path
        except FileNotFoundError:
            logger.warning(f"Source directory not found: {path}")
            raise
        except Exception as e:
            logger.error(f"Failed to rename directory {path}: {e}")
            raise

    @staticmethod
    def clear(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None or str:
        logger = log_curser or Dir._logger
        try:
            if not os.path.isdir(path):
                logger.warning(f"Path is not a directory: {path}")
                return "Path is not a directory."
            count = 0
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                count += 1
            logger.info(f"Directory cleared: {path} (removed {count} items)")
            return "Directory cleared successfully."
        except Exception as e:
            logger.error(f"Failed to clear directory {path}: {e}")
            raise

    @staticmethod
    def delete(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        logger = log_curser or Dir._logger
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                logger.info(f"Directory deleted: {path}")
            else:
                logger.warning(f"Directory not found for deletion: {path}")
                raise FileNotFoundError(f"Directory not found: {path}")
        except Exception as e:
            logger.error(f"Failed to delete directory {path}: {e}")
            raise