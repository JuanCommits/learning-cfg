from typing import List
from collections import deque

class TreeSymbol:
    """
    A symbol in a tree.
    Each symbol has a name and an arity (number of children).
    The arity is used to check if the symbol is well-formed.
    """

    def __init__(self, name: str, arity: int):
        self.name = name
        self.arity = arity
    
    def __str__(self):
        """
        String representation of the symbol.
        """
        return f"{self.name}"
    
    def __eq__(self, other):
        """
        Check if two symbols are equal.
        Two symbols are equal if they have the same name and arity.
        """
        return self.name == other.name and self.arity == other.arity
    
    def __hash__(self):
        """
        Hash function for the symbol.
        """
        return hash(self.name + str(self.arity))
    
    @property
    def value(self):
        return self.name


class Tree:
    """
    A tree structure with a root symbol and children.
    Each node in the tree is represented by a TreeSymbol.
    """
    def __init__(self, root: TreeSymbol, children: List['Tree'] = []):
        self.root = root
        assert root.arity == len(children), f"Arity of root {root} does not match number of children {len(children)}"
        self.children = children

    def apply_context(self, context):
        """
        Apply a context to the tree.
        The context must have exactly one context symbol.
        """
        if not context.has_exactly_one_context_symbol(context.root):
            print(context)
            raise ValueError("Tree must have exactly one context symbol.")
        
        return self._apply_recursive(context.root)
    
    def _apply_recursive(self, tree):
        """
        Recursively apply the context to the tree.
        This method traverses the tree and applies the context symbol to each node.
        """
        if tree.get_root_symbol() == context_symbol:
            return self
        
        new_children = []
        for child in tree.children:
            new_children.append(self._apply_recursive(child))
        
        return Tree(tree.get_root_symbol(), new_children)
    
    def is_leaf(self):
        """
        Check if the tree is a leaf node (i.e., has no children).
        """
        return self.root.arity == 0
    
    def __str__(self):
        """
        String representation of the tree.
        """
        return f"{self.root} {[child.__str__() for child in self.children]}"
    
    def __eq__(self, other):
        """
        Check if two trees are equal.
        Two trees are equal if they have the same root symbol and the same children.
        """
        return self.root == other.root and self.children == other.children
    
    def __hash__(self):
        """
        Hash function for the tree.
        """
        return hash((self.root, tuple(self.children)))
    
    def name(self):
        """
        Get the name of the root symbol of the tree.
        This method returns the name of the root symbol.
        """
        return self.root.name
    
    def get_root_symbol(self):
        """
        Get the root symbol of the tree.
        This method returns the root symbol of the tree.
        """
        return self.root
    

class Context:
    """
    A context for a tree.
    A context is a tree that has exactly one context symbol.
    The context symbol is represented by a special TreeSymbol.
    The context symbol is used to apply the context to the tree.
    """

    def __init__(self, tree: Tree):
        if self.has_exactly_one_context_symbol(tree):
            self.root = tree
        else:
            raise ValueError("Context must have exactly one context symbol.")
    
    def has_exactly_one_context_symbol(self, tree):
        """
        Check if the tree has exactly one context symbol.
        """
        queue = deque()
        has_context_symbol = False
        queue.append(tree)
        while queue:
            current_node = queue.popleft()
            if current_node.is_leaf():
                if current_node.root == context_symbol:
                    if has_context_symbol:
                        return False
                    has_context_symbol = True
            else:
                children = current_node.children
                for child in children:                    
                    queue.append(child)
        return has_context_symbol

    def __str__(self):
        """
        String representation of the context.
        """
        return self.root.__str__()
    
    def __eq__(self, other):
        """
        Check if two contexts are equal.
        Two contexts are equal if they have the same root symbol and the same children.
        """
        return self.root == other.root
    
    def __hash__(self):
        """
        Hash function for the context.
        """
        return hash(self.root, tuple(self.root.children))
    
    def get_children(self):
        """
        Get the children of the context.
        """
        return self.root.children
    
    def get_root_symbol(self):
        """
        Get the root symbol of the context.
        """
        return self.root.root
    
    def is_leaf(self):
        """
        Check if the context is a leaf node (i.e., has no children).
        """
        return self.root.is_leaf()


epsilon = 'ε'
empty_symbol = TreeSymbol(epsilon, 0)
empty_tree = Tree(empty_symbol, [])

context_symbol = TreeSymbol('•', 0)
context_node = Tree(context_symbol, [])
