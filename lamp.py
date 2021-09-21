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
            T = array([
                [cos(angle_rad), -sin(angle_rad), 0, 0],
                [sin(angle_rad),  cos(angle_rad), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            point_rot = matmul(T, transpose(point_ext))
            return point_rot[0:3]

        def rotate_x(point_xyz: array, angle_rad: float) -> array:
            """ Transform coordinates into coord system rotated around z axis """
            point_ext = array([point_xyz[0], point_xyz[1], point_xyz[2], 1])
            T = array([
                [1, 0, 0, 0],
                [0, cos(angle_rad), -sin(angle_rad),  0],
                [0, sin(angle_rad),  cos(angle_rad),  0],
                [0, 0, 0, 1]
            ])
            point_rot = matmul(T, transpose(point_ext))
            return point_rot[0:3]

        # 1 - souřadnice vůči systému se středem v lampě (x_diff, y_diff, -height)
        coord_lamp = array([x - self._position.x, y - self._position.y, -self._position.z])
        coord_zrot = rotate_z(coord_lamp, self._azimut - degrees(pi/2))
        coord_rot = rotate_x(coord_zrot, self._elevation)

        # 2 - transformace souřadnice do nového XYZ systému
        #   https://syzpc.ru/cs/electrical-equipment-and-electricity/matrica-povorota-sistemy-koordinat-matrica-povorota-v-dvumernom/
        #   see https://saint-paul.fjfi.cvut.cz/base/sites/default/files/POGR/POGR2/07.maticove_transformace.pdf
        #   * azimut - rotace kolem osy Z - určení souřadnice v souřadnicovém systému pootočeném kolem osy Z
        #   * elevace - rotace kolem osy X
        # 3 - z nových souřadnic (x, y, z) určit azimut a elevaci
        # 4 - dopočítat osvětlení
        dx, dy, dz = coord_rot[0], coord_rot[1], coord_rot[2]
        azimut_rad = compute_azimut_rad(dx, dy)
        distance = compute_distance(dx, dy, dz)
        elevation = degrees(compute_elevation_rad(distance, self._position.z))
        radiation_elevation = degrees(compute_elevation_rad(distance, dz))
        # just guessing
        radiation_elevation = elevation - cos(radians(azimut_rad - self._azimut)) * self._elevation
        # TODO - azimut is also changing
        # luminance intenzity I [cd = lm / sr]
        # illuminance Ev [lux = lm / m2]
        # Ev = I / r^2
        intenzity = self._light.intenzity(degrees(azimut_rad), radiation_elevation)
        factor = cos(radians(elevation))
        return factor * intenzity / distance**2

