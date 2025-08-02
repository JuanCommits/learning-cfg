from typing import Tuple
from tree_automata.tree_generator import TreeGenerator
from base.alphabet import RankedAlphabet
from base.tree import Tree

class TreeComparator:
    def __init__(self, model, tree_generator: TreeGenerator = None, sample_size = 1000):
        self.__target_model = model
        self.sample_size = sample_size
        if tree_generator is None:
            self._tree_generator = TreeGenerator(self.__target_model.alphabet)
        else:
            self._tree_generator = tree_generator

    @property
    def alphabet(self) -> RankedAlphabet:
        return self.__target_model.alphabet

    def equivalence_query(self, model) -> Tuple[bool, Tree]:
        trees = self._tree_generator.generate_trees(self.sample_size, max_depth=5)
        for tree in trees:
            if self.__target_model.is_accepted(tree) != model.is_accepted(tree):
                return False, tree
        
        return True, None
    
    def get_counter_example(self, model, oracle) -> Tree:
        return self.equivalence_query(model)[1]
