from tree_automata.tree_automata import TreeAutomata, TreeAutomataState, TreeAutomataTransitionKey
from base.tree import Tree, TreeSymbol, empty_symbol
from base.alphabet import RankedAlphabet
from tree_automata.tree_comparator import TreeComparator

q0 = TreeAutomataState('q0')
q1 = TreeAutomataState('q1') 
q2 = TreeAutomataState('q2')

states = {
        q0,
        q1,
        q2    
    }

a = TreeSymbol('a', 2)
b = TreeSymbol('b', 0)
c = TreeSymbol('c', 0)
alphabet = RankedAlphabet({a, b, c}, "RankedAlphabet({a, b, c})")

final_states = {q0}

b_key = TreeAutomataTransitionKey(b, [])
c_key = TreeAutomataTransitionKey(c, [])
a_key = TreeAutomataTransitionKey(a, [q1, q2])
transitions = {
    b_key: q1,
    c_key: q2,
    a_key: q0,
}

simple_tree_automaton = TreeAutomata(states, alphabet, final_states, transitions)

# Representa el árbol con 'a' como raíz y 'b', 'c' como hojas
correct_tree_example = Tree(a, [Tree(b, []), Tree(c, [])])

is_accepted = simple_tree_automaton.is_accepted(correct_tree_example)
#print(f"Correct tree example accepted: {is_accepted}")

# Representa el árbol con 'a' como raíz y 'c', 'c' como hojas
incorrect_tree_example = Tree(a, [Tree(c, []), Tree(c, [])])

is_accepted = simple_tree_automaton.is_accepted(incorrect_tree_example)
#print(f"Incorrect tree example accepted: {is_accepted}")


new_transitions = {
    b_key: q2,
    c_key: q2,
    a_key: q2,
}
tree_automaton2 = TreeAutomata(states, alphabet, {q2}, transitions)
tree_comparator = TreeComparator(simple_tree_automaton)

equivalence, counterexample = tree_comparator.equivalence_query(simple_tree_automaton)
#print(f"Equivalence: {equivalence}, counterexample: {counterexample}")

equivalence, counterexample = tree_comparator.equivalence_query(tree_automaton2)
#print(f"Equivalence: {equivalence}, counterexample: {counterexample}")

a = TreeSymbol('a', 2)
b = TreeSymbol('b', 2)
epsilon = empty_symbol
alphabet = RankedAlphabet({a, b, epsilon}, "RankedAlphabet({a, b, epsilon})")

qe = TreeAutomataState('q_eps')
qa = TreeAutomataState('qa') 
qb = TreeAutomataState('qb')
qab = TreeAutomataState('qab')

states = {qa, qb, qab, qe}

final_states = {qe, qa, qb, qab}

eps_key = TreeAutomataTransitionKey(epsilon, [])

a_ee_key = TreeAutomataTransitionKey(a, [qe, qe])
a_ea_key = TreeAutomataTransitionKey(a, [qe, qa])
a_ae_key = TreeAutomataTransitionKey(a, [qa, qe])
a_aa_key = TreeAutomataTransitionKey(a, [qa, qa])

a_ab_key = TreeAutomataTransitionKey(a, [qa, qb])
a_eb_key = TreeAutomataTransitionKey(a, [qe, qb])
a_aab_key = TreeAutomataTransitionKey(a, [qa, qab])
a_eab_key = TreeAutomataTransitionKey(a, [qe, qab])

a_ba_key = TreeAutomataTransitionKey(a, [qb, qa])
a_aba_key = TreeAutomataTransitionKey(a, [qab, qa])
a_be_key = TreeAutomataTransitionKey(a, [qb, qe])
a_abe_key = TreeAutomataTransitionKey(a, [qab, qe])

b_bb_key = TreeAutomataTransitionKey(b, [qb, qb])
b_be_key = TreeAutomataTransitionKey(b, [qb, qe])
b_eb_key = TreeAutomataTransitionKey(b, [qe, qb])
b_ee_key = TreeAutomataTransitionKey(b, [qe, qe])

new_transitions = {
    eps_key: qe,
    a_ee_key: qa,
    a_ea_key: qa,
    a_ae_key: qa,
    a_aa_key: qa,

    a_ab_key: qab,
    a_eb_key: qab,
    a_aab_key: qab,
    a_eab_key: qab,
    a_ba_key: qab,
    a_aba_key: qab,
    a_be_key: qab,
    a_abe_key: qab,

    b_bb_key: qb,
    b_be_key: qb,
    b_eb_key: qb,
    b_ee_key: qb,
}

tree1 = Tree(a, 
            [Tree(b, [
                Tree(epsilon, []), 
                Tree(epsilon, [])]), 
            Tree(a, [
                Tree(a, [
                    Tree(epsilon, []),
                    Tree(epsilon, [])]),
                Tree(a, [
                    Tree(b, [
                        Tree(b, [
                            Tree(epsilon, []),
                            Tree(epsilon, [])]),
                        Tree(epsilon, [])]),
                    Tree(epsilon, [])])])])

tree2 = Tree(a, 
            [Tree(a, [
                Tree(epsilon, []), 
                Tree(epsilon, [])]), #qa 
            Tree(b, [
                Tree(epsilon, []),
                Tree(epsilon, [])
                ])
            ])

tree3 = Tree(epsilon, [])

tree_automaton = TreeAutomata(states, alphabet, final_states, new_transitions)
is_accepted = tree_automaton.is_accepted(tree1)

def run_example():
    print("RUNNING TREE AUTOMATA EXAMPLE...")
    print("Tree Automaton:", tree_automaton)
    print("-"*20)

    print("Tree1:", tree1)
    print("Tree1 accepted:", tree_automaton.is_accepted(tree1))
    print("-"*20)

    print("Tree2:", tree2)
    print("Tree2 accepted:", tree_automaton.is_accepted(tree2))
    print("-"*20)

    print("Tree3:", tree3)
    print("Tree3 accepted:", tree_automaton.is_accepted(tree3))