from RoboterController import RoboterController
from RoboterInterface import RoboterInterface
from Communicator import Robot, Communicator
from MoleController import MoleController
from datatypes import Frame, Position, Orientation, Mole
from constants import *


def setup() -> tuple[RoboterController, MoleController, RoboterInterface]:
    """
    This function initializes relevant objects.
    :returns: tuple with initialized RoboterController, MoleController & RoboterInterface
    """
    interface = Communicator(mole_controller=None,
                             roboter_controller=None,
                             hammer_rob_frame=Frame(Position(0, 0, 1250), Orientation(0, 0, 0)),
                             mole_rob_frame=Frame(Position(4400, 0, 0), Orientation(180, 0, 0)),
                             active_mole_height=ACTIVE_HEIGHT,
                             inactive_mole_height=INACTIVE_HEIGHT,
                             host='192.168.128.2')
    rob_ctrl = RoboterController(interface)
    interface.set_roboter_controller(rob_ctrl)
    moles = []
    for x in range(3):
        for y in range(3):
            moles.append(
                Mole(3 * x + y, Position(HOLE_0_X - x * HOLE_DIST, HOLE_0_Y + y * HOLE_DIST, ACTIVE_HEIGHT), False))
    mole_ctrl = MoleController(moles, MIN_WAIT, MAX_WAIT, 1, interface)
    interface.set_mole_controller(mole_ctrl)
    return rob_ctrl, mole_ctrl, interface


def main() -> None:
    roboter_controller: RoboterController
    mole_controller: MoleController
    roboter_interface: RoboterInterface
    roboter_controller, mole_controller, roboter_interface = setup()

    mole_controller.main_loop()


if __name__ == "__main__":
    main()
