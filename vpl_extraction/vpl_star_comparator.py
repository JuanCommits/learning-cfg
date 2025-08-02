from abc import ABC, abstractmethod
from base.vpl import VPL
from vpl_extraction.vpl_star_oracle import VPLStarOracle

class VPLStarComparator(ABC):
    """
    Abstract base class for comparing VPLs using an oracle.
    This class provides a method to get a counter example from the oracle.
    """

    @abstractmethod
    def get_counter_example(self, automata: VPL, oracle: VPLStarOracle) -> str | None:
        """
        Get a counter example from the oracle.
        :param automata: The automata to be compared.
        :return: A counter example if one exists, otherwise None.
        """
        raise NotImplementedError("This method should be implemented in a subclass.")
