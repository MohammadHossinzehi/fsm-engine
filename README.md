# FSM Engine

A typed finite state machine engine for Python with visualization, hierarchical states, and comprehensive logging capabilities.

## What It Does

FSM Engine is a production-ready state machine library that helps you model complex workflows and application logic with clear, maintainable code. It supports:

* **Typed states and transitions** with full type hints for IDE autocomplete
* **Hierarchical (nested) states** for modeling complex behavior
* **State callbacks** (on_enter, on_exit) for side effects and lifecycle management
* **Conditional transitions** with custom guard predicates
* **Event queuing and processing** with configurable handlers
* **Visual state diagrams** in Graphviz DOT format
* **Comprehensive logging** of all state changes and transitions
* **History tracking** with full transition audit trail

## Why Use It?

Managing application state across workflows, business logic, and concurrent operations becomes complex quickly. FSM Engine provides:

1. **Correctness** via explicit state definitions preventing invalid state combinations
2. **Clarity** by expressing complex control flow as readable state transitions
3. **Debuggability** through detailed logging and visual diagrams of state graphs
4. **Testability** with deterministic state transitions independent of timing

Ideal for workflow engines, game logic, protocol implementations, and any domain requiring explicit state management.

## Installation

```bash
pip install fsm-engine
```

## Quick Start

```python
from fsm_engine import StateMachine, State, Transition

# Define states
idle = State('idle')
running = State('running')
paused = State('paused')
stopped = State('stopped')

# Create state machine
fsm = StateMachine('player', initial_state=idle)

# Add states
fsm.add_state(idle)
fsm.add_state(running)
fsm.add_state(paused)
fsm.add_state(stopped)

# Define transitions
fsm.add_transition(Transition(idle, running, 'play'))
fsm.add_transition(Transition(running, paused, 'pause'))
fsm.add_transition(Transition(paused, running, 'resume'))
fsm.add_transition(Transition(idle, stopped, 'stop'))
fsm.add_transition(Transition(running, stopped, 'stop'))
fsm.add_transition(Transition(paused, stopped, 'stop'))

# Use the state machine
print(fsm.current_state.name)  # Output: idle

fsm.trigger('play')
print(fsm.current_state.name)  # Output: running

fsm.trigger('pause')
print(fsm.current_state.name)  # Output: paused

fsm.trigger('stop')
print(fsm.current_state.name)  # Output: stopped
```

## Advanced Features

### State Callbacks

```python
def on_entering_running():
    print("Starting playback...")

def on_exiting_running():
    print("Stopping playback...")

running.on_enter(on_entering_running)
running.on_exit(on_exiting_running)
```

### Conditional Transitions

```python
# Transition only if guard condition is true
def check_battery(context: dict) -> bool:
    return context.get('battery_percent', 100) > 10

fsm.add_transition(
    Transition(idle, running, 'play'),
    guard=check_battery
)
```

### Hierarchical States

```python
# Parent and child states for nested behavior
power_on = State('power_on')
power_off = State('power_off')

idle_child = State('idle', parent=power_on)
running_child = State('running', parent=power_on)

# Transitions work within hierarchy
fsm.add_state(power_on)
fsm.add_state(power_off)
fsm.add_state(idle_child)
fsm.add_state(running_child)
```

### Visualization

```python
# Generate Graphviz diagram of the state machine
diagram = fsm.visualize(output_format='svg')
diagram.render('state_machine_diagram')
```

## Design Decisions

* **Immutability of transitions** ensures thread safety and prevents accidental modification of state graph structure
* **Callback system** rather than inheritance allows flexible composition without tight coupling
* **Guard functions** enable data driven logic without embedding conditionals in transition code
* **Separate state and transition objects** allows reuse across multiple machines and clear separation of concerns
* **Comprehensive logging** built in from day one rather than retrofitted, critical for debugging state issues

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Key test coverage includes:
* Basic state transitions and current state tracking
* Invalid transition rejection
* State callbacks execution order and exceptions
* Guard predicate evaluation
* Hierarchical state behavior
* Concurrent access patterns
* Event queuing and async dispatch
* Diagram generation and visualization

## License

MIT
