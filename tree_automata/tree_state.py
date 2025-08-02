from typing import List
from base.tree import TreeSymbol

class TreeAutomataState:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

class TreeAutomataTransitionKey:
    def __init__(self, symbol: TreeSymbol, child_states: List[TreeAutomataState]):
        self.symbol = symbol
        self.child_states = tuple(child_states)
    
    def __eq__(self, other):
        print(f"Comparing {self} with {other}")
        return self.symbol == other.symbol and tuple(self.child_states) == tuple(other.child_states)

    def __hash__(self):
        return hash(self.symbol) + hash(self.child_states)
    
    def __str__(self):
        return f"Key({self.symbol}, {[str(child) for child in self.child_states]})"

