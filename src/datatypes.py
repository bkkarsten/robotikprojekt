from dataclasses import dataclass, field


@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Orientation:
    _A: float = field(init=False, repr=False)
    _B: float = field(init=False, repr=False)
    _C: float = field(init=False, repr=False)

    def __init__(self, A: float = 0.0, B: float = 0.0, C: float = 0.0):
        self.A = A
        self.B = B
        self.C = C

    @property
    def A(self) -> float:
        return self._A

    @A.setter
    def A(self, value: float):
        self._validate_value(value, "A")
        self._A = value

    @property
    def B(self) -> float:
        return self._B

    @B.setter
    def B(self, value: float):
        self._validate_value(value, "B")
        self._B = value

    @property
    def C(self) -> float:
        return self._C

    @C.setter
    def C(self, value: float):
        self._validate_value(value, "C")
        self._C = value

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
    id: int
    position: Position
    isActive: bool
