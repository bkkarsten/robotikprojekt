import socket
import time
from datatypes import Frame, Position
import re


class Robot:
    def __init__(self, id: str, frame: "Frame", host: str, port: int):
        """
        Robot constructor.

        :param frame: The robot's position and rotation relative to WORLD.
        :param host: The IP address of the robot controller.
        :param port: The TCP port number.
        """
        self._id = id
        self._frame = frame
        self._host = host
        self._port = port
        self._socket = None

    def connect(self):
        """Establish a TCP connection to the robot."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

    def disconnect(self):
        """Close the TCP connection."""
        if self._socket:
            self._socket.close()
            self._socket = None

    def _send(self, message: str) -> None:
        """Send a message over the TCP connection."""
        if not self._socket:
            raise ConnectionError("Not connected to the robot.")
        self._socket.sendall(message.encode())

    def _receive(self, buffer_size: int = 300) -> str:
        """Receive data from the TCP connection."""
        if not self._socket:
            raise ConnectionError("Not connected to the robot.")
        return self._socket.recv(buffer_size).decode()

    def move(self, pos: Position) -> None:
        """
        Moves the robot in the simulation.

        param pos: The position to move to in the world coordinate system (!).
        """
        pos_in_my_system = pos.in_system(self._frame)
        command = f'<MovePTP Pos="{pos_in_my_system}" ID="{self._id}"/>'
        self._send(command)
        self._receive()

    def _select(self) -> None:
        """
        Selects the robot in the simulation.
        """
        command = f'<MovePTP Pos="{{}}" ID="{self._id}"/>'
        self._send(command)
        self._receive()

    def get_tcp_pos(self) -> Position:
        """
        Gets the position of the robot's tcp in the simulation in the world coordinate system.
        """
        self._select()
        self._send('<ShowVar Name="$POS_ACT"/>')
        data = self._receive()

        pattern = r'X ([\d\.\-]+), Y ([\d\.\-]+), Z ([\d\.\-]+)'
        match = re.search(pattern, data)
        if not match:
            return None

        values = list(map(float, match.groups()))
        if len(values) != 3:
            return None

        pos = Position(*values)
        return pos.transformed(self._frame)
        
    def is_moving(self, epsilon=0.0001) -> bool:
        """
        Returns whether the robot is currently moving.
        """
        self._select()
        pos1 = self.get_tcp_pos()
        time.sleep(0.1)
        pos2 = self.get_tcp_pos()

        return (
                abs(pos1.x - pos2.x) > epsilon or
                abs(pos1.y - pos2.y) > epsilon or
                abs(pos1.z - pos2.z) > epsilon
        )

    def _is_moving(self) -> bool:
        """
        Returns whether the robot is currently moving, assuming it is already selected.
        """
        pos1 = self.get_tcp_pos()
        time.sleep(0.1)
        pos2 = self.get_tcp_pos()
        return pos1 != pos2

    def wait_until_idle(self, wait_interval: float = 0.3) -> None:
        """
        Waits until the robot is not moving anymore.
        """
        self._select()
        while True:
            time.sleep(wait_interval)
            if not self._is_moving():
                break
