"""
Lamp is light placed in defined hight above ground giving
illumination to ground points
"""

from math import sqrt, sin, cos, acos, atan2, degrees, radians, pi
from numpy import array, matmul, transpose

from light import Light
from point import Point3D


class Lamp:

    def __init__(self,
                 light: Light,
                 position: Point3D = Point3D(0.0, 0.0, 0.0),
                 azimut_deg: float = 0.0,
                 elevation_deg: float = 0.0
                 ):
        """
        :param position: [m]
        :param azimut [deg] - light azimut counterclockwise from light front direction
                       (-90 .. right, 0 .. front, 90 .. left)"
  
        :param elevation [deg] - light elevation
                          (0 - standard mounting, positive - lighten longer distance, negative - shorter)

        """
        self._light = light
        self._position = position
        self._azimut_deg = azimut_deg
        self._elevation_deg = elevation_deg

    def illuminance(self, x: float, y: float):
        """
        :param x: [m]
        :param y: [m]
        :return illuminance: [lux = lm/m2]
        """

        def compute_azimut_rad(x_diff: float, y_diff: float):
            """ tg(azimut) = x / y
            :return azimut: [rad]
            Note: angle is from axis Y (not x as ordinary)
            """
            return atan2(y_diff, x_diff) - pi/2

        def compute_distance(x_diff: float, y_diff: float, height: float):
            return sqrt(y_diff**2 + x_diff**2 + height**2)

        def compute_elevation_rad(distance: float, height: float):
            return acos(height / distance)

        def rotate_z(point_xyz: array, angle_rad: float) -> array:
            """ Transform coordinates into coord system rotated around z axis """
            point_ext = array([point_xyz[0], point_xyz[1], point_xyz[2], 1])
            TMx = array([
                [cos(angle_rad), -sin(angle_rad), 0, 0],
                [sin(angle_rad),  cos(angle_rad), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            point_rot = matmul(TMx, transpose(point_ext))
            return point_rot[0:3]

        def rotate_x(point_xyz: array, angle_rad: float) -> array:
            """ Transform coordinates into coord system rotated around z axis """
            point_ext = array([point_xyz[0], point_xyz[1], point_xyz[2], 1])
            TMx = array([
                [1, 0, 0, 0],
                [0, cos(angle_rad), -sin(angle_rad),  0],
                [0, sin(angle_rad),  cos(angle_rad),  0],
                [0, 0, 0, 1]
            ])
            point_rot = matmul(TMx, transpose(point_ext))
            return point_rot[0:3]

        #   see https://saint-paul.fjfi.cvut.cz/base/sites/default/files/POGR/POGR2/07.maticove_transformace.pdf
        point_pos = array([x - self._position.x, y - self._position.y, -self._position.z])
        point_pos_zrot = rotate_z(point_pos, -radians(self._azimut_deg))
        point_pos_rot = rotate_x(point_pos_zrot, -radians(self._elevation_deg))

        dx, dy, dz = point_pos_rot[0], point_pos_rot[1], point_pos_rot[2]
        azimut_rad = compute_azimut_rad(dx, dy)
        distance = compute_distance(dx, dy, dz)
        elevation_rad = compute_elevation_rad(distance, self._position.z)
        radiation_elevation = degrees(compute_elevation_rad(distance, -dz))

        # luminance intenzity I [cd = lm / sr]
        # illuminance Ev [lux = lm / m2]
        # Ev = I / r^2
        intenzity = self._light.intenzity(degrees(azimut_rad), radiation_elevation)
        factor = cos(elevation_rad)
        return factor * intenzity / distance**2
