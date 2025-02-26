from RoboterInterface import RoboterInterface
from RoboterController import RoboterController
from MoleController import MoleController
from datatypes import Mole, Frame, Position, Orientation
from typing import List


class MockInterface(RoboterInterface):
    """
    Mock implementation of RoboterInterface for testing purposes.
    It stores its own moles and TCP position and if randomised is true, one mole will move around the board on every get_moles() call.
    """

    def __init__(self,
                 mole_controller: MoleController | None,
                 roboter_controller: RoboterController | None):
        """
        param randomised: Whether to move one mole to a random position every time get_moles is called
        """
        self.roboter_controller = roboter_controller
        self.mole_controller = mole_controller

    async def set_mole(self, mole: Mole) -> None:
        if mole not in self.get_moles():
            raise ValueError(f"Mole {mole} not found in moles list")
        mole.is_active = True
        print(f"Set mole {mole}")

    async def unset_mole(self, mole: Mole) -> None:
        if mole not in self.get_moles():
            raise ValueError(f"Mole {mole} not found in moles list")
        mole.is_active = False
        print(f"Unset mole {mole}")

    async def move_tcp(self, frame: Frame) -> None:
        self.tcp = frame
        print(f"TCP moved to {self.tcp}")

    async def get_tcp(self) -> Frame:
        return self.tcp

    async def get_moles(self) -> List[Mole]:
        return self.mole_controller.moles

    async def notify(self) -> None:
        await self.roboter_controller.notify()
        print("Notified")
