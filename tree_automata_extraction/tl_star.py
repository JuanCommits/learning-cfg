from tree_automata_extraction.observation_table import ObservationTable
from tree_automata.tree_automata import TreeAutomata
from tree_automata.tree_comparator import TreeComparator

class TLStar:
    def __init__(self, oracle, eq = None):
        self.observation_table = ObservationTable(oracle.alphabet)
        self.oracle = oracle
        self.comparator = eq if eq else TreeComparator(oracle)

    def learn(self):
        """
        Learns a tree automata from the observation table.
        """
        while True:
            automata = self.observation_table.synthesize()
            counterexample = self.comparator.get_counter_example(automata, self.oracle)
            if counterexample is None:
                return automata
            else:
                self.observation_table.extend(counterexample, self.oracle)
