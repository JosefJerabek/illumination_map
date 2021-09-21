from dataclasses import dataclass

@dataclass
class Point3D:
    """ Point in 3D space """
    x: float
    y: float
    z: float

@dataclass
class Point2D:
    """ Point in 2D space """
    x: float
    y: float
