import asyncio


from datatypes import Mole
from typing import List
from RoboterInterface import RoboterInterface


class MoleController:
    def __init__(self,
                 moles: List[Mole],
                 min_waiting_time: float,
                 max_waiting_time: float,
                 max_moles: int,
                 roboter_interface: RoboterInterface):

        # parameter validation
        if len(moles) == 0:
            raise ValueError('moles must have at least one element')
        if max_moles < 1:
            raise ValueError(f'max_moles must be positive. Actual value {max_moles}')
        if len(moles) < max_moles:
            raise ValueError('Maximum number of moles is higher than the overall number of moles.')

        if min_waiting_time < 0:
            raise ValueError(f'min_waiting_time must be non-negative. Actual value: {min_waiting_time}')
        if max_waiting_time < 0:
            raise ValueError(f'max_waiting_time must be non-negative. Actual value: {max_waiting_time}')
        if min_waiting_time > max_waiting_time:
            swap: float = max_waiting_time
            max_waiting_time = min_waiting_time
            min_waiting_time = swap

        self.moles: List[Mole] = moles
        self._min_waiting_time: float = min_waiting_time
        self._max_waiting_time: float = max_waiting_time
        self._max_moles: int = max_moles
        self._roboter_interface: RoboterInterface = roboter_interface
        self._task: asyncio.Task | None = None

    async def start_routine(self):
        pass
    async def update(self):
        pass

    def mole_hit(self):
        pass
