import sys
import os

if __name__ == "__main__":
    sys.path.append(os.getcwd())

import matplotlib.pyplot as pl
import numpy as np


from ldt_reader import LdtReader
from light import Light
from lamp import Lamp
from point import Point3D


LDT_PATH = './ldt/el-lumen/NITYA XL T5A 47k6 840.LDT'
HEIGHT = 5.0  # lamp height
LIGHT_AZIMUT = 0

y_distances = np.linspace(0.0, 10.0, 400)  # front
x_distances = np.linspace(-5.0, 5.0, 300)  # side

reader = LdtReader(LDT_PATH)
light = Light(reader.azimuts, reader.elevations, reader.intenzities)
lamp = Lamp(light, Point3D(1.0, 1.0, HEIGHT), LIGHT_AZIMUT)

grid_y_distances, grid_x_distances = np.meshgrid(y_distances, x_distances)
illuminancies = np.empty((len(y_distances), len(x_distances)))
for y_index, y_distance in enumerate(y_distances):
    for x_index, x_distance in enumerate(x_distances):
        illuminance = lamp.illuminance(y_distance, x_distance)
        illuminancies[y_index, x_index] = illuminance

#print(illuminancies)

pl.contourf(np.transpose(grid_x_distances), np.transpose(grid_y_distances), illuminancies)

pl.colorbar()
pl.title("Illuminance [lux]")
pl.xlabel("x [m]")
pl.ylabel("y [m]")

if __name__ == "__main__":
    pl.show()
