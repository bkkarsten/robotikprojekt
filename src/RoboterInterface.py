from abc import ABC, abstractmethod
from typing import List
import datatypes as types


class RoboterInterface(ABC):
    """
    Robot interface for managing moles and TCP (Tool Center Point) movements in the RobGL-Simulation.

    For detailed architecture documentation, see docs/architecture.
    """
    @abstractmethod
    def set_mole(self, mole: types.Mole) -> None:
        pass

    @abstractmethod
    def unset_mole(self, mole: types.Mole) -> None:
        pass

    @abstractmethod
    def move_tcp(self, pos: types.Position, return_home: bool = False) -> None:
        pass

    @abstractmethod
    def get_tcp(self) -> types.Position:
        pass

    @abstractmethod
    def get_moles(self) -> List[types.Mole]:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

