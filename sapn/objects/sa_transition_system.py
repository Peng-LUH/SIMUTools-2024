from typing import List, Tuple, Set, Union
import json
from pm4py.objects.transition_system.obj import TransitionSystem
from pm4py.objects.transition_system.utils import add_arc_from_to

from pm4py import view_transition_system

from itertools import combinations
from itertools import chain, combinations

from copy import copy

class SATransitionSystem(TransitionSystem):
    # class State(TransitionSystem.State):
    #     def __init__(self, name: str, multiplicity: int, incoming=None, outgoing=None, data=None):
    #         super().__init__(name, incoming, outgoing, data)
    #         self.multiplicity = multiplicity if multiplicity is not None else 0
        
    #     def __repr__(self):
    #         return str(f"(State: {self.name}, {self.multiplicity})")
        
    class Event(object):
        def __init__(self, name=None) -> None:
            self.name = name
        def __repr__(self) -> str:
            return str(self.name)
    
    class Transition(TransitionSystem.Transition):
        def __init__(self, name, from_state, to_state, data=None):
            super().__init__(name, from_state, to_state, data)
            
        def __repr__(self):
            return f"({self.from_state.name}, {self.name}, {self.to_state.name})"
        
        def get_state_transition(self):
            return (self.from_state, self.name, self.to_state)
        
        
    def __init__(self, name=None, states=None, transitions=None, initial_states=None, events=None, state_objects=None, transition_objects=None):
        super().__init__(name, states, transitions)
        self.initial_states = initial_states if initial_states is not None else set()
        self.events = events if events is not None else set()
    
    def read_from_json(self, path_to_json_file: str):
        '''
        Construct a transition system from a jason file
        
        PARAMETERS:
        path_to_json_file (str): the path to the json file
        
        RETURN:
        Binary: True if success, otherwise False.
        '''
        pass
    
    def ts_view(self):
        '''
        view the transition system in png format
        
        PARAMETERS: None
        RETURNS: None
        '''
        view_transition_system(transition_system=self, format='png', bgcolor='white')

    def print_info(self):
        '''
        print relevent information about the transition system
        
        PARAMETERS: None
        RETURNS: None
        '''
        print(f'Initial States: {self.get_initial_states()}')
        print(f'Events: {self.get_event_names()}')
        print(f'States: {self.get_state_names()}')
        print(f'State Transitions: {self.get_all_state_transitions()}')
    
    ## initial state
    def get_initial_states(self):
        '''
        Get the set of initial states
        
        Parameters: 
        None
        
        Returns:
        Set[State]: set of initial states
        '''
        return self.initial_states
    
    def set_intial_state(self, state_name: str) -> bool:
        """
        Sets an initial state for the transition system.

        Parameters:
        ----------
        state_name : str
            The name of the state to be set as the initial state.

        Returns:
        -------
        bool
            True if the state is set as the initial state successfully, otherwise False.

        Raises:
        ------
        ValueError
            If the state with the given name is not found.
        """
        try:    
            if state_name in self.get_state_names():
                self.initial_states.add(state_name)
                return True
            else:
                raise ValueError(f'State "{state_name}" not found.')
        except ValueError as e:
            print(f'Error: {e.args[0]}')
            return False
    
    ## State
    def __add_state(self, state_name:str) -> bool:
        '''
        Add a state object to the transition system.
        
        PARAMETERS:
        state_name (str): Name of the state
        
        RETURNS:
        bool: True if the state was added successfully, otherwise False
        '''
        if not state_name:
            return False
        
        if state_name not in self.get_state_names():
            state = TransitionSystem.State(name=state_name)
            self.states.add(state)
            return True
        return False
    
    def __add_states_batch(self, state_names: List[str]):
        '''
        add state objects to the transition system
        
        PARAMETERS:
        
        '''
        state_added = []
        for sn in state_names:
            flag = self.__add_state(state_name=sn)
            if flag:
                state_added.append(sn)
        return state_added
    
    def __ensure_state_exists(self, state_name: str):
        if state_name not in self.get_state_names():
            self.__add_state(state_name=state_name)
    
    def get_states(self) -> set:
        '''
        Get the set of state objects.
        
        Parameters:
        None
        
        Returns:
        Set[TransitionSystem.State]: A set of state objects
        '''
        return self.states
    
    def get_state_names(self) -> set:
        """
        Get the set of state names.

        PARAMETERS:
        None

        RETURNS:
        Set[str]: A set of state names
        """
        return {s.name for s in self.states}
    
    
    def get_state_by_name(self, state_name: str) -> TransitionSystem.State:
        """
        Retrieves a state object by its name from the list of states.

        Parameters:
        ----------
        state_name : str
            The name of the state to be retrieved.

        Returns:
        -------
        TransitionSystem.State or None
            The state object if found, or None if the state name is not found.

        Raises:
        ------
        ValueError
            If the state with the given name is not found.
        """
        try:
            if state_name not in self.get_state_names():
                raise ValueError(f'State with name "{state_name}" not found!')
            
            for s in self.states:
                if state_name == s.name:
                    return s
        except ValueError as e:
            print(f'Warning: {e.args[0]}')
            return None
    
    # def get_state_multiplicity(self, state_name: str) -> int:
        
    #     for s in self.states:
    #         if s.name == state_name:
    #             return s.multiplicity
    
    # def get_all_state_multiplicity(self) -> dict:
    #     state_multiplicity = {}
        
    #     for s in self.states:
    #         state_multiplicity[s.name] = s.multiplicity
            
    #     return state_multiplicity
    
    
    # def set_state_multiplicity(self, state_name: str, multiplicity: int) -> bool:
        
    #     for s in self.states:
    #         if s.name == state_name:
    #             s.multiplicity = multiplicity
        
    #             return True
        
    #     return False
    
    ## Event
    def __add_event(self, event_name: str) -> bool:
        """
        Adds a new event to the transition system if it does not already exist.

        Parameters:
        ----------
        event_name : str
            The name of the event to be added.

        Returns:
        -------
        bool: 
            True if the event was added successfully, or if the event already exists.
        """
        event_names = self.get_event_names()
        if event_name not in event_names:
            event = self.Event(name=event_name)
            self.events.add(event)
        return True
    
    def __ensure_event_exists(self, event_name: str):
        if event_name not in self.get_event_names():
            self.__add_event(event_name=event_name)
        
    
    def get_events(self) -> set:
        '''
        Get the set of event objects
        
        Parameters:
        ----------
        None
        
        Returns:
        --------
        Set[Event]: 
            the set of events in transition system.
        '''
        return self.events
    
    def get_event_names(self) -> set:
        """
        Retrieves the names of all events in the transition system.

        Parameters:
        ----------
        None

        Returns:
        -------
        Set[str]
            A set containing the names of all events in the transition system.
        """
        return {e.name for e in self.events}
    
    def get_event_by_name(self, event_name: str) -> Event:
        """
        Retrieves an event object by its name from the list of events.

        Parameters:
        ----------
        event_name : str
            The name of the event to be retrieved.

        Returns:
        -------
        Event or None
            The event object if found, or None if no event with the specified name exists.
        """
        event = None
        for e in self.events:
            if e.name == event_name:
                event = e
        return event
    
    ## transitions
    def add_transition(self, event_name: str, from_state_name: str, to_state_name: str, data=None) -> bool:
        """
        Adds a transition between states in the transition system.

        Parameters:
        ----------
        name : str
            The name of the event triggering the transition.
        from_state_name : str
            The name of the initial state.
        to_state_name : str
            The name of the target state.
        data : optional
            Additional data associated with the transition.

        Returns:
        -------
        bool
            True if the transition was successfully added, False otherwise.

        Raises:
        ------
        ValueError
            If the state transition already exists.
        """
        # check if state transition already exsits
        st = (from_state_name, event_name, to_state_name)
        if st in self.get_all_state_transitions():
            raise ValueError(f'State transition "{st}" already exists!')
        
        # ensure the event, from_state and to_state exist
        self.__ensure_event_exists(event_name=event_name)
        self.__ensure_state_exists(state_name=from_state_name)
        self.__ensure_state_exists(state_name=to_state_name)
        
        # get the from_state and to_state objects
        from_state = self.get_state_by_name(state_name=from_state_name)
        to_state = self.get_state_by_name(state_name=to_state_name)
        
        if from_state and to_state:
            add_arc_from_to(name=event_name, fr=from_state, to=to_state, ts=self, data=data)
            return True
        return False
    
    
    def add_transitions_batch(self, state_transitions: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """
        Adds multiple state transitions to the transition system.

        Parameters:
        ----------
        state_transitions : List[Tuple[str, str, str]]
            A list of tuples, each containing the from_state_name, event name, and to_state_name.

        Returns:
        -------
        List[Tuple[str, str, str]]
            A list of successfully added state transitions.
        """
        added_state_transitions = []
        for st in state_transitions:
            from_state_name, event_name, to_state_name = st
            try:
                flag = self.add_transition(event_name=event_name, from_state_name=from_state_name, to_state_name=to_state_name)
                if flag:
                    added_state_transitions.append(st)
            except ValueError as e:
                print(f"Failed to add transition {st}: {e.args[0]}")
        return added_state_transitions
    
    def get_transition(self, event_name:str, from_state_name:str, to_state_name:str) -> Union[Transition, None]:
        """
        Retrieves a specific transition object by its name and the names of its source and target states.

        Parameters:
        ----------
        transition_name : str
            The name of the transition.
        from_state_name : str
            The name of the source state.
        to_state_name : str
            The name of the target state.

        Returns:
        -------
        Transition or None
            The transition object if found, otherwise None.
        """
        for t in self.transitions:
            if t.name == event_name and t.from_state.name == from_state_name and t.to_state.name == to_state_name:
                return t
        return None
    
    def get_transitions_by_name(self, event_name: str) -> set:
        """
        Retrieves the set of transition objects associated with a specific event name in the transition system.
        
        Parameters:
        ----------
        event_name: str
            The name of the event to filter transitions by.

        Returns:
        -------
        set
            A set of transitions associtated with the sepcified event name.
        """
        transitions = set()
        for t in self.transitions:
            if t.name == event_name:
                transitions.add(t)
        return transitions
    
    
    def get_state_transition_by_event(self, event_name: str) -> Set[Tuple[str, str, str]]:
        """
        Retrieves all state transitions associated with a given event name.

        Each state transition is represented as a tuple containing the source state name,
        the event name, and the target state name.

        Parameters:
        ----------
        event_name : str
            The name of the event to filter transitions by.

        Returns:
        -------
        Set[Tuple[str, str, str]]
            A set of state transitions associated with the specified event name, 
            where each transition is a tuple (from_state_name, event_name, to_state_name).
        """
        # Initialize an empty set to store state transitions for the given event
        state_transitions = set()
        
         # Iterate through all transitions and collect those that match the event name
        for t in self.transitions:
            if t.name == event_name:
                st = (t.from_state.name, t.name, t.to_state.name)
                state_transitions.add(st)
        
        return state_transitions
    
    
    def get_state_transitions_by_from_state(self, from_state_name: str) -> Set[Tuple[str, str, str]]:
        """
        Retrieves a set of state transitions that originate from a specified source state.

        Each tuple in the set contains the source state name, the transition name, and the target state name.

        Parameters:
        ----------
        from_state_name : str
            The name of the source state to filter transitions by.

        Returns:
        -------
        set
            A set of tuples, each representing a state transition in the form (from_state_name, transition_name, to_state_name).
        """
        state_transitions = set() # Initialize an empty set to store machting transitions
        
        for t in self.transitions:
            if t.from_state.name == from_state_name:
                # add the transition to the set if it matches the source state
                st = (t.from_state.name, t.name, t.to_state.name)
                state_transitions.add(st) 
        
        return state_transitions # return the set of matching transitions
    
    def get_state_transitions_by_to_state(self, to_state_name: str) -> Set[Tuple[str, str, str]]:
        """
        Retrieves a set of state transitions that target a specified state.

        Each tuple in the set contains the source state name, the transition name, and the target state name.

        Parameters:
        ----------
        to_state_name : str
            The name of the target state to filter transitions by.

        Returns:
        -------
        set
            A set of tuples, each representing a state transition in the form (from_state_name, transition_name, to_state_name).
        """
        state_transitions = set() # Initialize an empty set to store 
        for t in self.transitions:
            if t.to_state.name == to_state_name:
                # add the transition to the set if it matches the target state
                st = (t.from_state.name, t.name, t.to_state.name)
                state_transitions.add(st)
        return state_transitions
    
    def get_all_state_transitions(self) -> Set[Tuple[str, str, str]]:
        """
        Retrieves the set of all state transitions represented as tuples.

        Each tuple contains the source state name, the event name, and the target state name.

        Parameters:
        ----------
        None

        Returns:
        -------
        <set>
            A set of tuples, each representing a state transition in the form (from_state_name, event_name, to_state_name).
        """
        state_transitions = set() # Initialize an empty set to store state transitions
        
        for t in self.transitions:
            st = (t.from_state.name, t.name, t.to_state.name)
            state_transitions.add(st) # Add each state transition as a tuple to the set
            
        return state_transitions
    
    
    def create_from_ts_dict(self, ts_dict: dict) -> bool:
        
        temp = SATransitionSystem()
        
        temp.add_transitions_batch(state_transitions=ts_dict["state_transitions"])
        
        if not temp.get_event_names() == ts_dict["events"]:
            return False
        
        if not temp.get_state_names() == ts_dict["states"]:
            return False
        
        if not temp.set_intial_state(state_name=ts_dict["initial_states"]):
            return False
        
        self = temp
        
        return True
    
    
    ## conversion
    def generate_ts_dict(self):
        try:
            ts_dict = {
                'events': self.get_event_names(),
                'states': self.get_state_names(),
                'state_transitions': self.get_all_state_transitions(),
                'initial_states': self.get_initial_states()
            }
            return ts_dict
        except ValueError as e:
            return e.args[0]
    
    
        