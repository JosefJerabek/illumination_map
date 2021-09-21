import sys
import os
import matplotlib.pyplot as pl

if __name__ == "__main__":
    sys.path.append(os.getcwd())

import numpy as np

from ldt_reader import LdtReader
from light import Light
from lamp import Lamp
from point import Point3D
from plot_illuminance_map import plot_illuminance_map

LDT_PATH = './ldt/portland/FLD153-D1.ldt'

HEIGHT = 5.0  # lamp height
LIGHT_AZIMUT = -90

x_distances = np.linspace(-5.0, 5.0, 60)  # side
y_distances = np.linspace(-10.0, 10.0, 50)  # front
#x_distances = np.array([0.0])
#y_distances = np.array([-5, -2.5, 0, 2.5, 5, 7.5, 10])

reader = LdtReader(LDT_PATH)
light = Light(reader.azimuts, reader.elevations, reader.intenzities)
#lamp = Lamp(light, Point3D(0.0, 0.0, HEIGHT), LIGHT_AZIMUT, LIGHT_ELEVATION)
#
#if __name__ == "__main__":
#    plot_illuminance_map(
#        lamp.illuminance, 
#        x_distances, 
#        y_distances, 
#        show=True
#    )

def test_elevation():

    def illum_map_elevation(elevation):
        """ Illumination map for specific elevation. """
        lamp = Lamp(light, Point3D(0.0, 0.0, HEIGHT), LIGHT_AZIMUT, elevation)

        plot_illuminance_map(
            lamp.illuminance, 
            x_distances, 
            y_distances,
            color_levels=np.linspace(0, 500, 25),
            title=f"Illumination [lux] (elev={elevation})"
        )

    pl.figure()
    pl.subplot(131)
    illum_map_elevation(-20)
    pl.subplot(132)
    illum_map_elevation(0)
    pl.subplot(133)
    illum_map_elevation(20)
    pl.show()


test_elevation()
