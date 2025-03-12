import random
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
        """
        Initializes the MoleController.

        :param moles: List of available moles.
        :param min_waiting_time: Minimum time interval before updating mole positions.
        :param max_waiting_time: Maximum time interval before updating mole positions.
        :param max_moles: Maximum number of active moles.
        :param roboter_interface: Interface for communicating with the simulation.

        :raises ValueError: If input parameters are invalid.
        """

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

    def main_loop(self) -> None:
        """
        Updates mole positions at random intervals within the defined time range.
        """
        while True:
            if len(self._get_active_moles()) >= self._max_moles:
                self._replace_active_mole()
            else:
                self._add_active_mole()
            self._roboter_interface.notify()

    def mole_hit(self, mole: Mole) -> None:
        """
        Handles a hit event for a specific mole.

        :param mole: The mole that was hit.
        """
        pass

    def _replace_active_mole(self) -> None:
        """
        Replaces one active mole with an inactive one.
        """
        active_moles = self._get_active_moles()
        non_active_moles = self._get_non_active_moles()

        new_inactive_mole = self._get_random_element(active_moles)
        new_active_mole = self._get_random_element(non_active_moles)

        if new_inactive_mole:
            new_inactive_mole.is_active = False
        if new_active_mole:
            new_active_mole.is_active = True

    def _add_active_mole(self) -> None:
        """
        Activates a random inactive mole.
        """
        non_active_moles: List[Mole] = self._get_non_active_moles()
        new_active_mole: Mole = self._get_random_element(non_active_moles)
        if new_active_mole:
            new_active_mole.is_active = True

    def _get_active_moles(self) -> List[Mole]:
        """
        Returns a list of currently active moles.

        :return: List of active moles.
        """
        return [mole for mole in self.moles if mole.is_active]

    def _get_non_active_moles(self) -> List[Mole]:
        """
        Returns a list of currently inactive moles.

        :return: List of inactive moles.
        """
        return [mole for mole in self.moles if not mole.is_active]

    @staticmethod
    def _get_random_element(moles: List[Mole]) -> Mole | None:
        """
        Returns a random mole from the given list.

        :param moles: List of moles to choose from.
        :return: A randomly selected mole or None if the list is empty.
        """
        return random.choice(moles) if moles else None
