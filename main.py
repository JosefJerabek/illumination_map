# for test only
from numpy import linspace, meshgrid, empty, transpose
import matplotlib.pyplot as pl

from lamp_area import LampPlacement, LampArea, Point3D

LDT_PATH = './ldt/el-lumen/NITYA XL T5A 47k6 840.LDT'
# N    x     y     z    elev  azimut
# 1  8.921 16.427 5.000 -8.5  -21.3
# 2 41.079 16.427 5.000 -8.5   21.3
# 3  8.921 33.573 5.000 -8.5  -158.7
# 4 41.079 33.573 5.000 -8.5   158.7
# 5 19.560 16.487 5.000 -10.9  0.4
# 6 30.440 16.487 5.000 -10.9 -0.4
# 7 19.560 33.513 5.000 -10.9  179.6
# 8 30.440 33.513 5.000 -10.9 -179.6

""" Skutečné rozmístění (elevace opačné znaménko) """
lamp_placements = (
    LampPlacement(Point3D( 8.921, 16.427, 5.000), -21.3, 8.5),
    LampPlacement(Point3D(41.079, 16.427, 5.000),  21.3, 8.5),
    LampPlacement(Point3D( 8.921, 33.573, 5.000),-158.7, 8.5),
    LampPlacement(Point3D(41.079, 33.573, 5.000), 158.7, 8.5),
    LampPlacement(Point3D(19.560, 16.487, 5.000),   0.4, 10.9),
    LampPlacement(Point3D(30.440, 16.487, 5.000),  -0.4, 10.9),
    LampPlacement(Point3D(19.560, 33.513, 5.000), 179.6, 10.9),
    LampPlacement(Point3D(30.440, 33.513, 5.000),-179.6, 10.9),
)
lamp_area = LampArea(LDT_PATH, lamp_placements)

x_axis = linspace( 8.9, 41.8, 150)
y_axis = linspace(16.5, 33.6, 100)

x_grid, y_grid = meshgrid(x_axis, y_axis) 
illuminancies = empty((len(x_axis), len(y_axis)))
for x_index, x in enumerate(x_axis):
    for y_index, y in enumerate(y_axis):
        illuminance = lamp_area.illuminance(x, y)
        illuminancies[x_index, y_index] = illuminance

pl.contourf(transpose(x_grid), transpose(y_grid), illuminancies)

pl.colorbar()
pl.title("Illuminance [lux]")
pl.xlabel("x [m]")
pl.ylabel("y [m]")
pl.show()
