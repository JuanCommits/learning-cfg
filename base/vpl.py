from abc import ABC, abstractmethod
from base.alphabet import VPAlphabet

class VPL(ABC):
    def __init__(self, alphabet: VPAlphabet):
        self.alphabet = alphabet

    def get_alphabet(self) -> VPAlphabet:
        return self.alphabet
    
    @abstractmethod
    def is_accepted(self, sequence: str) -> bool:
        raise NotImplementedError
    
    def get_random_word(self) -> str:
        """
        Generate a random word from the alphabet of the VPL.
        """
        return self.alphabet.get_random_word()
    