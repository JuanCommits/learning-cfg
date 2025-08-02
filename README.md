# Learning Context-Free Grammars (CFG) and Visibly Pushdown Languages (VPL)

A Python implementation for learning Context-Free Grammars and Visibly Pushdown Languages using tree automata and the TL* algorithm.

## Overview

This project implements algorithms for learning formal languages, specifically:
- **Tree Automata Learning**: Implementation of the TL* algorithm for learning tree automata from examples
- **Visibly Pushdown Language (VPL) Learning**: Extension of tree automata learning to VPLs using VPL* algorithm
- **Context-Free Grammar Learning**: Learning CFGs through tree automata representations

The project provides a complete framework for:
- Tree automata construction and manipulation
- Observation table-based learning algorithms
- Tree-to-sequence and sequence-to-tree encoding/decoding
- Well-formedness checking for VPL sequences
- Various examples demonstrating the learning algorithms

## Project Structure

```
learning-cfg/
├── base/                          # Core data structures
│   ├── alphabet.py               # Alphabet definitions (RankedAlphabet, VPAlphabet)
│   ├── state.py                  # State definitions
│   ├── tree.py                   # Tree and Context data structures
│   └── vpl.py                    # Abstract VPL base class
├── tree_automata/                # Tree automata implementation
│   ├── tree_automata.py          # Main tree automata class
│   ├── tree_comparator.py        # Tree automata comparison utilities
│   ├── tree_generator.py         # Tree generation utilities
│   └── tree_state.py             # Tree automata state definitions
├── tree_automata_extraction/     # Learning algorithms
│   ├── observation_table.py      # Observation table implementation
│   └── tl_star.py               # TL* learning algorithm
├── vpl_extraction/               # VPL learning algorithms
│   ├── vpl_star.py              # VPL* learning algorithm
│   ├── vpl_star_oracle.py       # VPL oracle implementation
│   ├── vpl_star_comparator.py   # VPL comparison utilities
│   └── vpl_star_random_comparator.py  # Random comparator for VPLs
├── models/                       # Model implementations
│   ├── tree_automata_vpl.py     # Tree automata to VPL conversion
│   └── vpa.py                   # Visibly Pushdown Automata
├── utils/                        # Utility functions
│   ├── encoding.py              # Tree-sequence encoding/decoding
│   └── well_formed.py           # Well-formedness checking
├── examples/                     # Example implementations
│   ├── tree_automata_example.py # Tree automata examples
│   ├── tl_star_example.py       # TL* algorithm examples
│   ├── ot_example.py            # Observation table examples
│   ├── context_example.py       # Context examples
│   └── dyck1.py                 # Dyck1 language implementation
├── run.py                       # Main execution script
└── encoding_tests.ipynb         # Jupyter notebook with encoding tests
```

## Key Features

### 1. Tree Automata
- **Tree Structure**: Implementation of ranked trees with symbols of varying arity
- **Tree Automata**: Deterministic tree automata with state transitions
- **Tree Processing**: Efficient tree traversal and acceptance checking
- **Tree Comparison**: Equivalence checking between tree automata

### 2. TL* Learning Algorithm
- **Observation Table**: Maintains examples and their observations
- **Context Management**: Handles tree contexts for learning
- **Counterexample Processing**: Extends observation table with counterexamples
- **Automata Synthesis**: Constructs tree automata from observation tables

### 3. VPL Learning (VPL*)
- **VPL Support**: Learning Visibly Pushdown Languages
- **Tree-to-VPL Conversion**: Converting learned tree automata to VPLs
- **Well-formedness Checking**: Validating VPL sequences
- **Encoding/Decoding**: Converting between trees and VPL sequences

### 4. Utility Functions
- **Alphabet Management**: Ranked alphabets and VPA alphabets
- **Tree Operations**: Context application, tree manipulation
- **Sequence Processing**: Well-formedness validation for VPL sequences

## Usage

### Running Examples

The project includes several examples that can be run using the main script:

```bash
# Run all examples
python run.py

# Run specific examples
python run.py 1  # TL* example
python run.py 2  # Observation table example
python run.py 3  # Tree automata example
python run.py 4  # Context example
```

### Basic Tree Automata Usage

```python
from tree_automata.tree_automata import TreeAutomata, TreeAutomataState
from base.tree import Tree, TreeSymbol
from base.alphabet import RankedAlphabet

# Define states
q0 = TreeAutomataState('q0')
q1 = TreeAutomataState('q1')

# Define alphabet
a = TreeSymbol('a', 2)  # Binary symbol
b = TreeSymbol('b', 0)  # Leaf symbol
alphabet = RankedAlphabet({a, b}, "TestAlphabet")

# Define transitions
transitions = {
    TreeAutomataTransitionKey(b, []): q1,
    TreeAutomataTransitionKey(a, [q1, q1]): q0,
}

# Create automaton
automaton = TreeAutomata({q0, q1}, alphabet, {q0}, transitions)

# Test a tree
tree = Tree(a, [Tree(b, []), Tree(b, [])])
is_accepted = automaton.is_accepted(tree)
```

### TL* Learning Example

```python
from tree_automata_extraction.tl_star import TLStar
from examples.tree_automata_example import simple_tree_automaton

# Create TL* learner
tl_star = TLStar(simple_tree_automaton)

# Learn the automaton
learned_automaton = tl_star.learn()
print("Learned automaton:", learned_automaton)
```

### VPL Learning Example

```python
from vpl_extraction.vpl_star import VPLStar
from examples.dyck1 import Dyck1

# Create VPL oracle
dyck1 = Dyck1()

# Create VPL* learner
vpl_star = VPLStar(dyck1)

# Learn the VPL
learned_vpl = vpl_star.learn()
```

## Examples Included

1. **Tree Automata Examples**: Basic tree automata construction and testing
2. **TL* Examples**: Learning tree automata using the TL* algorithm
3. **Observation Table Examples**: Demonstrating observation table operations
4. **Context Examples**: Tree context manipulation and application
5. **Dyck1 Language**: Implementation of the Dyck1 language (balanced parentheses)

## Dependencies

The project uses only Python standard library modules:
- `typing`
- `collections`
- `abc`
- `sys`

No external dependencies are required.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Juan Pedro da Silva

## Research Context

This implementation is designed for research in formal language learning, specifically:
- Learning Context-Free Grammars through tree automata
- Visibly Pushdown Language learning
- Active learning algorithms for formal languages
- Tree automata synthesis from examples

The project provides a foundation for experimenting with different learning algorithms and formal language representations.