import random

from typing import Set
from base.tree import TreeSymbol

bottom_symbol = '⊥'

class VPAlphabet:
    """
    A class representing the Visible Pushdown Alphabet.
    The alphabet consists of push, pop, and internal symbols.
    """

    def __init__(self, push_symbols: Set, pop_symbols: Set, 
                 int_symbols: Set, name='VPAlphabet'):
        self.push_symbols = push_symbols
        self.pop_symbols = pop_symbols
        self.int_symbols = int_symbols
        self.name = name
    
    def get_all_symbols(self) -> Set:
        return self.push_symbols.union(self.pop_symbols).union(self.int_symbols)
    
    def get_push_symbols(self) -> Set:
        return self.push_symbols
    
    def get_pop_symbols(self) -> Set:
        return self.pop_symbols
    
    def get_int_symbols(self) -> Set:
        return self.int_symbols
    
    def get_random_word(self, len: int = None) -> str:
        if len is None:
            len = random.randint(1, 50)
        if len < 1:
            raise ValueError("Length must be greater than 0.")
        
        return ''.join(random.choice(list(self.get_all_symbols())) for _ in range(len))
    
    def __str__(self):
        """
        String representation of the alphabet.
        """
        return f"VPAlphabet({self.name}): Push: {self.push_symbols}, Pop: {self.pop_symbols}, Int: {self.int_symbols}"
    
class StackAlphabet:
    def __init__(self, symbols: Set, name='StackAlphabet'):
        self.symbols = symbols
        self.name = name
    
    def get_symbols(self) -> Set:
        return self.symbols

class RankedAlphabet:
    def __init__(self, alphabets: Set[TreeSymbol], name):
        self.alphabets = alphabets
        self.name = name

    def get_symbols_by_arity(self, arity: int) -> Set:
        return {symbol for symbol in self.alphabets if symbol.arity == arity}
    