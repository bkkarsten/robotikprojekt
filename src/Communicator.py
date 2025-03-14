from RoboterInterface import RoboterInterface
from MoleController import MoleController
from RoboterController import RoboterController
from datatypes import Frame, Position, Orientation, Mole
from typing import List
import socket
from Robot import Robot
from constants import *


class Communicator(RoboterInterface):
    def __init__(self,
                 mole_controller: MoleController | None,
                 roboter_controller: RoboterController | None,
                 hammer_rob_frame: Frame,
                 mole_rob_frame: Frame,
                 active_mole_height: float,
                 inactive_mole_height: float,
                 host: str = '127.0.0.1',
                 port: int = 6106
                 ):
        self._host = host
        self._port = port
        self._roboter_controller = roboter_controller
        self._mole_controller = mole_controller
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self._hammer_robot = Robot("HammerRobot", hammer_rob_frame, sock=self._socket)
        self._hammer_robot_home: Position = Position(HOLE_0_X - HOLE_DIST, HOLE_0_Y + HOLE_DIST, HAMMER_HOME_HEIGHT)
        self._mole_robot = Robot("MoleRobot", mole_rob_frame, sock=self._socket)
        self._active_mole_id = -1
        self._active_mole_height = active_mole_height
        self._inactive_mole_height = inactive_mole_height

    def set_roboter_controller(self, controller: RoboterController) -> None:
        self._roboter_controller = controller

    def set_mole_controller(self, controller: MoleController) -> None:
        self._mole_controller = controller

    def set_mole(self, mole: Mole) -> None:
        mole_pos = mole.position
        self._mole_robot.move(Position(mole_pos.x, mole_pos.y, self._inactive_mole_height))
        self._mole_robot.wait_until_idle()
        self._mole_robot.move(Position(mole_pos.x, mole_pos.y, self._active_mole_height))
        self._mole_robot.wait_until_idle()
        self._active_mole_id = mole.mole_id

    def unset_mole(self, mole: Mole) -> None:
        if mole.mole_id == self._active_mole_id:
            mole_pos = mole.position
            self._mole_robot.move(Position(mole_pos.x, mole_pos.y, self._inactive_mole_height))
            self._mole_robot.wait_until_idle()
            self._active_mole_id = -1

    def move_tcp(self, pos: Position, return_home: bool = False) -> None:
        self._hammer_robot.move(pos)
        self._hammer_robot.wait_until_idle()

        if return_home:
            self._hammer_robot.move(self._hammer_robot_home)
            self._hammer_robot.wait_until_idle()

    def get_tcp(self) -> Position:
        return self._hammer_robot.get_tcp_pos()

    def get_moles(self) -> List[Mole]:
        return self._mole_controller.moles

    def notify(self) -> None:
        moles = self._mole_controller.moles
        if len([mole for mole in moles if mole.is_active]) > 1:
            raise Exception("Currently only one active mole at a time possible!")
        for mole in moles:
            if not mole.is_active:
                self.unset_mole(mole)
        for mole in moles:
            if mole.is_active: 
                self.set_mole(mole)
        self._roboter_controller.notify()
