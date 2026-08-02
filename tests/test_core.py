"""Unit tests for FSM Engine core components."""

import pytest
from fsm_engine.core import State, Transition, StateMachine
from fsm_engine.exceptions import InvalidStateError, InvalidTransitionError


def test_state_creation():
    """Test state creation and immutability."""
    state = State('idle')
    assert state.name == 'idle'
    assert state.parent is None


def test_state_hierarchy():
    """Test parent state relationships."""
    parent = State('power_on')
    child = State('idle', parent=parent)
    assert child.parent == parent
    assert child.name == 'idle'


def test_transition_creation():
    """Test transition creation."""
    state1 = State('idle')
    state2 = State('running')
    transition = Transition(state1, state2, 'start')
    
    assert transition.from_state == state1
    assert transition.to_state == state2
    assert transition.event == 'start'
    assert transition.guard is None


def test_transition_with_guard():
    """Test transition with guard predicate."""
    state1 = State('idle')
    state2 = State('running')
    
    def check_ready(ctx):
        return ctx.get('ready', False)
    
    transition = Transition(state1, state2, 'start', guard=check_ready)
    
    assert transition.is_valid({'ready': True})
    assert not transition.is_valid({'ready': False})


def test_state_machine_creation():
    """Test state machine initialization."""
    initial_state = State('idle')
    fsm = StateMachine('player', initial_state)
    
    assert fsm.name == 'player'
    assert fsm.current_state == initial_state


def test_basic_transition():
    """Test basic state transition."""
    idle = State('idle')
    running = State('running')
    
    fsm = StateMachine('player', idle)
    fsm.add_state(idle)
    fsm.add_state(running)
    fsm.add_transition(Transition(idle, running, 'play'))
    
    assert fsm.current_state == idle
    result = fsm.trigger('play')
    assert result is True
    assert fsm.current_state == running


def test_invalid_transition():
    """Test that invalid transitions fail."""
    idle = State('idle')
    running = State('running')
    stopped = State('stopped')
    
    fsm = StateMachine('player', idle)
    fsm.add_state(idle)
    fsm.add_state(running)
    fsm.add_state(stopped)
    
    fsm.add_transition(Transition(idle, running, 'play'))
    
    result = fsm.trigger('stop')
    assert result is False
    assert fsm.current_state == idle


def test_state_callbacks():
    """Test state enter/exit callbacks."""
    call_log = []
    
    idle = State('idle')
    running = State('running')
    
    def on_running_enter():
        call_log.append('enter_running')
    
    def on_idle_exit():
        call_log.append('exit_idle')
    
    idle.on_exit(on_idle_exit)
    running.on_enter(on_running_enter)
    
    fsm = StateMachine('player', idle)
    fsm.add_state(idle)
    fsm.add_state(running)
    fsm.add_transition(Transition(idle, running, 'play'))
    
    fsm.trigger('play')
    
    assert 'exit_idle' in call_log
    assert 'enter_running' in call_log


def test_transition_history():
    """Test that transition history is recorded."""
    idle = State('idle')
    running = State('running')
    stopped = State('stopped')
    
    fsm = StateMachine('player', idle)
    fsm.add_state(idle)
    fsm.add_state(running)
    fsm.add_state(stopped)
    
    fsm.add_transition(Transition(idle, running, 'play'))
    fsm.add_transition(Transition(running, stopped, 'stop'))
    
    fsm.trigger('play')
    fsm.trigger('stop')
    
    history = fsm.get_history()
    assert len(history) == 2
    assert history[0]['event'] == 'play'
    assert history[1]['event'] == 'stop'


def test_visualization():
    """Test state diagram generation."""
    idle = State('idle')
    running = State('running')
    
    fsm = StateMachine('player', idle)
    fsm.add_state(idle)
    fsm.add_state(running)
    fsm.add_transition(Transition(idle, running, 'play'))
    
    diagram = fsm.visualize()
    
    assert 'digraph player' in diagram
    assert 'idle' in diagram
    assert 'running' in diagram
    assert 'play' in diagram
