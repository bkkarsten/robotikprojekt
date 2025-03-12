import asyncio
from datatypes import Frame, Position, Orientation
import re

class Robot():
    def __init__(self, id:str, 
                 frame:Frame, 
                 reader: asyncio.StreamReader | None = None, 
                 writer: asyncio.StreamWriter | None = None):
        """
        Robot constructor.
        
        param frame: The robots position and rotation relative to WORLD
        """
        self._id = id
        self._frame = frame
        self._reader = reader
        self._writer = writer

    def set_reader(self, reader: asyncio.StreamReader) -> None:
        self._reader = reader

    def set_writer(self, writer: asyncio.StreamWriter) -> None:
        self._writer = writer

    async def move(self, pos: Position) -> None:
        """
        Moves the robot in the simulation.

        param pos: The position to move to in the world coordinate system (!).
        """
        pos_in_my_system = pos.in_system(self._frame)
        self._writer.write(f'<MovePTP Pos="{pos_in_my_system}" ID="{self._id}"/>'.encode())
        await self._writer.drain()
        await self._reader.read(300)

    async def _select(self) -> None:
        """
        Selects the robot in the simulation.
        """
        self._writer.write(f'<MovePTP Pos="{{}}" ID="{self._id}"/>'.encode())
        await self._writer.drain()
        await self._reader.read(300)

    async def get_tcp_pos(self) -> Position:
        """
        Gets the position of the robot's tcp in the simulation in the world coordinate system.
        """
        await self._select()
        self._writer.write('<ShowVar Name="$POS_ACT"/>'.encode())
        await self._writer.drain()
        data = str(await self._reader.read(300))
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
        
    
    async def is_moving(self, epsilon=0.0001) -> bool:
        """
        Returns whether the robot is currently moving.
        """
        await self._select()
        pos1 = await self.get_tcp_pos()
        await asyncio.sleep(0.1)
        pos2 = await self.get_tcp_pos()
        return abs(pos1.x - pos2.x > epsilon) or abs(pos1.y - pos2.y > epsilon) or abs(pos1.z - pos2.z > epsilon)
    
    async def _is_moving(self) -> bool:
        """
        Returns whether the robot is currently moving, assuming the robot is already selected.
        """
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
            if not await self._is_moving():
                break