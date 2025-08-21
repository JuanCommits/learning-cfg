from base.tree import Tree
from base.tree import TreeSymbol
from collections import deque
from base.alphabet import RankedAlphabet
from tree_automata.tree_state import TreeAutomataState, TreeAutomataTransitionKey

class TreeAutomata:
    def __init__(self, states: set[TreeAutomataState], alphabet: RankedAlphabet,
                 final_states: set[TreeAutomataState], 
                 transitions: dict[TreeAutomataTransitionKey, TreeAutomataState]):
        self.states = states
        self.alphabet = alphabet
        self.final_states = final_states
        self.transitions = transitions

    def process_tree(self, tree: Tree) -> bool:
        queue = deque()
        result = {}

        node_id = 0
        queue.append((tree, node_id))
        pending_children = {}

        while queue:
            current_node, current_id = queue.popleft()
            if current_node.is_leaf():
                result[current_id] = self.get_leaf_state(current_node)
            else:
                symbol = current_node.root
                children = current_node.children
                child_ids = []
                for child in children:
                    node_id += 1
                    child_ids.append(node_id)
                    queue.append((child, node_id))
                
                pending_children[current_id] = (symbol, child_ids)

        for node_id in sorted(pending_children.keys(), reverse=True):
            symbol, child_ids = pending_children[node_id]
            child_states = [result[child_id] for child_id in child_ids]
            transition = self.get_transition(symbol, child_states)
            result[node_id] = transition

        return result[0]

    def get_leaf_state(self, tree: Tree) -> TreeAutomataState:
        for transition_key, result_state in self.transitions.items():
            if transition_key.symbol == tree.root and transition_key.symbol.arity == 0:
                return result_state
        return None

    def get_transition(self, symbol: TreeSymbol, child_states: list[TreeAutomataState]) -> TreeAutomataState:
        for transition_key, result_state in self.transitions.items():
            if transition_key.symbol == symbol and transition_key.child_states == tuple(child_states):
                return result_state
        return None

    def is_accepted(self, tree: Tree) -> bool:
        final_state = self.process_tree(tree)
        return final_state in self.final_states
    
    def __str__(self):
        return f"TreeAutomata( \n -- states={[state.__str__() for state in self.states]} \n" \
                + f" -- final_states={[final_state.__str__() for final_state in self.final_states]} \n" \
                + f" -- transitions={[transition.__str__() for transition in self.transitions]} \n)"