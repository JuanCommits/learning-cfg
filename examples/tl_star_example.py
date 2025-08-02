from examples.tree_automata_example import tree_automaton as oracle
from examples.tree_automata_example import simple_tree_automaton as simple_oracle
from tree_automata_extraction.tl_star import TLStar

def run_example():
    print("RUNNING TL* EXMAPLE...\n")
    
    run_simple_example()

    print("\n\n"+"*"*120+"\n\n")

    run_drewes_example()

def run_drewes_example():
    print("Drewes Example")
    print("*"*120+'\n')
    print("Oracle:", oracle)
    print("*"*120+'\n')

    tl_star = TLStar(oracle)
    automata = tl_star.learn()
    print("Observation Table: ", tl_star.observation_table)

    print("*"*120+'\n')

    print("Result: ", automata)

    print("*"*120+'\n')

def run_simple_example():
    print("Simple Example")
    print("*"*120+'\n')

    print("Oracle:", simple_oracle)
    print("*"*120+'\n')

    tl_star = TLStar(simple_oracle)
    automata = tl_star.learn()
    print("Observation Table: ", tl_star.observation_table)

    print("*"*120+'\n')

    print("Result: ", automata)

    print("*"*120+'\n')