from RoboterInterface import RoboterInterface
from MoleController import MoleController
from RoboterController import RoboterController
from datatypes import Frame, Position, Orientation, Mole
from typing import List
import asyncio
from Robot import Robot

class Communicator(RoboterInterface):
    def __init__(self,
                 mole_controller: MoleController | None,
                 roboter_controller: RoboterController | None,
                 hammer_rob_frame: Frame,
                 mole_rob_frame: Frame,
                 active_mole_height: float,
                 inactive_mole_height: float):
        self._roboter_controller = roboter_controller
        self._mole_controller = mole_controller
        self._hammer_robot = Robot("HammerRobot", hammer_rob_frame)
        self._mole_robot = Robot("MoleRobot", mole_rob_frame)
        self._active_mole_id = -1
        self._active_mole_height = active_mole_height
        self._inactive_mole_height = inactive_mole_height

    async def set_roboter_controller(self, controller: RoboterController) -> None:
        self._roboter_controller = controller

    async def set_mole_controller(self, controller: MoleController) -> None:
        self._mole_controller = controller

    async def connect(self, addr: str = "localhost", port:int = 6106):
        self._reader, self._writer = await asyncio.open_connection(addr, port)
        self._hammer_robot.set_reader(self._reader)
        self._hammer_robot.set_writer(self._writer)
        self._mole_robot.set_reader(self._reader)
        self._mole_robot.set_writer(self._writer)

    async def set_mole(self, mole: Mole) -> None:
        mole_pos = mole.position
        await self._mole_robot.move(Position(mole_pos.x, mole_pos.y, self._inactive_mole_height))
        await self._mole_robot.wait_until_idle()
        await self._mole_robot.move(Position(mole_pos.x, mole_pos.y, self._active_mole_height))
        await self._mole_robot.wait_until_idle()
        self._active_mole_id = mole.mole_id

    async def unset_mole(self, mole: Mole) -> None:
        print(mole.mole_id)
        print(self._active_mole_id)
        if mole.mole_id == self._active_mole_id:
            mole_pos = mole.position
            await self._mole_robot.move(Position(mole_pos.x, mole_pos.y, self._inactive_mole_height))
            await self._mole_robot.wait_until_idle()
            self._active_mole_id = -1

    async def move_tcp(self, pos: Position) -> None:
        await self._hammer_robot.move(pos)
        await self._hammer_robot.wait_until_idle()

    async def get_tcp(self) -> Position:
        return await self._hammer_robot.get_tcp_pos()

    async def get_moles(self) -> List[Mole]:
        return self._mole_controller.moles

    async def notify(self) -> None:
        moles = self._mole_controller.moles
        if len([mole for mole in moles if mole.is_active]) > 1:
            raise Exception("Currently only one active mole at a time possible!")
        for mole in moles:
            if not mole.is_active:
                await self.unset_mole(mole)
        for mole in moles:
            if mole.is_active: 
                await self.set_mole(mole)
        await self._roboter_controller.notify()