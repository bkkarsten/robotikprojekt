from math import sqrt
from datatypes import Position


def calculate_distance(position1: Position, position2: Position) -> float:
    """
    Calculates the Euclidean distance between two positions.
    :param position1: First position (3D)
    :param position2: Second position (3D)
    :return: Euclidean distance as float.
    """
    return sqrt((position1.x - position2.x) ** 2 +
                (position1.y - position2.y) ** 2 +
                (position1.z - position2.z) ** 2)
