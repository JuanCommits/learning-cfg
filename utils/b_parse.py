from tree_automata.tree_automata import (
    TreeAutomata,
    TreeAutomataState,
    TreeAutomataTransitionKey,
    TreeSymbol
)
from base.tree import empty_symbol
from base.alphabet import VPAlphabet
from utils.encoding import vpalphabet_2_ranked


def get_t_b_parse(alphabet: VPAlphabet) -> TreeAutomata:
    """
    Given a VPG alphabet returns T(B_parse) this is the tree automata that accepts a tree iif
        the mapped sequence is accepted by the most permissive VPG.

    VPG: G_Σ = ({S}, S, →) with set of rules {S → ε} U {S → cS | c ∈ Σint} U {S → aSbS | a ∈ Σ_push and b ∈ Σ_pop}.
    """

    s_state = TreeAutomataState("S")
    pop_state = TreeAutomataState("PopState")
    transitions = {}
    ranked_alphabet = vpalphabet_2_ranked(alphabet)

    # Add epsilon transition
    epsilon_transition_key = TreeAutomataTransitionKey(
        empty_symbol,
        []
    )
    transitions[epsilon_transition_key] = s_state

    for push_symbol in alphabet.get_push_symbols():
        for pop_symbol in alphabet.get_pop_symbols():

            # Add the pop transition (just an intermediate transition to PopState)
            #   This is used to generate the pop push grammar rule.
            pop_transition_key = TreeAutomataTransitionKey(
                TreeSymbol(pop_symbol, 1),
                [s_state]
            )
            transitions[pop_transition_key] = pop_state

            # Add the push transition to the S state (balanced state)
            push_transition_key = TreeAutomataTransitionKey(
                TreeSymbol(push_symbol, 2),
                [s_state, pop_state]
            )
            transitions[push_transition_key] = s_state

    # Add all the internal symbol transitions. The internal symbols dont affect the balance.
    for int_symbol in alphabet.get_int_symbols():
        int_transition_key = TreeAutomataTransitionKey(
            TreeSymbol(int_symbol, 1),
            [s_state]
        )
        transitions[int_transition_key] = s_state
            
            
    # Create and return the result TreeAutomaton.
    return TreeAutomata(
        states={s_state},
        alphabet=ranked_alphabet,
        final_states={s_state},
        transitions=transitions
    )