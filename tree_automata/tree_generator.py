import random
from base.tree import Tree
from base.tree import TreeSymbol
from base.alphabet import RankedAlphabet

class TreeGenerator:
    def __init__(self, ranked_alphabet: RankedAlphabet):
        self.ranked_alphabet = ranked_alphabet

    def generate_tree(self, max_depth: int) -> Tree:
        symbols = list(self.ranked_alphabet.alphabets)
        root_symbol = random.choice(symbols)

        if max_depth == 0 or root_symbol.arity == 0:
            root_symbol = root_symbol if root_symbol.arity == 0  else \
                random.choice(list(self.ranked_alphabet.get_symbols_by_arity(0)))
            return Tree(root=root_symbol, children=[])

        # Generar los hijos según la aridad del símbolo raíz
        children = [
            self.generate_tree(max_depth - 1) for _ in range(root_symbol.arity)
        ]

        return Tree(root=root_symbol, children=children)
    
    def generate_trees(self, n: int, max_depth: int) -> list[Tree]:
        return [self.generate_tree(max_depth) for _ in range(n)]