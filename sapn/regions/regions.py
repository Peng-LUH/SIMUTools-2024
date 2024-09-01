import random
import math
from pprint import pprint
from copy import copy
from typing import Set, Union, Dict, List

from objects.sa_transition_system import SATransitionSystem


def create_sample_ts() -> SATransitionSystem:
    """
    Creates a sample transition system for testing.

    Returns:
    -------
    SATransitionSystem
        A sample transition system with predefined states and transitions.
    """
    # Initialize the transition system
    ts = SATransitionSystem()
    
    # Define a list of state transitions
    state_transitions = [('s_1', 'a', 's_2'), ('s_1', 'b', 's_3'), ('s_2', 'c', 's_4'), ('s_3', 'c', 's_4')]
    
    # Add the state transitions to the transition system in a batch
    ts.add_transitions_batch(state_transitions=state_transitions)
    
    # Set the initial state of the transition system
    ts.set_intial_state(state_name='s_1')
    
    # Print transition system information for verification
    ts.print_info()
    
    # Return the created transition system
    return ts
    
def generate_multiset(k: int, transition_system: SATransitionSystem) -> dict:
    """
    Generates a multiset as a dictionary where keys are state names of the transition system,
    and values are random integers ranging from 0 to k.

    Parameters:
    ----------
    k : int
        The upper bound (inclusive) for the random integers.
    transition_system : SATransitionSystem
        The transition system from which to get state names.

    Returns:
    -------
    dict
        A dictionary with state names as keys and random integers as values.
    """
    state_names = transition_system.get_state_names()
    multiset = {key: random.randint(0, k) for key in state_names}
    return multiset
    
def get_excitation_set_by_event(event_name: str, transition_system: SATransitionSystem) -> Union[Dict[str, int],None]:
    """
    Retrieves the set of state names where the given event is enabled.

    Parameters:
    ----------
    event_name : str
        The name of the event to check.
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    Union[set, None]
        A set of states where the given event is enabled, or None if the event is not defined.
    """
    try:
        # Check if event exists in the transition system
        if event_name in transition_system.get_event_names():
            
            excitation_set = {}
            keys = transition_system.get_state_names()
            for k in keys:
                excitation_set[k] = 0
            # Iterate through all state transitions and add the source state to the excitation set
            # if the event matches the given event name
            state_transitions = transition_system.get_all_state_transitions()
            
            for st in state_transitions:
                if st[1] == event_name:
                    excitation_set[st[0]] = 1                    
                    
            return dict(sorted(excitation_set.items()))
        else:
            raise ValueError(f'Warning: event "{event_name}" not defined!')
    except ValueError as e:
        print(e.args[0])
        return None
    
    
def get_excitation_sets(transition_system: SATransitionSystem) -> dict:
    """
    Retrieves the excitation sets for each event in a transition system.

    An excitation set for an event is the set of states where the event is enabled.

    Parameters:
    ----------
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    dict
        A dictionary where keys are event names and values are sets of states 
        where each event is enabled.
    """
    excitation_sets = {} # Initialize an empty dictionary to store excitation sets
    events = transition_system.get_event_names() # get all the event names in the transition system
    
    for e in events:
        excitation_sets[e] = get_excitation_set_by_event(event_name=e, transition_system=transition_system)
        
    return excitation_sets # Return the dictionary of excitation sets


def get_switching_set_by_event(event_name: str, transition_system: SATransitionSystem) -> Union[Dict[str, int], None]:
    """
    Retrieves the set of target states where the given event leads to a transition.

    Parameters:
    ----------
    event_name : str
        The name of the event to check.
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    set
        A set of target states where the given event leads to a transition, or None if the event is not defined.
    """
    try:
        # Check if event exists in the transition system
        if event_name in transition_system.get_event_names():
            
            switching_set = {}
            keys = transition_system.get_state_names()
            for k in keys:
                switching_set[k] = 0
            # Iterate through all state transitions and add the source state to the excitation set
            # if the event matches the given event name
            state_transitions = transition_system.get_all_state_transitions()
            
            for st in state_transitions:
                if st[1] == event_name:
                    switching_set[st[2]] = 1
                    
            return dict(sorted(switching_set.items()))
        else:
            raise ValueError(f'Warning: event "{event_name}" not defined!')
    except ValueError as e:
        # Print the error message and return None if the event is not defined
        print(e.args[0])
        return None
    

def get_switching_sets(transition_system: SATransitionSystem) -> dict:
    """
    Retrieves the switching sets for each event in a transition system.

    A switching set for an event is the set of target states where the event leads to a transition.

    Parameters:
    ----------
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    dict
        A dictionary where keys are event names and values are sets of target states
        where each event leads to a transition.
    """
    switching_sets = {} # Initialize an empty dictionary to store switching sets
    events = transition_system.get_event_names() # get all the event names in the transition system
    
    # Iterate through each event and get its switching set
    for e in events:
        switching_sets[e] = get_switching_set_by_event(event_name=e, transition_system=transition_system)
        
    return switching_sets # Return the dictionary of switching sets
    

#     def is_preregion(event_name: str, multiset: dict, transition_system: SATransitionSystem) -> bool:
#         pass


def is_valid_multiset(multiset: dict, transition_system: SATransitionSystem) -> bool:
    """
    Checks if a given multiset is valid with respect to the state names in the transition system.

    A valid multiset has keys that match exactly the set of state names in the transition system.

    Parameters:
    ----------
    multiset : dict
        A dictionary representing the multiset, where keys are state names.
    transition_system : SATransitionSystem
        The transition system containing the states.

    Returns:
    -------
    bool
        True if the multiset is valid (keys match the state names in the transition system), otherwise False.
    """
    # Get the set of state names from the multiset keys
    states = set(multiset.keys())
    
    # Return True if the state names in the multiset match the state names in the transition system,
    # otherwise False
    return states == transition_system.get_state_names()

    
def get_support_of_region(multiset: dict) -> list:
    """
    Retrieves the supports of a multiset.

    Supports are the elements of the multiset whose multiplicity is larger than zero.

    Parameters:
    ----------
    multiset : dict
        A dictionary representing the multiset, where keys are elements and values are their multiplicities.

    Returns:
    -------
    list
        A list of elements whose multiplicity is larger than zero.
    """
    # Iterate through the multiset and collect keys with values greater than zero
    supports = [key for key, value in multiset.items() if value > 0]
    return supports


def get_power_of_multiset(multiset: dict) -> int:
    """
    Retrieves the power of a multiset.

    The power of a multiset is defined as the maximum multiplicity among its elements.

    Parameters:
    ----------
    multiset : dict
        A dictionary representing the multiset, where keys are elements and values are their multiplicities.

    Returns:
    -------
    int
        The maximum multiplicity among the elements of the multiset.
    """
    # Get the list of multiplicities from the multiset
    values = list(multiset.values())
    
    # Return the maximum value among the multiplicities
    return max(values)


def get_k_topset(k: int, multiset: dict) -> dict:
    """
    Retrieves a modified version of the multiset where elements with multiplicity less than k are set to zero.

    Parameters:
    ----------
    k : int
        The threshold value for the multiplicity.
    multiset : dict
        A dictionary representing the multiset, where keys are elements and values are their multiplicities.

    Returns:
    -------
    dict
        A modified dictionary where elements with multiplicity less than k have their values set to zero.
    """
    # Create a copy of the multiset to avoid modifying the original dictionary
    temp = copy(multiset)
    for key in list(temp.keys()):
        if temp.get(key) < k: 
            # if the value is smaller than k, set it to 0
            temp[key] = 0
    return temp
    
def get_gradient_of_event(event_name: str, multiset: dict, transition_system: SATransitionSystem) -> list:
    """
    Computes the gradients for a specific event in a transition system based on the given multiset.

    The gradient for an event is calculated as the difference in multiplicity between
    the target state and the source state for each transition involving the event.

    Parameters:
    ----------
    event_name : str
        The name of the event to compute the gradients for.
    multiset : Dict[str, int]
        A dictionary representing the multiset, where keys are state names and values are their multiplicities.
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    list
        A list of gradients for the specified event.
    """
    # Initialize an empty list to store the gradients
    gradients = []
    # Get all state transitions from the transition system
    state_transitions = transition_system.get_all_state_transitions() 
    # print(state_transitions)
    # print(event_name)
    # Iterate through each state transition
    for st in state_transitions:
        if st[1] == event_name: # Check if the event name matches
            # Compute the gradient as the difference in multiplicity between the target and source states
            g = multiset.get(st[2]) - multiset.get(st[0])
            gradients.append(g) # Add the gradient to the list
            
    # Return the set of gradients
    return gradients

def get_gradients_for_multisets(multiset: Dict[str, int], transition_system: SATransitionSystem) -> Dict[str, set]:
    """
    Computes the gradients for all events in a transition system based on the given multiset.

    Parameters:
    ----------
    multiset : Dict[str, int]
        A dictionary representing the multiset, where keys are elements and values are their multiplicities.
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    Dict[str, float]
        A dictionary where keys are event names and values are the computed gradients for each event.
    """
    # Get all the event names in the transition system
    events = transition_system.get_event_names()
    
    # Initialize an empty dictionary to store the gradients
    gradients = {}
    
    # Compute the gradient for each event and store it in the dictionary
    for e in events:
        grad = get_gradient_of_event(e, multiset=multiset, transition_system=transition_system)
        gradients[e] = grad
    return gradients
    

def is_subset(multiset_a, multiset_b):
    """
    Checks if multiset_a is a subset of multiset_b.

    A multiset_a is a subset of multiset_b if all elements in multiset_a have a multiplicity
    that is less than or equal to the corresponding elements in multiset_b.

    Parameters:
    ----------
    multiset_a : dict
        The first multiset represented as a dictionary where keys are elements and values are their multiplicities.
    multiset_b : dict
        The second multiset represented as a dictionary where keys are elements and values are their multiplicities.

    Returns:
    -------
    bool
        True if multiset_a is a subset of multiset_b, otherwise False.

    Raises:
    ------
    ValueError
        If the keys of the multisets do not match.
    """
    try:
        # Check if both multisets have the same keys
        if not multiset_a.keys() == multiset_b.keys():
            raise ValueError('Warning: input multisets mismatch!')
        
        # Check if all elements in multiset_a have multiplicity less than or equal to corresponding elements in multiset_b
        for item in list(multiset_a.items()):
            k, v = item
            if not v <= multiset_b.get(k):
                return False
        return True
    except ValueError as e:
        print(f'{e.args[0]}')
        return False


def is_multiset_k_bounded(k: int, multiset: Dict[str, int]) -> bool:
    """
    Checks if all multiplicities in the multiset are less than or equal to a given bound k.

    Parameters:
    ----------
    k : int
        The upper bound for the multiplicities.
    multiset : Dict[str, int]
        A dictionary representing the multiset, where keys are elements and values are their multiplicities.

    Returns:
    -------
    bool
        True if all multiplicities are less than or equal to k, otherwise False.
    """
    # Iterate through the multiset and check if each multiplicity is less than or equal to k
    for key in multiset.keys():
        if not multiset[key] <= k:
            return False
    return True
    

def get_union_of_multisets(multiset_a: Dict[str, int], multiset_b: Dict[str, int]) -> Union[Dict[str, int], None]:
    """
    Computes the union of two multisets.

    The union of two multisets is a multiset where the multiplicity of each element
    is the maximum of its multiplicities in the two input multisets.

    Parameters:
    ----------
    multiset_a : dict
        The first multiset, where keys are elements and values are their multiplicities.
    multiset_b : dict
        The second multiset, where keys are elements and values are their multiplicities.

    Returns:
    -------
    dict or None
        A dictionary representing the union of the two multisets if their keys match, otherwise None.

    Raises:
    ------
    ValueError
        If the keys of the two multisets do not match.
    """
    try:
        # Check if the keys of the two multisets match
        if not multiset_a.keys() == multiset_b.keys():
            raise ValueError(f'Multiset mismatch')
        
        # Initialize an empty dictionary to store the union of the multisets
        union_of_multisets = {}
        keys = multiset_a.keys()
        
        # Compute the union of the multisets by taking the maximum multiplicity for each key
        for k in keys:
            union_of_multisets[k] = max([multiset_a[k], multiset_b[k]])
        
        return union_of_multisets
    except ValueError as e:
        # Print a warning message if the keys of the multisets do not match
        print(f"Warning: {e.args[0]}")
        return None


def get_intersection_of_multisets(multiset_a: Dict[str, int], multiset_b: Dict[str, int]) -> Union[Dict[str, int], None]:
    """
    Computes the intersection of two multisets.

    The intersection of two multisets is a multiset where the multiplicity of each element
    is the minimum of its multiplicities in the two input multisets.

    Parameters:
    ----------
    multiset_a : dict
        The first multiset, where keys are elements and values are their multiplicities.
    multiset_b : dict
        The second multiset, where keys are elements and values are their multiplicities.

    Returns:
    -------
    dict or None
        A dictionary representing the intersection of the two multisets if their keys match, otherwise None.

    Raises:
    ------
    ValueError
        If the keys of the two multisets do not match.
    """
    try:
        # Check if the keys of the two multisets match
        if not multiset_a.keys() == multiset_b.keys():
            raise ValueError("Multisets mismatch!")
        
        # Initialize an empty dictionary to store the intersection of the multisets
        intersetction_of_multisets = {}
        keys = multiset_a.keys()
        
        # Compute the intersection of the multisets by taking the minimum multiplicity for each key
        for k in keys:
            intersetction_of_multisets[k] = min([multiset_a[k], multiset_b[k]])

        return intersetction_of_multisets
    except ValueError as e:
        print(f"Warning: {e.args[0]}")
        return None


def get_difference_of_multisets(multiset_a: Dict[str, int], multiset_b: Dict[str, int]) -> Union[Dict[str, int], None]:
    """
    Computes the difference of two multisets.

    The difference of two multisets is a multiset where the multiplicity of each element
    is the result of subtracting its multiplicity in `multiset_b` from its multiplicity in `multiset_a`,
    with a minimum value of 0.

    Parameters:
    ----------
    multiset_a : Dict[str, int]
        The first multiset, where keys are elements and values are their multiplicities.
    multiset_b : Dict[str, int]
        The second multiset, where keys are elements and values are their multiplicities.

    Returns:
    -------
    Dict[str, int] or None
        A dictionary representing the difference of the two multisets if their keys match, otherwise None.

    Raises:
    ------
    ValueError
        If the keys of the two multisets do not match.
    """
    try:
        # Check if the keys of the two multisets match
        if not multiset_a.keys() == multiset_b.keys():
            raise ValueError("Multisets mismatch!")

        # Initialize an empty dictionary to store the difference of the multisets
        difference_of_multisets = {}
        keys = multiset_a.keys()
        
        # Compute the difference of the multisets by subtracting the multiplicity in multiset_b from multiset_a
        # Ensure the result is not less than 0
        for k in keys:
            difference_of_multisets[k] = max([0, multiset_a[k] - multiset_b[k]])
        
        return difference_of_multisets
    except ValueError as e:
        # Print a warning message if the keys of the multisets do not match
        print(f"Warning: {e.args[0]}")
        return None


def is_region(multiset: Dict[str, int], transition_system: SATransitionSystem) -> bool:
    """
    Determines if a given multiset is a region in the transition system.

    A multiset is considered a region if the gradients for all events are uniform,
    meaning that for each event, the gradients are identical across all states.

    Parameters:
    ----------
    multiset : Dict[str, int]
        A dictionary representing the multiset, where keys are state names and values are their multiplicities.
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    bool
        True if the multiset is a region (gradients for all events are uniform), otherwise False.
    """
    # Get the gradients for the multiset in the transition system
    gradients = get_gradients_for_multisets(multiset=multiset, transition_system=transition_system)
    
    # Check if the gradients for each event are uniform
    for key in gradients.keys():
        if not len(set(gradients[key])) == 1:
            return False
        
    return True


def is_preregion_of_event(event_name: str, multiset: dict, transition_system: SATransitionSystem) -> bool:
    
    # get the excitation set of the event
    excitation_set_by_event = get_excitation_set_by_event(event_name=event_name, transition_system=transition_system)
    
    # check if multiset is a region of the transition system
    if is_region(multiset=multiset, transition_system=transition_system):
        # check if the excitation set is subset of the region
        if is_subset(multiset_a=excitation_set_by_event, multiset_b=multiset):
            return True
    
    return False


def is_postregion_of_event(event_name: str, multiset: dict, transition_system: SATransitionSystem) -> bool:
    
    # get the switching set of the event
    switching_set_by_event = get_switching_set_by_event(event_name=event_name, transition_system=transition_system)
    
    # check if multiset is a region
    if is_region(multiset=multiset, transition_system=transition_system):
        # check if the switching set is subset of the region
        if is_subset(multiset_a=switching_set_by_event, multiset_b=multiset):
            return True
    
    return False


def get_delta_g(g: int, multiset: dict, event_name: str, state_name: str, transition_system: SATransitionSystem) -> int:
    """
    Computes the delta_g value for a given event and state in the transition system.

    The delta_g value is calculated as the maximum of the difference between the multiplicities
    of the target state and the source state minus g, for all transitions triggered by the given event.

    Parameters:
    ----------
    g : int
        The value to be subtracted from the multiplicity difference.
    multiset : Dict[str, int]
        A dictionary representing the multiset, where keys are state names and values are their multiplicities.
    event_name : str
        The name of the event to filter transitions by.
    state_name : str
        The name of the source state.
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    int
        The computed delta_g value.
    """
    # Get all state transitions for the given event
    state_transitions_e = transition_system.get_state_transition_by_event(event_name=event_name)
    
    # Initialize a list to store the computed values
    max_values = []
    
    # Iterate through the state transitions and compute the values
    for st in state_transitions_e:
        if st[0] == state_name:
            v = multiset[st[2]] - multiset[st[0]] - g
            max_values.append(v)
    
    # If no transitions are found, return 0
    if max_values == []:
        return 0
    
    # Compute delta_g as the maximum value in the list, or 0 if the list is empty
    return max(0, max(max_values))


def get_delta_G(g: int, multiset: dict, event_name: str, state_name: str, transition_system: SATransitionSystem) -> int:
    """
    Computes the delta_G value for a given event and state in the transition system.

    The delta_G value is calculated as the maximum of the difference between the multiplicities
    of the source state and the target state plus g, for all transitions leading to the given state.

    Parameters:
    ----------
    g : int
        The value to be added to the multiplicity difference.
    multiset : Dict[str, int]
        A dictionary representing the multiset, where keys are state names and values are their multiplicities.
    event_name : str
        The name of the event to filter transitions by.
    state_name : str
        The name of the target state.
    transition_system : SATransitionSystem
        The transition system containing the events and state transitions.

    Returns:
    -------
    int
        The computed delta_G value.
    """
    # Get all state transitions for the given event
    state_transitions_e = transition_system.get_state_transition_by_event(event_name=event_name)
    # print(state_transitions_e)
    # Initialize a list to store the computed values
    max_values = []
    
    # Iterate through the state transitions and compute the values
    for st in state_transitions_e:
        if st[2] == state_name:
            v = multiset[st[0]] - multiset[st[2]] + g
            max_values.append(v)
    
    # If no transitions are found, return 0
    if max_values == []:
        return 0
    # print(f"max values for G: {max_values}")
    # Compute delta_G as the maximum value in the list, ensuring it is not less than 0
    return max(0, max(max_values))


def get_multiset_expansion_on_event_by_g(g: int, event_name: str, multiset: dict, transition_system: SATransitionSystem ):
    if not multiset.keys() == transition_system.get_state_names():
        raise ValueError
    
    multiset_expansion = {}
    for key in multiset.keys():
        multiset_expansion[key] = multiset[key] + get_delta_g(g=g, event_name=event_name, state_name=key, transition_system=transition_system, multiset=multiset)
    
    return multiset_expansion


def get_multiset_expansion_on_event_by_G(g: int, event_name: str, multiset: dict, transition_system: SATransitionSystem) -> dict:
    if not multiset.keys() == transition_system.get_state_names():
        raise ValueError
    
    multiset_expansion = {}
    for key in multiset.keys():
        multiset_expansion[key] = multiset[key] + get_delta_G(g=g, event_name=event_name, state_name=key, transition_system=transition_system, multiset=multiset)
    
    return multiset_expansion


def get_candidates(transition_system: SATransitionSystem) -> list:
    
    candidates = []
    
    excitation_sets = get_excitation_sets(transition_system=transition_system)
    switching_sets = get_switching_sets(transition_system=transition_system)
    
    for value in excitation_sets.values():
        # print(value)
        candidates.append(value)
    
    for value in switching_sets.values():
        # print(value)
        candidates.append(value)
    
    return candidates


def get_illegal_events(multiset: dict, transition_system: SATransitionSystem) -> list:
    gradients = get_gradients_for_multisets(multiset=multiset, transition_system=transition_system)
    # print(dict(sorted(gradients.items())))
    gradients = dict(sorted(gradients.items()))
    # Check if the gradients for each event are uniform
    lst = []
    for key in gradients.keys():
        if not len(set(gradients[key])) == 1:
            g_min = min(gradients[key])
            g_max = max(gradients[key])
            lst.append((key, g_min, g_max, __get_gradient_for_binary_search(g_min=g_min, g_max=g_max)))
    return lst


def is_trivial(multiset: dict) -> bool:
    values = list(multiset.values())
    return all(value >= 1 for value in values)
    

def generate_all_minimal_regions_o(k: int, transition_system: SATransitionSystem) -> List[dict]:
    """
    Generates all minimal regions for a given transition system.

    A minimal region is a multiset that satisfies the region property and cannot be further reduced
    while maintaining the property.

    Parameters:
    ----------
    k : int
        The maximum allowed power of a region.
    transition_system : SATransitionSystem
        The transition system containing the states and transitions.

    Returns:
    -------
    List[dict]
        A list of minimal regions, each represented as a dictionary.
    """
    ts = transition_system
    minimal_multisets = []      # R
    explored_multisets = []
    max_iterations = 1
    iterations = 0
    candidates = get_candidates(transition_system=transition_system)  # P
    # candidates = [{'s_0': 6, 's_1': 3, 's_2': 2, 's_3': 0, 's_4': 3, 's_5': 0, 's_6': 0}]
    # print(candidates)
    
    # while candidates and iterations < max_iterations:
    while candidates:
        # pprint(f"Number of Candidates: {len(candidates)}", width=120)
        
        candidate = candidates.pop()        # r
        explored_multisets.append(candidate)
        # candidate = {'s_0': 1, 's_1': 1, 's_2': 1, 's_3': 0, 's_4': 1, 's_5': 0, 's_6': 0}
        # print(f"candidate: {list(candidate.values())}")
        
        if candidate in minimal_multisets:
            print("****** candidate already in minimal_multisets...")
        else:
            minimal_multisets.append(candidate)
            
            # Check if the candidate is a valid region
            if is_region(multiset=candidate, transition_system=ts):
                print("Candidate is a region. Expansion is not necessary")
            else:
                # print("Candidate is not a region. Expansion starts...")
                # Get the event with a non-constant gradient
                lst_non_constant_events = get_illegal_events(multiset=candidate, transition_system=ts)
                # pprint(f"Illegal Events:{lst_non_constant_events}")
                
                # for e in lst_non_constant_events:
                event_name, g_min, g_max, g_e = __get_event_gradient_for_expansion(lst_non_constant_events)
                # print(f"Chosen Event: {event_name}, g_min: {g_min}, g_max: {g_max}, g_e: {g_e}")

                r_1 = get_multiset_expansion_on_event_by_g(g=g_e, event_name=event_name, multiset=candidate, transition_system=ts)
                # print(f"r_1: {list(r_1.values())}")
                if get_power_of_multiset(r_1) <= k and not is_trivial(r_1):
                    # print("r_1 is a valid candidate, add to the candidates...")
                    candidates.append(r_1)
                else:
                    explored_multisets.append(r_1)
                    # print("r_1 is not valid.")
                
                r_2 = get_multiset_expansion_on_event_by_G(g=int(g_e+1), event_name=event_name, multiset=candidate, transition_system=ts)
                # print(f"r_2: {list(r_2.values())}")
                if get_power_of_multiset(r_2) <= k and not is_trivial(r_2):
                    # print("r_2 is a valid candidate, add to the candidates...")
                    candidates.append(r_2)
                else:
                    explored_multisets.append(r_2)
                    # print("r_2 is not valid.")
        
        iterations += 1
        print(f"****************** {iterations} *********************")
    
    print(f"Found Minimal Multisets: ")
    for m in minimal_multisets:
        print(list(m.values()))
    
    minimal_regions = []
    temp = []
    # remove multisets that are not regions                
    for ms in minimal_multisets:
        if is_region(multiset=ms, transition_system=ts):
            temp.append(ms)
        iterations += 1
    
    print(f"Temp: ")
    for t in temp:
        print(list(t.values()))
    
    # make a copy of minimal_multisets
    copy_minimal_multisets = copy(temp)
    
    # Remove non-minimal regions
    for ms in temp:
        l_filtered = [e for e in copy_minimal_multisets if e != ms]
        if not __has_subset_of_list(multiset=ms, lst_of_multisets=l_filtered):
            print(f"{ms.values()} does not have subset")
            minimal_regions.append(ms)
        else:
            print(f"{ms.values()} has subsets")
        iterations += 1
    
    print(f"Number of Iterations: {iterations}")
    return minimal_regions, explored_multisets, iterations


def generate_all_minimal_regions_v1(k: int, transition_system: SATransitionSystem):
    """
    Generates all minimal regions for a given transition system.

    A minimal region is a multiset that satisfies the region property and cannot be further reduced
    while maintaining the property.

    Parameters:
    ----------
    k : int
        The maximum allowed power of a region.
    transition_system : SATransitionSystem
        The transition system containing the states and transitions.

    Returns:
    -------
    List[dict]
        A list of minimal regions, each represented as a dictionary.
    """
    ts = transition_system
    int_k = k
    
    discovered_minimal_regions = []     # R
    explored_multisets = []             # M

    candidates = get_candidates(transition_system=ts)    # P

    # remove duplicates
    candidates = __remove_duplicates(list_of_multisets=candidates)

    # # remove supersets
    candidates = __remove_supersets(list_of_multisets=candidates)

    
    iterations = 0
    
    while candidates:
        print("****************")
        print(f"Iteration: {iterations}")
        print(f"Num Candidates: {len(candidates)}")
        
        l_candidates = [list(c.values()) for c in candidates]
        idx = min(range(len(l_candidates)), key=lambda i: sum(l_candidates[i]))
        
        r_tilde = candidates.pop(idx)
        print(f"candidate: {list(r_tilde.values())}")
        
        if is_region(multiset=r_tilde, transition_system=ts):
            if not r_tilde in discovered_minimal_regions:
                print("Candidate is a region, add to the list.")
                discovered_minimal_regions.append(r_tilde)
                explored_multisets.append(r_tilde)
                iterations = iterations + 1
            else:
                print("Candidate is a region, already exists.")
                iterations = iterations + 1
        else:
            discovered_minimal_regions, explored_multisets, niter = multiset_expansion(k=int_k, multiset=r_tilde, niter=iterations, discovered_minimal_regions=discovered_minimal_regions, explored_multisets=explored_multisets, transition_system=ts)
            
            print(f"len l_r: {len(discovered_minimal_regions)}")
            print(f"len l_m: {len(explored_multisets)}")
            print(f"niter: {niter}")

            iterations = niter
    
    # make a copy of minimal_multisets
    copy_discovered_minimal_regions = copy(discovered_minimal_regions)
    temp = []
    
    # Remove non-minimal regions
    for ms in discovered_minimal_regions:
        l_filtered = [e for e in copy_discovered_minimal_regions if e != ms]
        if not __has_subset_of_list(multiset=ms, lst_of_multisets=l_filtered):
            print(f"{ms.values()} does not have subset")
            temp.append(ms)
        else:
            print(f"{ms.values()} has subsets")
        iterations += 1
    
    discovered_minimal_regions = __remove_duplicates(list_of_multisets=temp)
     
    print(f"Number of Discovered Minimal Regions: {len(discovered_minimal_regions)}")
    print(f"Number of Explored Multisets: {len(explored_multisets)}")    
    return discovered_minimal_regions, explored_multisets, iterations


def multiset_expansion(k: int, multiset: dict, niter: int, transition_system: SATransitionSystem, discovered_minimal_regions:list, explored_multisets: list):
    
    # local variables
    int_k = k
    r = [multiset]
    ts = transition_system
    discovered = copy(discovered_minimal_regions)
    explored = copy(explored_multisets)
    
    while r:
        # get the element with the max. cardinality as the candidate
        l_r = [list(i.values()) for i in r]
        idx = max(range(len(l_r)), key=lambda i: sum(l_r[i]))
        r_hat = r.pop(idx)
        print("*"*20)
        print(f"Number of Iteration: {niter}")
        print(f"Chosen Candidate: {list(r_hat.values())}")
        
        if  list(r_hat.values()) in explored:
            print("Already explored. Jump to next.")
            niter += 1
            continue
        
        explored.append(list(r_hat.values()))
        
        # Get the event with a non-constant gradient
        lst_non_constant_events = get_illegal_events(multiset=r_hat, transition_system=ts)
        pprint(f"Illegal Events:{lst_non_constant_events}")
        
        # for e in lst_non_constant_events:
        event_name, g_min, g_max, g_e = __get_event_gradient_for_expansion(lst_non_constant_events)
        print(f"Chosen Event: {event_name}, g_min: {g_min}, g_max: {g_max}, g_e: {g_e}")
        
        # Expand the multiset based on the chosen illegal event and g
        r_1 = get_multiset_expansion_on_event_by_g(g=g_e, event_name=event_name, multiset=r_hat, transition_system=ts)
        print(f"r_1: {list(r_1.values())}")
        
        r_2 = get_multiset_expansion_on_event_by_G(g=int(g_e+1), event_name=event_name, multiset=r_hat, transition_system=ts)
        print(f"r_2: {list(r_2.values())}")
        
        
        
        for i in [r_1, r_2]:
            if list(i.values()) in explored:
                continue
            else:
                if __is_valid_candidate(k=int_k, multiset=i):
                    if is_region(multiset=i, transition_system=ts):
                        discovered.append(i)
                        explored.append(list(i.values()))
                        continue
                    r.append(i)
                else:
                    explored.append(list(i.values()))
                    
        niter += 1      
    return discovered, explored, niter


def __remove_duplicates(list_of_multisets: list):
    seen = set()
    unique_dicts = []
    
    for d in list_of_multisets:
        # Convert dictionary to a sorted tuple of items
        t = tuple(sorted(d.items()))
        # Check if the tuple is not in the seen set
        if t not in seen:
            seen.add(t)
            unique_dicts.append(d)
    
    # The list of dictionaries with duplicates removed
    return unique_dicts

def __remove_supersets(list_of_multisets: list):
    temp = []
    
    for m in list_of_multisets:
        l_filtered = [e for e in list_of_multisets if e != m]
        if not __has_subset_of_list(multiset=m, lst_of_multisets=l_filtered):
            temp.append(m)  
    return temp    
    

def __is_minimal_region(k: int, multiset: dict, minimal_regions: list) -> bool:
    if __is_valid_candidate(k=k, multiset=multiset):
        if not multiset in minimal_regions:
            if not __has_subset_of_list(multiset=multiset, lst_of_multisets=minimal_regions):
                return True
    return False


def __is_valid_candidate(k: int, multiset: dict) -> bool:
    return get_power_of_multiset(multiset=multiset) <= k and not is_trivial(multiset=multiset)

def __get_event_gradient_for_expansion(tuples_list):
    """
    Returns the tuple with the maximal absolute value of the fourth element.

    If multiple tuples have the same maximal absolute value, the first encountered is returned.

    Parameters:
    ----------
    tuples_list : list of tuples
        The list of tuples to search through.

    Returns:
    -------
    tuple
        The tuple with the maximal absolute value of the fourth element.
    """
    return max(tuples_list, key=lambda x: abs(x[3]))


def __get_gradient_for_binary_search(g_min: int, g_max: int):
    return int(math.floor((g_min+g_max)/2))

def __remove_duplicates_from_list(lst: list, target) -> list:
    return [d for d in lst if not all(d.get(k) == v for k, v in target.items())]


def __has_subset_of_list(multiset: dict, lst_of_multisets: list) -> bool:
    for m in lst_of_multisets:
        if is_subset(multiset_a=m, multiset_b=multiset):
            return True
    return False
#     def __gen_candidates(self, given_set):
#         # Convert the set to a list for easier manipulation
#         s = list(given_set)
#         # Use chain and combinations from itertools to generate all possible combinations of the set elements
#         power_set = [set(subset) for subset in chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))]
#         list_of_candidates = power_set[1:len(power_set)-1]
#         return list_of_candidates


#     def find_nontrivial_regions(self):
#         """
#         Finds all nontrivial regions in a state graph.
        
#         Args:
#         - state_graph: A dictionary representing the state graph
        
#         Returns:
#         - A list of sets, where each set is a nontrivial region.
#         """
#         print(f'**********find_nontrivial_regions************')
#         state_graph = self.generate_ts_dict()
        
#         # nodes = list(state_graph.keys())  # Extract all nodes
#         #all_labels = set(label for transitions in state_graph.values() for label, _ in transitions)  # Extract all labels
#         nodes = state_graph['states']
#         all_labels = state_graph['activities']
#         state_transitions = state_graph['state_transitions']
#         e_labelled_arcs = {}
#         for label in all_labels:
#             e_labelled_arcs[label] = [st for st in state_transitions if label in st]
            
#         def is_region(candidate):
#             # print(f'\ncandidate: {candidate}')
#             flag = 1
            
#             for label in all_labels:
#                 # get e-labelled arcs
#                 # print(f'label: {label}')
#                 arcs = list(e_labelled_arcs[label])
#                 # print(f'arcs: {arcs}')
#                 input_nodes = {a[0] for a in arcs}
#                 output_nodes = {a[2] for a in arcs}
#                 nodes = [(a[0], a[2]) for a in arcs]
                
#                 test = nodes[0]
                
#                 if set(test) <= candidate or set(test)&candidate == set():
#                     for n in nodes[1:]:
#                         if set(n)&candidate:
#                             if set(n) != set(n)&candidate:
#                                 flag = flag*0
#                                 return flag
                
                        
#                 if (test[0] in candidate) and (not test[1] in candidate):
#                     if not input_nodes <= candidate:
#                         flag = flag*0
#                         return flag
                    
#                     if not output_nodes&candidate == set():
#                         flag = flag*0
#                         return flag
                
#                 if (not test[0] in candidate) and (test[1] in candidate):
#                     if not input_nodes&candidate == set():
#                         flag = flag*0
#                         return flag
                    
#                     if not output_nodes <= candidate:
#                         flag = flag*0
#                         return flag
            
#             # Generate all possible nontrivial subsets of nodes
#             nontrivial_regions = []
#             list_of_candidates = self.__gen_candidates(nodes)
#             for candidate in list_of_candidates:
#                 # print("candidate: ")
#                 # print(candidate)
#                 if is_region(candidate):
#                     nontrivial_regions.append(candidate)
                        
#             return nontrivial_regions
    