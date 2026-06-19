import logging
import time
from typing import Optional, Any

logger = logging.getLogger(__name__)


class LifeCycleLog:
    """
    Abstract class for tracking the lifecycle of an operating system process,
    application, or workflow. It defines hooks for starting, logging actions,
    checking state, stopping, and generating a report.

    This class uses static methods and shared class-level attributes to maintain
    state across calls. It is designed to be used as a singleton-like logger
    for lifecycle events.
    """

    # Shared class attributes for state management
    main_dir = None
    _path = None
    child_name = None
    path_split = None
    parent = None
    head_name = None
    file_name: str = None          # The name of the file being logged
    format_name: str = None        # The format (e.g., 'json', 'pkl')
    start_working: bool = False    # Flag indicating whether the lifecycle has started
    status_code: int = 0           # Current HTTP-like status code
    _log_cursor = None             # A cursor-like object for writing logs (assumed to have .update())

    @staticmethod
    def life_cycle(
        http_request_type: str,
        life_cycle: str = "working",
        msg: Optional[Any] = None,
        status_code: int = 201
    ) -> None:
        """
        Internal method to log a lifecycle event.

        Args:
            http_request_type (str): The type of HTTP request (e.g., 'GET', 'POST').
            life_cycle (str): The lifecycle phase ('start', 'working', 'stop').
            msg (Any, optional): Additional message or data.
            status_code (int): HTTP-like status code for the event.

        Logs:
            - If start_working is False, it calls start() and returns.
            - If _log_cursor is None, it silently returns.
            - Otherwise, it updates the log cursor with a structured log entry.
        """
        logger.debug(
            f"life_cycle called: request_type={http_request_type}, "
            f"life_cycle={life_cycle}, status={status_code}, msg={msg}"
        )

        # If lifecycle hasn't been started, start it
        if not LifeCycleLog.start_working:
            logger.warning("Lifecycle not started; calling start() automatically.")
            LifeCycleLog.start(http_request_type)
            return

        # If no cursor is set, we cannot write logs
        if LifeCycleLog._log_cursor is None:
            logger.error("Log cursor is None; cannot write lifecycle log.")
            return

        # Build a structured log entry and update the cursor
        log_entry = {
            LifeCycleLog.file_name: {
                life_cycle: {
                    LifeCycleLog.format_name: {
                        http_request_type: {
                            "time_stamp": time.time(),
                            "msg": msg,
                            "status_code": status_code
                        }
                    }
                }
            }
        }
        try:
            LifeCycleLog._log_cursor.update(path="log.json", data=log_entry)
            logger.info(f"Lifecycle log written: {life_cycle} for {http_request_type}")
        except Exception as e:
            logger.error(f"Failed to write lifecycle log: {e}")

    @staticmethod
    def working(http_request_type: str, status_code: int, msg: Any) -> None:
        """
        Log a 'working' lifecycle event.

        Args:
            http_request_type (str): The HTTP request type.
            status_code (int): The status code.
            msg (Any): The message or data.
        """
        logger.info(f"Working event: {http_request_type} status {status_code}")
        LifeCycleLog.life_cycle(http_request_type, life_cycle="working", msg=msg, status_code=status_code)
        LifeCycleLog.status_code = status_code

    @staticmethod
    def start(http_request_type: str) -> None:
        """
        Log the 'start' lifecycle event. Also sets start_working to True.

        Args:
            http_request_type (str): The HTTP request type.
        """
        logger.info(f"Starting lifecycle for request: {http_request_type}")
        LifeCycleLog.start_working = True
        LifeCycleLog.life_cycle(
            http_request_type,
            life_cycle="start",
            msg="Wow I'm here!",
            status_code=LifeCycleLog.status_code
        )

    @staticmethod
    def stop(http_request_type: str, status_code: int, msg: Any) -> None:
        """
        Log the 'stop' lifecycle event.

        Args:
            http_request_type (str): The HTTP request type.
            status_code (int): The final status code.
            msg (Any): The closing message.
        """
        logger.info(f"Stopping lifecycle for request: {http_request_type} with status {status_code}")
        LifeCycleLog.life_cycle(
            http_request_type=http_request_type,
            life_cycle="stop",
            msg=msg,
            status_code=status_code
        )