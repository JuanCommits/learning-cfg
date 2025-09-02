from tree_automata.tree_automata import (
    TreeAutomata,
    TreeAutomataTransitionKey,
    TreeAutomataState
)
from base.alphabet import VPAlphabet

class VPG:

    def __init__(
        self, 
        variables: set[str],
        start_symbols: set[str], 
        rules: tuple[str, str, str],
        variable_map: dict[str, str] = {},
        name: str = "VPG"
    ):
        self.name = name
        self.variables = variables
        self.start_symbols = start_symbols
        self.variable_map = variable_map
        self.rules = rules


    def print_grammar(self):
        result = f"Grammar {self.name}\n"
        result += f"Variables: {', '.join(self.variables)}\n"
        result += f"Start Symbols: {', '.join([self.variable_map[start_symbol] for start_symbol in self.start_symbols])}\n"
        result += f"Rules:\n"
        for rule in self.rules:
            if 'q4' not in str(rule[0]):
                result += f"{rule[0]} -> {rule[1]}    # {rule[2]}\n"
        result += f"\n\nVariable Map:\n"
        for state, var in self.variable_map.items():
            result += f"{state} -> {var}\n"
        return result
    



def vpg_from_tree_automata(tree_automata: TreeAutomata, alphabet: VPAlphabet) -> VPG:
    start_symbols = {state.name for state in tree_automata.final_states}
    variable_map = {
        state.name:f"q{i}" for i, state in enumerate(list(tree_automata.states))
    }
    variables = {variable_map[state.name] for state in tree_automata.states}

    rules = []
    # Create epsilon rules
    for transition_key, transition_state in tree_automata.transitions.items():
        # q → ε for all q ∈ δ(ε());
        if transition_key.is_epsilon():
            rules.append(
                _process_epsilon_rule(
                    transition_key,
                    transition_state,
                    variable_map
                )
            )
        # q' → cq for all c ∈ Σint, q ∈ Q, and q' ∈ δ(c(q));
        elif transition_key.symbol.value in alphabet.get_int_symbols():
            rules.append(
                _process_internal_rule(
                    transition_key,
                    transition_state,
                    variable_map
                )
            )
        # q^ → apbq for all a ∈ Σpush, b ∈ Σpop, and p, q, q', q^ ∈ Q such that q' ∈ δ(b(q)) and q^ ∈ δ(a(p, q')).
        elif transition_key.symbol.value in alphabet.get_pop_symbols():
            rules.extend(
                _process_push_pop_rules(
                    transition_key,
                    transition_state,
                    variable_map,
                    tree_automata,
                    alphabet
                )
            )
    return VPG(
            variables=variables, 
            variable_map=variable_map,
            start_symbols=start_symbols, 
            rules=rules
        )


def _process_epsilon_rule(
    transition_key: TreeAutomataTransitionKey,
    transition_state: TreeAutomataState,
    variable_map: dict[str, str]
):
    """
    Epsilon rule definition:
    q → ε for all q ∈ δ(ε());
    """
    return (
        variable_map[transition_state.name],
        transition_key.symbol,
        "epsilon"
    )

def _process_internal_rule(
    transition_key: TreeAutomataTransitionKey,
    transition_state: TreeAutomataState,
    variable_map: dict[str, str]
) -> tuple[str, str, str]:
    """
    Internal rule definition:
    q' → cq for all c ∈ Σint, q ∈ Q, and q' ∈ δ(c(q));
    """
    assert len(transition_key.child_states) == 1, "Int symbols should have exactly one child state."
    return (
        variable_map[transition_state.name],
        f"{transition_key.symbol} {variable_map[transition_key.child_states[0].name]}",
        "internal"
    )

def _process_push_pop_rules(
    transition_key: TreeAutomataTransitionKey,
    transition_state: TreeAutomataState,
    variable_map: dict[str, str],
    tree_automata: TreeAutomata,
    alphabet: VPAlphabet
):
    """
    Push Pop rule definition:
    - q^ → apbq for all a ∈ Σpush, b ∈ Σpop, and p, q, q', q^ ∈ Q such that q' ∈ δ(b(q)) and q^ ∈ δ(a(p, q')).
    """
    assert len(transition_key.child_states) == 1, "Pop symbols should have exactly one child state."

    push_pop_rules = []
    # We found - b.  -   q' ∈ δ(b(q))
    b = transition_key.symbol
    # q is the only child of the transition
    q = variable_map[transition_key.child_states[0].name]
    # q' is the reaching state of b
    q_prime = transition_state
    
    # Now that we have b, let's search for an a.  -   q^ ∈ δ(a(p, q'))
    for transition_key2, transition_state2 in tree_automata.transitions.items():
        if transition_key2.symbol.value in alphabet.get_push_symbols():
            assert len(transition_key2.child_states) == 2, "Push symbols should have exactly two child states."
            # We found - a.   -   q^ ∈ δ(a(p, q'))
            a = transition_key2.symbol
            # q^ is the reaching state of a
            q_hat = variable_map[transition_state2.name]
            # p is the first child of the transition
            p = variable_map[transition_key2.child_states[0].name]
            # Check if q' is the second child (continuation) of a. If it is, we found a new rule
            if q_prime == transition_key2.child_states[1]:
                # Now we are certain that there is a new push rule
                # Let's build it - q^ → apbq
                push_pop_rules.append((
                    q_hat,
                    f"{a} {p} {b} {q}",
                    "push-pop"
                ))
    return push_pop_rules

