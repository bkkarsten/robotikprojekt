from dataclasses import dataclass, field
import numpy as np


@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def translate(self, mov: 'Position') -> None:
        self.x += mov.x
        self.y += mov.y
        self.z += mov.z

    def translated(self, mov: 'Position') -> 'Position':
        return Position(self.x + mov.x, self.y + mov.y, self.z + mov.z)
    
    def rotated(self, rot: 'Orientation') -> 'Position': 
        ca, sa = np.cos(np.radians(rot.a)), np.sin(np.radians(rot.a))
        cb, sb = np.cos(np.radians(rot.b)), np.sin(np.radians(rot.b))
        cc, sc = np.cos(np.radians(rot.c)), np.sin(np.radians(rot.c))
        r11 = ca * cb
        r12 = ca * sb * sc - sa * cc
        r13 = ca * sb * cc + sa * sc
        r21 = sa * cb
        r22 = sa * sb * sc + ca * cc
        r23 = sa * sb * cc - ca * sc
        r31 = -sb
        r32 = cb * sc
        r33 = cb * cc
        rotation_matrix = np.array([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])
        position = np.array([self.x, self.y, self.z])
        rotated_position = np.dot(rotation_matrix, position)
        x, y, z = rotated_position
        return Position(x, y, z)
    
    def rotate(self, rot: 'Orientation') -> None:
        rotated = self.rotated(rot)
        self.x, self.y, self.z = rotated.x, rotated.y, rotated.z

    def transformed(self, transformation: 'Frame') -> 'Position':
        return self.rotated(transformation.orientation).translated(transformation.position)
    
    def transform(self, transformation: 'Frame') -> None:
        transformed = self.transformed(transformation)
        self.x, self.y, self.z = transformed.x, transformed.y, transformed.z

    def in_system(self, system: 'Frame') -> 'Position':
        transformation = system.inverse()
        return self.translated(transformation.position).rotated(transformation.orientation)
    
    def __repr__(self):
        return f"{{X {self.x}, Y {self.y}, Z {self.z}}}"

@dataclass
class Orientation:
    _a: float = field(init=False, repr=False)
    _b: float = field(init=False, repr=False)
    _c: float = field(init=False, repr=False)

    def __init__(self, a: float = 0.0, b: float = 0.0, c: float = 0.0):
        self.a = a
        self.b = b
        self.c = c

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, value: float):
        self._validate_value(value, "a")
        self._a = value

    @property
    def b(self) -> float:
        return self._b

    @b.setter
    def b(self, value: float):
        self._validate_value(value, "b")
        self._b = value

    @property
    def c(self) -> float:
        return self._c

    @c.setter
    def c(self, value: float):
        self._validate_value(value, "c")
        self._c = value

    @staticmethod
    def _validate_value(value, name: str):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number, got {type(value).__name__}")
        if not (0.0 <= value < 360):
            raise ValueError(f"{name} must be in range [0, 360). Given: {value}")

    def inverse(self) -> 'Orientation':
        return Orientation((-self.a) % 360.0, 
                           (-self.b) % 360.0, 
                           (-self.c) % 360.0)

    def invert(self) -> None:
        self.a = (-self.a) % 360.0
        self.b = (-self.b) % 360.0
        self.c = (-self.c) % 360.0

    def rotated(self, other: 'Orientation') -> 'Orientation':
        return Orientation((self.a + other.a) % 360.0, 
                           (self.b + other.b) % 360.0, 
                           (self.c + other.c) % 360.0)
    
    def rotate(self, other: 'Orientation') -> None:
        self.a = (self.a + other.a) % 360.0
        self.b = (self.b + other.b) % 360.0
        self.c = (self.c + other.c) % 360.0

    def __repr__(self):
        return f"{{A {self.a}, B {self.b}, C {self.c}}}"

@dataclass
class Frame:
    position: Position
    orientation: Orientation

    def __repr__(self):
        return f"{{X {self.position.x}, Y {self.position.y}, Z {self.position.z}, A {self.orientation.a}, B {self.orientation.b}, C {self.orientation.c}}}"

    def inverse(self) -> 'Frame':
        return Frame(
            Position(-self.position.x, -self.position.y, -self.position.z),
            self.orientation.inverse()
        )
    
    def invert(self) -> None:
        self.position = Position(-self.position.x, -self.position.y, -self.position.z)
        self.orientation.invert()

    def translate(self, mov: Position) -> None:
        self.position.translate(mov)

    def translated(self, mov: Position) -> 'Frame':
        return Frame(
            self.position.translated(mov),
            self.orientation
        )

    def transformed(self, transformation: 'Frame') -> 'Frame':
        translated = self.translated(transformation.position)
        rotated = self.rotated(transformation.orientation)
        return Frame(translated.position, rotated.orientation)

@dataclass
class Mole:
    _mole_id: int = field(init=False, repr=False)
    position: Position
    is_active: bool

    def __init__(self, mole_id: int, position: Position, isActive: bool):
        if mole_id < 0:
            raise ValueError("Id must be non-negative")
        object.__setattr__(self, "_mole_id", mole_id)
        self.position = position
        self.is_active = isActive

    def __repr__(self):
        return f"Mole(id={self.mole_id}, position={self.position}, isActive={self.is_active})"

    @property
    def mole_id(self) -> int:
        return self._mole_id
