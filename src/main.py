import asyncio
from RoboterController import RoboterController
from RoboterInterface import RoboterInterface
from Communicator import Robot, Communicator
from MoleController import MoleController
from datatypes import Frame, Position, Orientation, Mole

hole_dist = 285.0
hole_0_x = 2690.0
hole_0_y = -285.0
active_height = 2000.0
inactive_heigth = 1500.0
min_wait = 2.0
max_wait = 5.0

async def setup() -> tuple[RoboterController, MoleController, RoboterInterface]:
    """
    This function initializes relevant objects.
    :returns: tuple with initialized RoboterController, MoleController & RoboterInterface
    """
    interface = Communicator(None, 
                             None, 
                             Frame(Position(0,0,1250), Orientation(0,0,0)),
                             Frame(Position(4400, 0, 0), Orientation(180, 0, 0)),
                             active_height,
                             inactive_heigth)
    await interface.connect()
    rob_ctrl = RoboterController(interface)
    await interface.set_roboter_controller(rob_ctrl)
    moles = []
    for x in range(3):
        for y in range(3):
            moles.append(Mole(3 * x + y, Position(hole_0_x - x * hole_dist, hole_0_y + y * hole_dist, active_height), False))
    mole_ctrl = MoleController(moles, min_wait, max_wait, 1, interface)
    await interface.set_mole_controller(mole_ctrl)
    return rob_ctrl, mole_ctrl, interface


async def main() -> None:
    roboter_controller: RoboterController
    mole_controller: MoleController
    roboter_interface: RoboterInterface
    roboter_controller, mole_controller, roboter_interface = await setup()

    await mole_controller.main_loop()


if __name__ == "__main__":
    asyncio.run(main())
