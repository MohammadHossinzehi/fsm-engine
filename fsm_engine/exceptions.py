"""FSM Engine custom exceptions."""


class InvalidStateError(Exception):
    """Raised when state is invalid or undefined."""
    pass


class InvalidTransitionError(Exception):
    """Raised when transition is not allowed from current state."""
    pass


class GuardFailedError(Exception):
    """Raised when transition guard predicate fails."""
    pass
