import asyncio
from typing import List, Tuple
from datatypes import Position, Mole
from RoboterController import RoboterController
from RoboterInterface import RoboterInterface
from MockInterface import MockInterface as Communicator
from MoleController import MoleController


def setup() -> tuple[RoboterController, MoleController, RoboterInterface]:
    """
    This function initializes relevant objects.
    :returns: tuple with initialized RoboterController, MoleController & RoboterInterface
    """
    moles: List[Mole] = []
    # home position of the simulation
    home_position: Position = Position(2405, 5, 1000)

    for x in range(-1, 2):
        for y in range(-1, 2):
            position: Position = Position(home_position.x + x * 100, home_position.y + y * 100, home_position.z)
            moles.append(Mole(mole_id=x + y, position=position, isActive=False))

    communicator: RoboterInterface = Communicator(randomised=True, roboter_controller=None, mole_controller=None)
    roboter_controller: RoboterController = RoboterController(roboter_interface=communicator)
    mole_controller: MoleController = MoleController(moles=moles,
                                                     min_waiting_time=1,
                                                     max_waiting_time=2,
                                                     max_moles=1,
                                                     roboter_interface=communicator)
    communicator.roboter_controller = roboter_controller
    communicator.mole_controller = mole_controller
    return roboter_controller, mole_controller, communicator


async def main() -> None:
    roboter_controller: RoboterController
    mole_controller: MoleController
    roboter_interface: RoboterInterface
    roboter_controller, mole_controller, roboter_interface = setup()

    await mole_controller.main_loop()


if __name__ == "__main__":
    asyncio.run(main())
