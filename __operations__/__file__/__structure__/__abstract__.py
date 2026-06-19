from abc import ABC, abstractmethod
from typing import Union, Optional, List, Dict, Any
from __operations__.__file__.__base__ import DictAttr, LifeCycleLog
import logging
import os


class HttpOperatorRequest(ABC, LifeCycleLog):
    """
    Abstract base class defining the standard interface for HTTP-like operations
    on resources. Uses logging for event recording.
    """

    born = None
    http_status = DictAttr(
        {
            "status" : "in develop"
        }
    )  # همان ساختار قبلی، ولی فقط برای مرجع

    @staticmethod
    @abstractmethod
    def create(path: str, data: Optional[Union[List, Dict, str]] = None, log_curser: object = None) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def read(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def update(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def clear(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        pass

    @staticmethod
    @abstractmethod
    def delete(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> None:
        pass

    @staticmethod
    def clear_and_update(path: str, data: Optional[Union[List, Dict]] = None, log_curser: object = None) -> Any:
        """Perform clear then update, logging both steps."""
        logger = log_curser or logging.getLogger('HttpOperatorRequest')
        try:
            HttpOperatorRequest.clear(path, data, log_curser)
            logger.info("Clear succeeded, proceeding to update")
        except Exception as e:
            logger.error(f"Clear failed: {e}")
            raise
        try:
            result = HttpOperatorRequest.update(path, data, log_curser)
            logger.info("Update succeeded after clear")
            return result
        except Exception as e:
            logger.error(f"Update failed after clear: {e}")
            raise