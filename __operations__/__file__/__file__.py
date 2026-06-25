import os
import logging
from typing import Optional, Union, List, Dict, Any
from hiu_os.__operations__.__file__.__structure__ import HttpOperatorRequest


class File(HttpOperatorRequest):
    """
    Operations on plain text files (txt, csv, etc.).
    Uses logging to record events.
    """
    _logger = logging.getLogger(__name__)

    @staticmethod
    def create(path: str, data: Optional[Union[List, Dict, str]] = None, log_curser: object = None) -> None:
        """Create a text file with the given data (overwrites if exists)."""
        logger = log_curser or File._logger
        try:
            with open(path, 'w', encoding='utf-8') as f:
                if data is None:
                    f.write('')
                elif isinstance(data, str):
                    f.write(data)
                else:
                    f.write(str(data))
            logger.info(f"File created successfully: {path}")
        except Exception as e:
            logger.error(f"Failed to create file {path}: {e}")
            raise

    @staticmethod
    def read(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> str:
        """Read the entire content of a text file. Returns default if file not found."""
        logger = log_curser or File._logger
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"File read successfully: {path} (length={len(content)})")
            return content
        except FileNotFoundError:
            logger.warning(f"File not found: {path}, returning default")
            return data if data is not None else ""
        except Exception as e:
            logger.error(f"Failed to read file {path}: {e}")
            raise

    @staticmethod
    def update(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        """Overwrite the file with new data (same as create)."""
        File.create(path, data, log_curser)
        logger = log_curser or File._logger
        logger.info(f"File updated: {path}")

    @staticmethod
    def clear(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        """Empty the file content."""
        logger = log_curser or File._logger
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write('')
            logger.info(f"File cleared: {path}")
        except Exception as e:
            logger.error(f"Failed to clear file {path}: {e}")
            raise

    @staticmethod
    def delete(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        """Delete the file. Raises FileNotFoundError if it does not exist."""
        logger = log_curser or File._logger
        try:
            if os.path.exists(path):
                os.remove(path)
                logger.info(f"File deleted: {path}")
            else:
                logger.warning(f"File not found for deletion: {path}")
                raise FileNotFoundError(f"File not found: {path}")
        except Exception as e:
            logger.error(f"Failed to delete file {path}: {e}")
            raise