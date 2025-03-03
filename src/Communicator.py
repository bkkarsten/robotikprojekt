from RoboterInterface import RoboterInterface
from MoleController import MoleController
from RoboterController import RoboterController
from datatypes import Frame, Position, Orientation, Mole
from typing import List
import asyncio
import re

class Robot():
    def __init__(self, id:str, frame:Frame):
        self._id = id
        self._frame = frame

    async def move(self, frame: Frame, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        Moves the robot in the simulation.
        """
        writer.write(f'<MoveLIN Pos="{frame}" ID="{self._id}"/>'.encode())
        await writer.drain()
        await reader.read(200)

    async def get_frame(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> Frame:
        """
        Gets the frame of the robot's tcp in the simulation.

        !!! WARNING !!! Due to limits in the TCP interface, this will currently always get the 
        frame of the active robot, not necessarily this one.
        """
        writer.write('<ShowVar Name="$POS_ACT"/>'.encode())
        await writer.drain()
        data = str(await reader.read(200))
        pattern = r'X ([\d\.\-]+), Y ([\d\.\-]+), Z ([\d\.\-]+), A ([\d\.\-]+), B ([\d\.\-]+), C ([\d\.\-]+)'
        match = re.search(pattern, data)
        if match:
            values = list(map(float, match.groups()))
            return Frame(Position(*values[:3]), Orientation(*values[3:]))
        else:
            return None
        
    async def get_pos(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> Position:
        """
        Gets the position of the robot's tcp in the simulation.

        !!! WARNING !!! Due to limits in the TCP interface, this will currently always get the 
        position of the active robot, not necessarily this one.
        """
        return (await self.get_frame(reader, writer)).position
    
    async def get_rot(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> Orientation:
        """
        Gets the orientation of the robot's tcp in the simulation.

        !!! WARNING !!! Due to limits in the TCP interface, this will currently always get the 
        orientation of the active robot, not necessarily this one.
        """
        return (await self.get_frame(reader, writer)).orientation
    
    async def is_moving(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
        """
        Returns whether the robot is currently moving.

        !!! WARNING !!! Due to limits in the TCP interface, this will currently always get the
        moving status of the active robot, not necessarily this one.
        """
        pos1 = await self.get_pos(reader, writer)
        pos2 = await self.get_pos(reader, writer)
        return pos1 != pos2
    
    async def wait_for_move_completed(self, 
                                      frame: Frame, 
                                      reader: asyncio.StreamReader, 
                                      writer: asyncio.StreamWriter,
                                      wait_interval: float = 0.3) -> None:
        """
        Moves the robot and waits until it has finished moving.

        !!! WARNING !!! Due to limits in the TCP interface, this will currently check for the 
        moving status of the active robot, not necessarily this one.
        """
        await self.move(frame, reader, writer)
        while True:
            await asyncio.sleep(wait_interval)
            if not await self.is_moving(reader, writer):
                break

class Communicator(RoboterInterface):
    def __init__(self,
                 mole_controller: MoleController | None,
                 roboter_controller: RoboterController | None,
                 mole_rob_frame: Frame,
                 hammer_rob_frame: Frame,
                 addr: str = "localhost",
                 port:int = 6106):
        self._roboter_controller = roboter_controller
        self._mole_controller = mole_controller
        asyncio.run(self._connect())

    async def _connect(self):
        self._reader, self._writer = await asyncio.open_connection(self.addr, self.port)

    async def set_mole(self, mole: Mole) -> None:
        pass

    async def unset_mole(self, mole: Mole) -> None:
        pass

    async def move_tcp(self, frame: Frame) -> None:
        pass

    async def get_tcp(self) -> Frame:
        return Frame()

    async def get_moles(self) -> List[Mole]:
        return await self._mole_controller.moles

    async def notify(self) -> None:
        await self._roboter_controller.notify()