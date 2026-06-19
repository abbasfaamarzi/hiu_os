import os
import json
import logging
from typing import Optional, Union, List, Dict, Any
from hiu_os.__operations__.__file__.__structure__ import HttpOperatorRequest


class JsonFile(HttpOperatorRequest):
    """
    Operations on JSON files.
    Uses logging to record events.
    """
    _logger = logging.getLogger(__name__)

    @staticmethod
    def create(path: str, data: Optional[Union[List, Dict, str]] = None, log_curser: object = None) -> None:
        logger = log_curser or JsonFile._logger
        try:
            if data is None:
                data = {}
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.info(f"JSON file created: {path}")
        except Exception as e:
            logger.error(f"Failed to create JSON file {path}: {e}")
            raise

    @staticmethod
    def read(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> Union[Dict, List]:
        logger = log_curser or JsonFile._logger
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            logger.info(f"JSON file read successfully: {path}")
            return content
        except FileNotFoundError:
            logger.warning(f"JSON file not found: {path}, returning default")
            return data if data is not None else {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {path}: {e}")
            return data if data is not None else {}
        except Exception as e:
            logger.error(f"Failed to read JSON file {path}: {e}")
            raise

    @staticmethod
    def update(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        JsonFile.create(path, data, log_curser)
        logger = log_curser or JsonFile._logger
        logger.info(f"JSON file updated: {path}")

    @staticmethod
    def clear(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        JsonFile.create(path, {}, log_curser)
        logger = log_curser or JsonFile._logger
        logger.info(f"JSON file cleared: {path}")

    @staticmethod
    def delete(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        logger = log_curser or JsonFile._logger
        try:
            if os.path.exists(path):
                os.remove(path)
                logger.info(f"JSON file deleted: {path}")
            else:
                logger.warning(f"JSON file not found for deletion: {path}")
                raise FileNotFoundError(f"File not found: {path}")
        except Exception as e:
            logger.error(f"Failed to delete JSON file {path}: {e}")
            raise