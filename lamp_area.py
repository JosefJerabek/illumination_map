from numpy import array
from dataclasses import dataclass
from typing import List

from point import Point3D
from ldt_reader import LdtReader
from light import Light
from lamp import Lamp


@dataclass
class LampPlacement:
    position: Point3D
    azimut: float  # [deg] light mounting azimut
    elevation: float # [deg]


class LampArea:
    """ Set of placed lamps """

    def __init__(self, lamp_ldt_path: str, lamp_placements: List[LampPlacement]):
        reader = LdtReader(lamp_ldt_path)
        light = Light(reader.azimuts, reader.elevations, reader.intenzities)
        self._lamps = [Lamp(light, p.position, p.azimut, p.elevation) for p in lamp_placements]

    def illuminance(self, x: float, y: float):
        """ 
        :return illuminance: [lux]
        """
        illuminance = sum([lamp.illuminance(x,y) for lamp in self._lamps])
        return illuminance