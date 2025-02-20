from RoboterInterface import RoboterInterface
import datatypes as types
from typing import List
import random

class MockInterface(RoboterInterface):
    """
    Mock implementation of RoboterInterface for testing purposes.
    It stores its own moles and TCP position and if randomised is true, one mole will move around the board on every get_moles() call.
    """
    def __init__(self, randomised:bool):
        """
        param randomised: Whether to move one mole to a random position every time get_moles is called
        """
        self.tcp = types.Frame(types.Position(100, -50, 220), types.Orientation(280, 170, 0))
        self.mymoles = [types.Mole(i, types.Position((i%3)*100, (i//3)*100, 100), False) for i in range(9)]
        self.randomised = randomised
        if randomised:
            self.moving_mole: types.Mole = None

    async def set_mole(self, mole: types.Mole) -> None:
        if not mole in self.mymoles:
            raise ValueError(f"Mole {mole} not found in moles list")
        mole.is_active = True
        print(f"Set mole {mole}")

    async def unset_mole(self, mole: types.Mole) -> None:
        if not mole in self.mymoles:
            raise ValueError(f"Mole {mole} not found in moles list")
        mole.is_active = False
        print(f"Unset mole {mole}")

    async def move_tcp(self, frame: types.Frame) -> None:
        self.tcp = frame
        print(f"TCP moved to {self.tcp}")

    async def get_tcp(self) -> types.Frame:
        return self.tcp

    async def get_moles(self) -> List[types.Mole]:
        if self.randomised:
            if self.moving_mole:
                await self.unset_mole(self.moving_mole)
            self.moving_mole = self.mymoles[random.randint(0, 8)]
            await self.set_mole(self.moving_mole)
        return self.mymoles

    async def notify(self) -> None:
        print("Notified")