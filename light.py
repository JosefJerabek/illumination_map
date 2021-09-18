import numpy as np
from typing import List, Tuple

from point import Point2D


class Light:
    """ 
    From sampled intenzity characteristics
    interpolate whole characteristics in whole space

    note: Better name "EmmitterCharacteristic"
    * azimut is fullrange
    * elevation is aproximated behind bounds <0, 90>
    """

    def __init__(self, azimuts: np.array, elevations: np.array, intenzities: np.array):
        """ 
        :param azimuts: [deg] - measured from front axis, range covers full circle 
        :param elevations: [deg] - angle from down direction
        :param intenzities: [cd] - matrix [azimut, elevation]
        """
        # azimut full range
        assert((azimuts[0] - azimuts[-1]) % 360 == azimuts[1] - azimuts[0])
        assert(intenzities.shape == (len(azimuts), len(elevations)))

        self._azimuts = azimuts
        self._elevations = elevations
        self._intenzities = intenzities

    def intenzity(self, azimut, elevation):
        """ 
        Returns light intenzity for input azimut and elevation. Azimut is not 
        limited. Elevation use bound value if lowest or highes value exceeded.
        :param azimut: [deg] accepts all azimuts (not limited)
        :param elevation: [deg] accepts <-180, 180>
        :returns [cd]
        """

        # range for elevation 
        assert (-180 <= elevation <= 180)
        # azimut not limited, just convert into basic interval <0, 360)
        if elevation < 0:
            elevation = -elevation
            azimut -= 180
        azimut = azimut % 360

        def angle_diff(first, second):
            """ Angle between two azimuts """
            diff = (second - first) % 360
            if diff > 180:
                diff = 360 - diff
            return diff

        def get_azimut_index_pair(azimut_axis: np.array, azimut) -> Tuple[float, float]:
            """
            :param azimut_axis: sorted list of values covering full circle
            """
            penalty_axis = np.abs(azimut_axis - azimut) % 360
            min_index = np.argmin(penalty_axis)
            cindex = lambda x: x % len(azimut_axis)

            if penalty_axis[cindex(min_index-1)] < penalty_axis[cindex(min_index + 1)]:
                return (min_index, cindex(min_index - 1))
            else:
                return (min_index, cindex(min_index + 1))

        def get_elevation_index_pair(elevation_axis: np.array, elevation) -> Tuple[float, float]:
            """
            """
            penalty_axis = np.abs(elevation_axis - elevation)
            min_index = np.argmin(penalty_axis)

            if min_index == 0:
                return (0, None)
            elif min_index == len(elevation_axis) - 1:
                return (min_index, None)
            elif penalty_axis[min_index-1] < penalty_axis[min_index + 1]:
                return (min_index, min_index - 1)
            else:
                return (min_index, min_index + 1)

        def linear_angle_approx(first: Point2D, second: Point2D, x:float) -> float:
            """ Linear approximation from two points """

            point_dx = angle_diff(first.x, second.x)
            dx = angle_diff(first.x, x)
            point_dy = second.y - first.y

            return first.y + dx / point_dx * point_dy

        i_azimut0, i_azimut1 = get_azimut_index_pair(self._azimuts, azimut)
        i_elev0, i_elev1 = get_elevation_index_pair(self._elevations, elevation)

        first = Point2D(self._azimuts[i_azimut0], self._intenzities[i_azimut0, i_elev0])
        second = Point2D(self._azimuts[i_azimut1], self._intenzities[i_azimut1, i_elev0])

        intenzity_elev0 = linear_angle_approx(first, second, azimut)

        if i_elev1:
            first = Point2D(self._azimuts[i_azimut0], self._intenzities[i_azimut0, i_elev1])
            second = Point2D(self._azimuts[i_azimut1], self._intenzities[i_azimut1, i_elev1])

            intenzity_elev1 = linear_angle_approx(first, second, azimut)

            first = Point2D(self._elevations[i_elev0], intenzity_elev0)
            second = Point2D(self._elevations[i_elev1], intenzity_elev1)

            return linear_angle_approx(first, second, elevation)
        else:
            return intenzity_elev0
