from abc import ABC, abstractmethod
from typing import List
import datatypes as types
import asyncio


class RoboterInterface(ABC):
    """
    Robot interface for managing moles and TCP (Tool Center Point) movements in the RobGL-Simulation.

    For detailed architecture documentation, see docs/architecture.
    """
    @abstractmethod
    async def set_mole(self, mole: types.Mole) -> None:
        pass

    @abstractmethod
    async def unset_mole(self, mole: types.Mole) -> None:
        pass

    @abstractmethod
    async def move_tcp(self, frame: types.Frame) -> None:
        pass

    @abstractmethod
    async def get_tcp(self) -> types.Frame:
        pass

    @abstractmethod
    async def get_moles(self) -> List[types.Mole]:
        pass

    @abstractmethod
    async def notify(self) -> None:
        pass
