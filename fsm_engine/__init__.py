"""FSM Engine: Typed finite state machine with visualization and logging."""

__version__ = "0.1.0"

from .core import State, StateMachine, Transition, TransitionGuard
from .exceptions import InvalidStateError, InvalidTransitionError, GuardFailedError
from .logging_config import setup_fsm_logging

__all__ = [
    "State",
    "StateMachine",
    "Transition",
    "TransitionGuard",
    "InvalidStateError",
    "InvalidTransitionError",
    "GuardFailedError",
    "setup_fsm_logging",
]
