import os
import pickle
import logging
from typing import Optional, Union, List, Dict, Any
from hiu_os.__operations__.__file__.__structure__ import HttpOperatorRequest


class PickleFile(HttpOperatorRequest):
    """
    Operations on Pickle files (binary serialization).
    Uses logging to record events.
    """
    _logger = logging.getLogger(__name__)

    @staticmethod
    def create(path: str, data: Optional[Union[List, Dict, str]] = None, log_curser: object = None) -> None:
        logger = log_curser or PickleFile._logger
        try:
            if data is None:
                data = {}
            with open(path, 'wb') as f:
                pickle.dump(data, f)
            logger.info(f"Pickle file created: {path}")
        except Exception as e:
            logger.error(f"Failed to create Pickle file {path}: {e}")
            raise

    @staticmethod
    def read(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> Any:
        logger = log_curser or PickleFile._logger
        try:
            with open(path, 'rb') as f:
                content = pickle.load(f)
            logger.info(f"Pickle file read successfully: {path}")
            return content
        except FileNotFoundError:
            logger.warning(f"Pickle file not found: {path}, returning default")
            return data if data is not None else {}
        except pickle.PickleError as e:
            logger.error(f"Invalid pickle in {path}: {e}")
            return data if data is not None else {}
        except Exception as e:
            logger.error(f"Failed to read Pickle file {path}: {e}")
            raise

    @staticmethod
    def update(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        PickleFile.create(path, data, log_curser)
        logger = log_curser or PickleFile._logger
        logger.info(f"Pickle file updated: {path}")

    @staticmethod
    def clear(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        PickleFile.create(path, {}, log_curser)
        logger = log_curser or PickleFile._logger
        logger.info(f"Pickle file cleared: {path}")

    @staticmethod
    def delete(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        logger = log_curser or PickleFile._logger
        try:
            if os.path.exists(path):
                os.remove(path)
                logger.info(f"Pickle file deleted: {path}")
            else:
                logger.warning(f"Pickle file not found for deletion: {path}")
                raise FileNotFoundError(f"File not found: {path}")
        except Exception as e:
            logger.error(f"Failed to delete Pickle file {path}: {e}")
            raise