from base.vpl import VPL
from base.alphabet import VPAlphabet

class Dyck1(VPL):
    """
    Dyck1 language is the language of well-formed parentheses.
    It is a simple VPL that accepts sequences of balanced parentheses.
    """

    def __init__(self):
        self.alphabet = VPAlphabet(
            push_symbols={'('},
            pop_symbols={')'},
            int_symbols={'a'},
            name='Dyck1Alphabet'
        )
        super().__init__(self.alphabet)


    def is_accepted(self, sequence: str) -> bool:
        """
        Check if the sequence is a well-formed Dyck1 sequence.
        """

        balance = 0
        for char in sequence:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
            if balance < 0:
                return False
        return balance == 0
    