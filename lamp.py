""" 
Lamp is light placed in defined hight above ground giving 
illumination to ground points
""" 
from math import sqrt, cos, acos, atan2, degrees, radians, pi

from light import Light
from point import Point3D


class Lamp:

    def __init__(self, 
                light: Light, 
                position: Point3D = (0.0, 0.0, 0.0), 
                azimut: float = 0.0,
                elevation: float = 0.0
                ):
        """ 
        :param position: [m]
        :param azimut: light mounting angle measured from Y axis [deg]
        :param elevation: light mounting angle around X axis [deg]
        """
        self._light = light
        self._position = position
        self._azimut = azimut
        self._elevation = elevation

    def illuminance(self, x: float, y: float):
        """ 
        :param x: [m]
        :param y: [m]
        :return illuminance: [lux = lm/m2]
        """
        x_diff = x - self._position.x 
        y_diff = y - self._position.y 
        azimut = Lamp._compute_azimut(x_diff, y_diff) - self._azimut
        distance = Lamp._compute_distance(x_diff, y_diff, self._position.z)
        elevation = Lamp._compute_elevation(distance, self._position.z)
        radiation_elevation = elevation - self._elevation
        # luminance intenzity I [cd = lm / sr] 
        # illuminance Ev [lux = lm / m2]
        # Ev = I / r^2
        intenzity = self._light.intenzity(azimut, radiation_elevation)
        factor = cos(radians(elevation))
        return factor * intenzity / distance**2

    @staticmethod
    def _compute_azimut(x_diff: float, y_diff: float):
        """ tg(azimut) = x / y
        :return azimut: [deg]
        Note: angle is from axis Y (not x as ordinary)
        """
        azimut_rad = atan2(y_diff, x_diff) - pi/2
        return degrees(azimut_rad)
    
    @staticmethod
    def _compute_distance(x_diff: float, y_diff: float, height: float):
        return sqrt(y_diff**2 + x_diff**2 + height**2)
            
    @staticmethod
    def _compute_elevation(distance: float, height: float):
        elevation_rad = acos(height / distance) 
        return degrees(elevation_rad)