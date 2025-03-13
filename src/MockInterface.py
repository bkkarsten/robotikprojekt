from RoboterInterface import RoboterInterface
from RoboterController import RoboterController
from MoleController import MoleController
from datatypes import Mole, Position
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
        self._tcp = Position(0, 0, 0)
        self._roboter_controller = roboter_controller
        self._mole_controller = mole_controller

    def set_mole(self, mole: Mole) -> None:
        if mole not in self.get_moles():
            raise ValueError(f"Mole {mole} not found in moles list")
        mole.is_active = True
        print(f"Set mole {mole}")

    def unset_mole(self, mole: Mole) -> None:
        if mole not in self.get_moles():
            raise ValueError(f"Mole {mole} not found in moles list")
        mole.is_active = False
        print(f"Unset mole {mole}")

    def move_tcp(self, pos: Position) -> None:
        self._tcp = pos
        print(f"TCP moved to {self._tcp}")

    def get_tcp(self) -> Position:
        return self._tcp

    def get_moles(self) -> List[Mole]:
        return self._mole_controller.moles

    def notify(self) -> None:
        self._roboter_controller.notify()
        print("Notified")

    def set_roboter_controller(self, roboter_controller: RoboterController) -> None:
        self._roboter_controller = roboter_controller

    def set_mole_controller(self, mole_controller: MoleController) -> None:
        self._mole_controller = mole_controller
