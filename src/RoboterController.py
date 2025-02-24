from typing import List
from datatypes import Frame, Position, Orientation, Mole
import geometry
from RoboterInterface import RoboterInterface


class RoboterController:
    """
    Controls the movement of the robot via an implementation of the RoboterInterface.
    """
    def __init__(self, roboter_interface: RoboterInterface):
        """
        :param roboter_interface: Implementation of the RoboterInterface base class.
        """
        self._target: Frame = Frame(Position(0, 0, 0), Orientation(0, 0, 0))
        self._roboter_interface = roboter_interface

    async def notify(self) -> None:
        """
        If this method is called, a new target frame is calculated based on the current tcp and active moles.
        The new tcp position is then sent to the robot.
        """
        _target = await self._calculate_target()
        await self._roboter_interface.move_tcp(_target)

    async def _calculate_target(self) -> Frame:
        """
        Calculates new target frame based on the current tcp and active moles.
        :returns: new target frame
        """
        active_moles: List[Mole] = await self._get_active_moles()
        target_mole: Mole = await self._get_closest_mole(active_moles)
        return Frame(position=target_mole.position, orientation=Orientation(0, 0, 0))

    async def _get_active_moles(self) -> List[Mole]:
        """
        Checks which moles are currently active.
        :returns: active moles as a list
        """
        moles: List[Mole] = await self._roboter_interface.get_moles()
        return [mole for mole in moles if mole.is_active]

    async def _get_closest_mole(self, moles: List[Mole]) -> Mole:
        """
        Calculates the closest mole to current tcp.
        :param moles: list of active moles
        :return:
        """
        tcp: Frame = await self._roboter_interface.get_tcp()
        return min(moles, key=lambda mole: geometry.calculate_distance(tcp.position, mole.position))
