from utils.encoding import tree_2_sequence, vpalphabet_2_ranked
from utils.well_formed import tree_is_well_formed
from base.alphabet import VPAlphabet
from base.tree import Tree
from base.vpl import VPL
from utils.b_parse import get_t_b_parse

class VPLStarOracle:
    """
    An oracle for VPLs that provides methods to check if a tree is accepted
    by the VPL and to generate random words from the VPL's alphabet.
    """

    def __init__(self, vpl: VPL):
        self.vpl = vpl
        self.t_b_parse = get_t_b_parse(vpl.get_alphabet())

    @property
    def alphabet(self) -> VPAlphabet:
        """
        Get the alphabet of the VPL.
        This is a property to allow easy access to the alphabet.
        """
        return self.vpl.get_alphabet()
    

    def get_alphabet(self) -> VPAlphabet:
        """
        Get the alphabet of the VPL.
        """

        return self.vpl.get_alphabet()


    def is_accepted(self, tree: Tree) -> bool:
        """
        Check if a sequence is accepted by the VPL.
        """
        if not self.t_b_parse.is_accepted(tree):
            return False
        sequence = tree_2_sequence(tree, self.get_alphabet())
        return self.vpl.is_accepted(sequence)
    
    
    def get_random_word(self) -> str:
        """
        Generate a random word from the alphabet of the VPL.
        """

        return self.vpl.get_random_word()