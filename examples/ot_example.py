from base.tree import Tree
from tree_automata_extraction.observation_table import ObservationTable
from examples.tree_automata_example import tree_automaton as oracle
from examples.tree_automata_example import a, b, epsilon, alphabet

def run_example():
    print("RUNNING OBSERVATION TABLE EXAMPLE...\n")
    print("*"*120+'\n')

    t2 = ObservationTable(alphabet)
    print("Starting with an empyty table...")
    print("T1:")
    print(str(t2))

    counterexample = Tree(a, [
                        Tree(a, [
                            Tree(epsilon, []),
                            Tree(epsilon, [])
                        ]), 
                        Tree(b, [
                            Tree(epsilon, []),
                            Tree(epsilon, [])
                        ])
                    ])
    print("*"*120+'\n')
    print(f"Extending T1 with counterexample {counterexample}")
    print("T2:")
    t2.extend(counterexample, oracle)
    t2.complete()
    print(str(t2))
    
    print("*"*120+'\n')
    print(f"Extending T2 with counter-example {counterexample}:")
    print("T3:")
    t2.extend(counterexample, oracle)
    t2.complete()
    print(str(t2))

    print("*"*120+'\n')
    print(f"Extending T3 with counter-example {counterexample}:")
    print("T4:")
    t2.extend(counterexample, oracle)
    print(str(t2))

    counterexample = Tree(b, [
                            Tree(a, [
                                Tree(a, [
                                    Tree(epsilon, []),
                                    Tree(epsilon, [])
                                ]),
                                Tree(epsilon, [])
                            ]), 
                            Tree(a, [
                                Tree(epsilon, []),
                                Tree(epsilon, [])
                            ])
                        ])
    print("*"*120+'\n')
    print(f"Extending T4 with counter-example {counterexample}:")
    print("T5:")
    t2.extend(counterexample, oracle)
    t2.complete()
    print(str(t2))

    counterexample = Tree(a, [
                            Tree(b, [
                                Tree(epsilon, []),
                                Tree(epsilon, [])
                            ]),
                            Tree(b, [
                                Tree(epsilon, []),
                                Tree(epsilon, [])
                            ])
                        ])
    print("*"*120+'\n')
    print(f"Extending T5 with counter-example {counterexample}:")
    print("T6:")
    t2.extend(counterexample, oracle)
    print(str(t2))

    print("*"*120+'\n')
    print("Finished Observation Table example...")



    

