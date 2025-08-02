from base.alphabet import VPAlphabet, StackAlphabet, bottom_symbol
from base.state import VPAState, VPATransitions
from base.vpl import VPL

class VPA(VPL):
    def __init__(self, alphabet: VPAlphabet, states: set[VPAState], 
                 initial_state: VPAState, final_states: set[VPAState],
                 transitions: VPATransitions, stack_alphabet: StackAlphabet = None):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions
        self.stack_alphabet = stack_alphabet if stack_alphabet \
                                else StackAlphabet(alphabet.get_push_symbols())
        self.stack = []

    def _push_symbol(self, symbol: str):
        """Push a symbol onto the stack."""

        self.stack.append(symbol)
    
    def _pop_symbol(self) -> str:
        """Pop a symbol from the stack."""

        if not self.stack:
            return bottom_symbol
        
        return self.stack.pop()
    
    def _get_top_symbol(self) -> str:
        """Get the top symbol from the stack without popping it."""

        return self.stack[-1]
    
    def process_sequence(self, sequence: str) -> bool:
        """
        Process a sequence of symbols and determine if it is accepted by the VPA.
        """

        current_state = self.initial_state
        for symbol in sequence:
            if symbol in self.alphabet.get_push_symbols():
                push_symbol = self.stack_alphabet.get_push_symbol(symbol)
                if not push_symbol:
                    return False
                self._push_symbol(push_symbol)
                current_state = self.transitions.get_push_next_state(current_state, symbol, push_symbol)
            elif symbol in self.alphabet.get_pop_symbols():
                current_state, pop_symbol = self.transitions.get_pull_transition(current_state, symbol)
                if self._get_top_symbol() != self.stack_alphabet(pop_symbol):
                    return False
                self._pop_symbol()
            elif symbol in self.alphabet.get_int_symbols():
                current_state = self.transitions.get_internal_next_state(current_state, symbol)
            else:
                return False
        return current_state in self.final_states

def most_permossive(alphabet):
    """
    Create a most permissive VPA with the given alphabet.
    """

    # Create a new VPA with the given alphabet
    states = {VPAState("q0")}
    initial_state = VPAState("q0")
    final_states = {VPAState("qf")}
    transitions = VPATransitions()

    # Add transitions for each symbol in the alphabet
    for symbol in sigma:
        transitions.add_transition(initial_state, symbol, final_states)

    # Create the VPA