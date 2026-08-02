"""Core FSM Engine components: State, Transition, and StateMachine."""

from typing import Callable, Dict, List, Optional, Set
from dataclasses import dataclass, field
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

TransitionGuard = Callable[[dict], bool]


@dataclass(frozen=True)
class State:
    """Immutable state in a state machine."""
    
    name: str
    parent: Optional['State'] = None
    _callbacks_enter: List[Callable[[], None]] = field(default_factory=list, repr=False)
    _callbacks_exit: List[Callable[[], None]] = field(default_factory=list, repr=False)
    
    def on_enter(self, callback: Callable[[], None]) -> None:
        """Register a callback when entering this state."""
        self._callbacks_enter.append(callback)
    
    def on_exit(self, callback: Callable[[], None]) -> None:
        """Register a callback when exiting this state."""
        self._callbacks_exit.append(callback)
    
    def __hash__(self) -> int:
        return hash(self.name)


@dataclass(frozen=True)
class Transition:
    """Immutable transition between two states."""
    
    from_state: State
    to_state: State
    event: str
    guard: Optional[TransitionGuard] = None
    
    def is_valid(self, context: dict) -> bool:
        """Check if transition can be triggered given context."""
        if self.guard is None:
            return True
        try:
            return self.guard(context)
        except Exception as e:
            logger.warning(f"Guard predicate failed: {e}")
            return False
    
    def __hash__(self) -> int:
        return hash((self.from_state, self.to_state, self.event))


class StateMachine:
    """Typed finite state machine with hierarchical states and callbacks."""
    
    def __init__(self, name: str, initial_state: State):
        """Initialize state machine.
        
        Args:
            name: Machine name for logging
            initial_state: Starting state
        """
        self.name = name
        self._current_state = initial_state
        self._states: Set[State] = {initial_state}
        self._transitions: Dict[tuple, List[Transition]] = {}
        self._history: List[dict] = []
        self._context: dict = {}
        
        logger.info(f"FSM '{name}' initialized with state '{initial_state.name}'")
    
    @property
    def current_state(self) -> State:
        """Get current state."""
        return self._current_state
    
    def add_state(self, state: State) -> None:
        """Add state to machine."""
        self._states.add(state)
        logger.debug(f"Added state '{state.name}' to FSM '{self.name}'")
    
    def add_transition(self, transition: Transition, guard: Optional[TransitionGuard] = None) -> None:
        """Add transition to machine."""
        key = (transition.from_state, transition.event)
        if key not in self._transitions:
            self._transitions[key] = []
        
        if guard is not None:
            transition = Transition(
                transition.from_state,
                transition.to_state,
                transition.event,
                guard
            )
        
        self._transitions[key].append(transition)
        logger.debug(
            f"Added transition: {transition.from_state.name} "
            f"--{transition.event}--> {transition.to_state.name}"
        )
    
    def trigger(self, event: str, context: Optional[dict] = None) -> bool:
        """Trigger state transition.
        
        Args:
            event: Event name
            context: Context data for guards
            
        Returns:
            True if transition occurred, False otherwise
        """
        if context is None:
            context = {}
        
        self._context.update(context)
        
        key = (self._current_state, event)
        if key not in self._transitions:
            logger.warning(
                f"No transition from '{self._current_state.name}' on event '{event}'"
            )
            return False
        
        for transition in self._transitions[key]:
            if transition.is_valid(self._context):
                self._execute_transition(transition)
                return True
        
        logger.warning(f"All guards failed for event '{event}' from '{self._current_state.name}'")
        return False
    
    def _execute_transition(self, transition: Transition) -> None:
        """Execute state transition with callbacks."""
        old_state = self._current_state
        
        # Call exit callbacks
        for callback in old_state._callbacks_exit:
            try:
                callback()
            except Exception as e:
                logger.error(f"Error in exit callback for '{old_state.name}': {e}")
        
        self._current_state = transition.to_state
        
        # Call enter callbacks
        for callback in transition.to_state._callbacks_enter:
            try:
                callback()
            except Exception as e:
                logger.error(f"Error in enter callback for '{transition.to_state.name}': {e}")
        
        # Record history
        self._history.append({
            'timestamp': datetime.now(),
            'from_state': old_state.name,
            'to_state': transition.to_state.name,
            'event': transition.event,
            'context': self._context.copy()
        })
        
        logger.info(
            f"FSM '{self.name}' transitioned: {old_state.name} "
            f"--{transition.event}--> {transition.to_state.name}"
        )
    
    def get_history(self) -> List[dict]:
        """Get transition history."""
        return self._history.copy()
    
    def visualize(self, output_format: str = 'dot') -> str:
        """Generate state diagram in Graphviz DOT format."""
        lines = [f'digraph {self.name} {{']
        lines.append('  rankdir=LR;')
        
        # Add states
        for state in self._states:
            lines.append(f'  "{state.name}";')
        
        # Add transitions
        seen = set()
        for (from_state, event), transitions in self._transitions.items():
            for transition in transitions:
                key = (from_state.name, transition.to_state.name, event)
                if key not in seen:
                    lines.append(
                        f'  "{from_state.name}" -> "{transition.to_state.name}" '
                        f'[label="{event}"];'
                    )
                    seen.add(key)
        
        lines.append('}')
        return '\n'.join(lines)
