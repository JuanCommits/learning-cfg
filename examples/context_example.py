from examples.tree_automata_example import tree1, tree2, tree3
from base.tree import Context, Tree, context_node, TreeSymbol

tree4 = context_node
tree5 = Tree(TreeSymbol("a", 2), [context_node, context_node])
tree6 = Tree(TreeSymbol("a", 2), [Tree(TreeSymbol("b", 0)), context_node])

def run_example():
    print("RUNNING CONTEXT EXAMPLE...")
    create_context(tree1)
    print("*"*120)
    create_context(tree2)
    print("*"*120)
    create_context(tree3)
    print("*"*120)
    create_context(tree4)
    print("*"*120)
    create_context(tree5)
    print("*"*120)
    create_context(tree6)
    

def create_context(tree):
    print("Creating context for tree:", tree)
    try:
        context1 = Context(tree)
        print("Tree is a context!!")
    except Exception as e:
        print(e)
        print("Tree is NOT a context!")

