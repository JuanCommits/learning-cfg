from base.vpl import VPL
from tree_automata.tree_automata import TreeAutomata
from utils.well_formed import is_well_formed
from base.alphabet import VPAlphabet

from utils.encoding import sequence_2_tree

class TreeAutomataVPL(VPL):
    def __init__(self, alphabet: VPAlphabet, tree_automaton: TreeAutomata):
        super().__init__(alphabet)
        self.tree_automaton = tree_automaton

    def is_accepted(self, sequence: str) -> bool:
        """
        Check if the sequence corresponds to an accepted tree structure.
        """

        # Check if the sequence is well-formed
        if not is_well_formed(sequence, self.get_alphabet()):
            return False

        tree = sequence_2_tree(sequence, self.get_alphabet())
        return self.tree_automaton.is_accepted(tree)


def nta_2_vpg(nta, alphabet: VPAlphabet) -> TreeAutomataVPL:
    return TreeAutomataVPL(alphabet, nta)