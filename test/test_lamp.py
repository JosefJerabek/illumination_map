import sys
import os

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
LIGHT_AZIMUT = 0
LIGHT_ELEVATION = 20

x_distances = np.linspace(-5.0, 5.0, 60)  # side
y_distances = np.linspace(-5.0, 10.0, 50)  # front
# x_distances = np.array([-5, -2, 0, 2, 5])
# y_distances = np.array([-5, -2,  0, 2, 5, 10])

reader = LdtReader(LDT_PATH)
light = Light(reader.azimuts, reader.elevations, reader.intenzities)
lamp = Lamp(light, Point3D(0.0, 0.0, HEIGHT), LIGHT_AZIMUT, LIGHT_ELEVATION)

if __name__ == "__main__":
    plot_illuminance_map(
        lamp.illuminance, 
        x_distances, 
        y_distances, 
        show=True
    )
