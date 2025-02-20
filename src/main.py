import asyncio
from RoboterController import RoboterController
from RoboterInterface import RoboterInterface, Communicator
from MoleController import MoleController


def setup() -> tuple[RoboterController, MoleController, RoboterInterface]:
    """
    This function initializes relevant objects.
    :returns: tuple with initialized RoboterController, MoleController & RoboterInterface
    """
    return RoboterController(), MoleController(), Communicator()


async def main() -> None:
    roboter_controller: RoboterController
    mole_controller: MoleController
    roboter_interface: RoboterInterface
    roboter_controller, mole_controller, roboter_interface = setup()

    mole_controller.start_routine()


if __name__ == "__main__":
    asyncio.run(main())
