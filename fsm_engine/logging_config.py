"""Logging configuration for FSM Engine."""

import logging
import sys


def setup_fsm_logging(
    level: int = logging.INFO,
    format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> None:
    """Configure logging for FSM engine.
    
    Args:
        level: Logging level (default: INFO)
        format_str: Log format string
    """
    formatter = logging.Formatter(format_str)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    fsm_logger = logging.getLogger('fsm_engine')
    fsm_logger.setLevel(level)
    fsm_logger.addHandler(handler)
