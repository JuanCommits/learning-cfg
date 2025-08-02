from base.alphabet import VPAlphabet, RankedAlphabet
from base.tree import TreeSymbol, Tree, empty_symbol, epsilon, empty_tree


def vpalphabet_2_ranked(vpalphabet: VPAlphabet) -> RankedAlphabet:
    """
    Convert a VPA alphabet to a ranked alphabet.
    """

    push_symbols = {TreeSymbol(push_symbol, 2) for push_symbol in vpalphabet.push_symbols}
    pop_symbols = {TreeSymbol(pop_symbol, 1) for pop_symbol in vpalphabet.pop_symbols}
    int_symbols = {TreeSymbol(int_symbol, 1) for int_symbol in vpalphabet.int_symbols}
    base_symbol = {empty_symbol}
    all_symbols = push_symbols.union(pop_symbols).union(int_symbols).union(base_symbol)
    return RankedAlphabet(all_symbols, vpalphabet.name)


def tree_2_sequence(tree: Tree, alphabet: VPAlphabet) -> str:
    """
    Convert a well-formed tree to a sequence of symbols.
    The tree must be well-formed, meaning that it should belong to T(B_parse).
    """

    pending = [tree]
    sequence = []
    while pending:
        current = pending.pop()
        if not current.is_leaf():
            symbol = current.root.name
            if symbol not in alphabet.get_all_symbols():
                raise ValueError(f"Symbol {symbol} is not in the alphabet.")
            if symbol in alphabet.get_push_symbols() and current.root.arity != 2:
                raise ValueError(f"Symbol {symbol} is not a push symbol.")
            if (symbol in alphabet.get_pop_symbols() or symbol in alphabet.get_int_symbols()) and current.root.arity != 1:
                raise ValueError(f"Symbol {symbol} is not a pop or internal symbol.")
            sequence.append(current.root.name)
            for child in reversed(current.children):
                pending.append(child)
    
    return ''.join(sequence)


def sequence_2_tree(sequence: str, alphabet: VPAlphabet) -> Tree:
    """
    Convert a sequence of symbols to a tree.
    The sequence must be well-formed, meaning that it should belong to B_parse.

    If the sequnce is not well-formed or has symbols that are not in the alphabet, it raises a ValueError.
    """

    if sequence is None:
        raise ValueError(f"Sequence cannot be None.")

    if len(sequence) == 0 or sequence == epsilon:
        return Tree(TreeSymbol(empty_symbol, 0), [])

    stack: list[Tree] = []
    for i in range(len(sequence)-1, -1, -1):
        symbol = sequence[i]

        # If the symbol is not in the alphabet, raise an error.
        if symbol not in alphabet.get_all_symbols():
            raise ValueError(f"Symbol {symbol} is not in the alphabet.")
        
        
        # If the stack is empty and the symbol is push the sequence is not well-formed
        # If not we just add the correspondig tree to the stack.
        if not stack:
            if symbol in alphabet.get_push_symbols():
                raise ValueError(f"Sequence is not well-formed. Push symbol {symbol} without a pop symbol.")
            else:
                stack.append(Tree(TreeSymbol(symbol, 1), [empty_tree]))
            continue

        if symbol in alphabet.get_push_symbols():
            last_to_process = stack.pop()
            if last_to_process.root.value in alphabet.get_pop_symbols():
                # If the last processed symbol is a pop symbol, 
                # it means there is no symbol between the push and pop.
                left_child = empty_tree
            else:
                # If the last processed symbol is not a pop symbol, 
                # it means there is a subtree that should be the left chile of the new push symbol.
                left_child = stack.pop()
            new_sub_tree = Tree(TreeSymbol(symbol, 2), [last_to_process, left_child])
            stack.append(new_sub_tree)

        elif symbol in alphabet.get_pop_symbols():
            last_to_process = stack.pop()
            if last_to_process.root.value in alphabet.get_pop_symbols():
                # If the last processed symbol is a pop symbol then it can't be the child of other pop symbol.
                # We add the last pop symbol and the new one with an ampty tree as child.
                stack.append(last_to_process)
                child = empty_tree
            else:
                # If the last processed symbol is not a pop symbol,
                # it means it is a child of the pop tree.
                child = last_to_process
            stack.append(Tree(TreeSymbol(symbol, 1), [child]))

        elif symbol in alphabet.get_int_symbols():
            last_to_process = stack.pop()
            if last_to_process.root.value in alphabet.get_pop_symbols():
                # If it's a pop symbol, then it can't be a child of an internal symbol.
                # We add the pop tree and set the child of the internal tree to empty tree.
                stack.append(last_to_process)
                child = empty_tree
            else:
                # If it's not a pop symbol, then it is a child of the internal tree.
                # We set the child of the internal tree to the last processed tree.
                child = last_to_process
            stack.append(Tree(TreeSymbol(symbol, 1), [child]))

    # After processing all symbols, there should be exactly one tree in the stack.
    # If there are more than one, it means the sequence is not well-formed.
    if len(stack) != 1:
        raise ValueError("Sequence does not form a well-formed tree.")

    return stack[0]
