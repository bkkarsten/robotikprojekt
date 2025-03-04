from RoboterInterface import RoboterInterface
from MoleController import MoleController
from RoboterController import RoboterController
from datatypes import Frame, Position, Orientation, Mole
from typing import List
import asyncio
import re

class Robot():
    def __init__(self, id:str, frame:Frame, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._id = id
        self._frame = frame
        self._reader = reader
        self._writer = writer

    async def move(self, pos: Position) -> None:
        """
        Moves the robot in the simulation.

        param pos: The position to move to in the world coordinate system (!).
        """
        pos_in_my_system = pos.in_system(self._frame)
        self._writer.write(f'<MovePTP Pos="{pos_in_my_system}" ID="{self._id}"/>'.encode())
        await self._writer.drain()
        await self._reader.read(200)

    async def _select(self) -> None:
        """
        Selects the robot in the simulation.
        """
        self._writer.write(f'<MovePTP Pos="{{}}" ID="{self._id}"/>'.encode())
        await self._writer.drain()
        await self._reader.read(200)

    async def get_tcp_pos(self) -> Position:
        """
        Gets the position of the robot's tcp in the simulation in the world coordinate system.
        """
        await self._select()
        self._writer.write('<ShowVar Name="$POS_ACT"/>'.encode())
        await self._writer.drain()
        data = str(await self._reader.read(200))
        pattern = r'X ([\d\.\-]+), Y ([\d\.\-]+), Z ([\d\.\-]+)'
        match = re.search(pattern, data)
        if not match: 
            return None
        values = list(map(float, match.groups()))
        if len(values) != 3:
            return None
        pos = Position(*values)
        pos_in_world = pos.transformed(self._frame)
        return pos_in_world
        
    
    async def is_moving(self) -> bool:
        """
        Returns whether the robot is currently moving.
        """
        await self._select()
        pos1 = await self.get_tcp_pos()
        await asyncio.sleep(0.1)
        pos2 = await self.get_tcp_pos()
        return pos1 != pos2
    
    async def wait_until_idle(self,
                             wait_interval: float = 0.3) -> None:
        """
        Waits until the robot is not moving anymore.
        """
        await self._select()
        while True:
            await asyncio.sleep(wait_interval)
            if not await self.is_moving():
                break

class Communicator(RoboterInterface):
    def __init__(self,
                 mole_controller: MoleController | None,
                 roboter_controller: RoboterController | None,
                 hammer_rob_frame: Frame,
                 mole_rob_frame: Frame,
                 active_mole_height: float,
                 inactive_mole_height: float,
                 addr: str = "localhost",
                 port:int = 6106):
        self._roboter_controller = roboter_controller
        self._mole_controller = mole_controller
        asyncio.run(self._connect())
        self._hammer_robot = Robot("HammerRobot", hammer_rob_frame, self._reader, self._writer)
        self._mole_robot = Robot("MoleRobot", mole_rob_frame)
        self._active_mole_id = -1

    async def _connect(self):
        self._reader, self._writer = await asyncio.open_connection(self.addr, self.port)

    async def set_mole(self, mole: Mole) -> None:
        mole_pos = mole.position
        await self._mole_robot.move(Position(mole_pos.x, mole_pos.y, self._active_mole_heigt))
        await self._mole_robot.wait_until_idle()
        self._active_mole_id = mole.mole_id

    async def unset_mole(self, mole: Mole) -> None:
        if mole.mole_id == self._active_mole_id:
            mole_pos = mole.position
            await self._mole_robot.move(Position(mole_pos.x, mole_pos.y, self._inactive_mole_heigt))
            await self._mole_robot.wait_until_idle()
            self._active_mole_id = -1

    async def move_tcp(self, pos: Position) -> None:
        await self._hammer_robot.move(pos)
        await self._hammer_robot.wait_until_idle()

    async def get_tcp(self) -> Position:
        return await self._hammer_robot.get_tcp_pos()

    async def get_moles(self) -> List[Mole]:
        return await self._mole_controller.moles

    async def notify(self) -> None:
        moles = self._mole_controller.moles
        if len([mole for mole in moles if mole.is_active]) > 1:
            raise Exception("Currently only one active mole at a time possible!")
        for mole in moles:
            if mole.is_active:
                self.set_mole(mole)
            else: 
                self.unset_mole(mole)
        await self._roboter_controller.notify()