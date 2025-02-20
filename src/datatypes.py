from dataclasses import dataclass, field


@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


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


@dataclass
class Frame:
    position: Position
    orientation: Orientation


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
