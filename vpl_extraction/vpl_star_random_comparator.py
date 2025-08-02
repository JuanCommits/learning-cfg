from vpl_extraction.vpl_star_comparator import VPLStarComparator
from vpl_extraction.vpl_star_oracle import VPLStarOracle
from base.alphabet import VPAlphabet
from utils.encoding import vpalphabet_2_ranked
from tree_automata.tree_generator import TreeGenerator
from tree_automata.tree_automata import TreeAutomata

class VPLRandomComparator(VPLStarComparator):
    """
    A comparator for VPLs that uses a random sequence of symbols to compare two automata.
    """
    
    def __init__(self, alphabet: VPAlphabet, random_trees: int = 100, max_depth: int = 6):
        self.random_trees = random_trees
        self.max_depth = max_depth
        self.vpa_alphabet = alphabet
        self.generator = TreeGenerator(vpalphabet_2_ranked(alphabet))


    def get_counter_example(self, tree_automata: TreeAutomata, oracle: VPLStarOracle) -> str | None:
        """
        Get a counter example from the oracle by generating random words.
        """

        trees = self.generator.generate_trees(self.random_trees, self.max_depth)
        for tree in trees:
            if oracle.is_accepted(tree) != tree_automata.is_accepted(tree):
                return tree
        return None