import asyncio
from RoboterController import RoboterController
from RoboterInterface import RoboterInterface
from MockInterface import MockInterface as Communicator
from MoleController import MoleController


def setup() -> tuple[RoboterController, MoleController, RoboterInterface]:
    """
    This function initializes relevant objects.
    :returns: tuple with initialized RoboterController, MoleController & RoboterInterface
    """
    return RoboterController(), MoleController(), Communicator(randomised=True)


async def main() -> None:
    roboter_controller: RoboterController
    mole_controller: MoleController
    roboter_interface: RoboterInterface
    roboter_controller, mole_controller, roboter_interface = setup()

    await mole_controller.update()


if __name__ == "__main__":
    asyncio.run(main())
