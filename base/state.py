from typing import Tuple

class VPAState:
    def __init__(self, name: str):
        self.name = name

class VPATransitions:
    def __init__(self, transition_dict: dict):
        self.transition_dict = transition_dict

    def get_transition(self, state: VPAState, symbol: str, push_symbol: str = None):
        if push_symbol:
            return self.transition_dict[state][symbol][push_symbol]
        else:
            return self.transition_dict[state][symbol]
        
    def get_push_next_state(self, state: VPAState, symbol: str, push_symbol: str) -> VPAState:
        return self.transition_dict[state][symbol][push_symbol]
    
    def get_pull_transition(self, state: VPAState, symbol: str) -> Tuple[VPAState, str]:
        return self.transition_dict[state][symbol]
    
    def get_internal_next_state(self, state: VPAState, symbol: str) -> VPAState:
        return self.transition_dict[state][symbol]
