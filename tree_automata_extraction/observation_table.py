from base.tree import Tree, Context, context_node
from typing import Set, List, Dict, Tuple
from base.alphabet import RankedAlphabet
from tree_automata.tree_automata import TreeAutomata
from tree_automata.tree_state import TreeAutomataState, TreeAutomataTransitionKey

class ObservationTable:
    def __init__(self, alphabet: RankedAlphabet):
        self.S: Set[Tree] = set()  # Árboles confirmados (estados del autómata)
        self.R: Set[Tree] = set()  # Árboles candidatos (a ser verificados)
        self.C: List[Context] = []     # Contextos observados
        self.alphabet: RankedAlphabet = alphabet # Alfabeto clasificado
        self.observations: Dict[Tree, List[bool]] = {} # Tabla de observación
        self.C.append(Context(context_node))

    def complete(self):
        """
        Completes the observation table.
        An OT is complete iif 
            for all s in S,
                for all c in C,
                    there exists a r in R such that,
                        obs(s, c) = obs(r, c)
        """
        for r_tree in self.R:
            not_in_S = True
            for s_tree in self.S:
                if self.complete_obs(s_tree) == self.complete_obs(r_tree):
                    not_in_S = False
                    break
            if not_in_S:
                self.promote_to_S(r_tree)

    def obs(self, tree: Tree, context: Context) -> str:
        """
        Returns the observation of a tree in a given context.
        """
        context_index = self.C.index(context)
        return self.observations.get(tree)[context_index]
    
    def complete_obs(self, tree: Tree):
        """
        Completes the observation of a tree.
        """
        return self.observations.get(tree)
    
    def add_observation(self, tree: Tree, context: Context, observation: str):
        """
        Adds an observation to the observation table.
        """
        if tree not in self.observations:
            self.observations[tree] = [False for _ in range(len(self.C))]
        context_index = self.C.index(context)
        if context_index == len(self.observations[tree]):
            self.observations[tree].append(observation)
        elif context_index > len(self.observations[tree]):
            raise ValueError("Context index is out of bounds.")
        else:
            self.observations[tree][context_index] = observation

    def add_tree(self, tree: Tree, oracle: TreeAutomata):
        """
        Adds a tree to the observation table.
        """
        self.R.add(tree)
        for context in self.C:
            applied_context = tree.apply_context(context)
            # print("Adding observation for tree", tree, "with context", context)
            # print("Applied context", applied_context)
            # print("Is accepted?", oracle.is_accepted(applied_context))
            self.add_observation(tree, context, oracle.is_accepted(applied_context))

    def promote_to_S(self, tree: Tree):
        """
        Promotes a tree from R to S.
        """
        self.S.add(tree)

    def add_context(self, context: Context, oracle: TreeAutomata):
        """
        Adds a context to the observation table.
        """
        self.C.append(context)
        for tree in self.R:
            applied_context = tree.apply_context(context)
            self.add_observation(tree, context, oracle.is_accepted(applied_context))

    def synthesize(self) -> TreeAutomata:
        """
        Synthesizes the tree automaton from the observation table.
        """
        states = set()
        final_states = set()
        transitions = {}
        state_dict = {}
        for tree in self.S:
            state = TreeAutomataState(str(tree))
            state_dict[tuple(self.observations.get(tree))] = state
            states.add(state)
            if self.obs(tree, Context(context_node)):
                final_states.add(state)

        for tree in self.R:
            tree_observations = self.observations.get(tree)
            next_state = state_dict[tuple(tree_observations)]
            transition_symbol = tree.get_root_symbol()
            transition_child_states = self._find_states(tree.children, state_dict)
            key = TreeAutomataTransitionKey(transition_symbol, transition_child_states)
            transitions[key] = next_state
            
        return TreeAutomata(states, self.alphabet, final_states, transitions)
    
    def _find_states(self, trees: List[Tree], state_dict: Dict[List[bool], TreeAutomataState]):
        """
        Finds the states of the children of a tree.
        """
        states = []
        for tree in trees:
            tree_observations = self.observations.get(tree)
            states.append(state_dict[tuple(tree_observations)])
        return states
    
    def _find_equivalent_in_S(self, tree: Tree):
        """
        Finds an equivalent tree in S.
        """
        for s_tree in self.S:
            if self.complete_obs(s_tree) == self.complete_obs(tree):
                return s_tree
        return None
    
    def extend(self, counterexample: Tree, oracle: TreeAutomata):
        """
        Extends the observation table with a counterexample.
        """
        cs = self._decompose(counterexample, Context(context_node))
        if cs is None:
            raise ValueError(f"Counterexample {counterexample} is not decomposable.")

        c, s = cs
        if s in self.R:
            s_prime = self._find_equivalent_in_S(s)
            if s_prime is None:
                raise ValueError(f"Equivalent tree for {s} not found in S.")
            cs_prime = s_prime.apply_context(c)
            # print("Tree", s_prime, "with context", c, "is equivalent to", cs_prime)
            if oracle.is_accepted(cs_prime) == oracle.is_accepted(counterexample):
                # print("Counterexample is consistent.")
                self.extend(cs_prime, oracle)
            else:
                self.add_tree(s, oracle)
                self.promote_to_S(s)
                self.add_context(c, oracle)
                self.complete()
        else:
            # print("Tree not in R!!")
            self.add_tree(s, oracle)
            self.complete()

    def _decompose(self, tree: Tree, context: Context) -> Tuple[Context, Tree] | None:
        """
        Decomposes a tree into c and s.
        """

        if tree in self.S and tree.is_leaf():
            return None

        if tree not in self.S:
            childs_in_S = True
            for child in tree.children:
                childs_in_S = childs_in_S and (child in self.S)
            
            if childs_in_S:
                return context, tree
        
        for i in range(len(tree.children)):
            child = tree.children[i]
            context_part = Context(
                            Tree(
                                tree.root,
                                [tree.children[j] if j != i else context_node for j in range(len(tree.children))]
                                )
                            )
            
            next_context = context_part.root.apply_context(context)
            
            cs = self._decompose(child, Context(next_context))
            if cs is not None:
                return cs
            
        return None
            

    def __str__(self):
        """
        Returns a string representation of the observation table.
        """
        tree_string = ""
        trees = list(self.R)
        s_trees = list(self.S)

        max_len = 4 if not trees else max([len(str(tree)) for tree in trees])

        ctxs_lens = []
        ctxs = (max_len-3)*" " + "| "
        for ctx in self.C:
            ctxs_lens.append(len(str(ctx)))
            ctxs += f"{str(ctx)}\t| "

        tree_string += f"{'Árbol'} {ctxs}\n"
        len_spaces = len(tree_string)
        tree_string += ("-"*(len_spaces+ 10) + "\n")

        for tree in s_trees:
            obs = (2+max_len-len(str(tree)))*" " +"| "
            for context_index in range(len(self.C)):
                context = self.C[context_index]
                new_obs = str(self.obs(tree, context))
                spaces = (ctxs_lens[context_index]-len(new_obs))
                obs += " "*(int(spaces/2)) + new_obs + " "*(int(spaces/2)) + "\t" + "| "
            tree_string += f"{str(tree)} {str(obs)}\n"
        
        tree_string += ("-"*(len_spaces + 10) + "\n")
        for tree in trees:
            if tree in self.S:
                continue
            obs = (2+max_len-len(str(tree)))*" " +"| "
            for context_index in range(len(self.C)):
                context = self.C[context_index]
                new_obs = str(self.obs(tree, context))
                spaces = (ctxs_lens[context_index]-len(new_obs))
                obs += " "*(int(spaces/2)) + new_obs + " "*(int(spaces/2)) + "\t" + "| "
            
            tree_string += f"{str(tree)} {str(obs)}\n"

        return "Tabla de Observación:\n" + tree_string
