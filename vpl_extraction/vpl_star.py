from vpl_extraction.vpl_star_oracle import VPLStarOracle
from vpl_extraction.vpl_star_random_comparator import VPLRandomComparator
from tree_automata_extraction.tl_star import TLStar
from models.tree_automata_vpl import nta_2_vpg
from base.vpl import VPL

class VPLStar:
    def __init__(self, oracle: VPL, comparator: VPLRandomComparator=None):
        self.oracle = VPLStarOracle(oracle)
        if comparator is None:
            comparator = VPLRandomComparator(oracle.alphabet)
        
        self.comparator = comparator
        self.TLStar = TLStar(self.oracle, self.comparator)

    def learn(self):
        learned_tree_automata = self.TLStar.learn()
        return nta_2_vpg(learned_tree_automata, self.oracle.get_alphabet())