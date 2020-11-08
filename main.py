# for test only
from numpy import linspace, meshgrid, empty, transpose
import matplotlib.pyplot as pl
import yaml

from lamp_area import LampPlacement, LampArea, Point3D

config = yaml.load(open("config.yaml"))

# TODO def
lamp_placements = [
    LampPlacement(Point3D(item["x"], item["y"], item["z"]), item["azimut"], item["elevation"]) 
    for item in config["lamp_placements"]
    ]
lamp_area = LampArea(config["ldt_path"], lamp_placements)
axis = config["x_axis"] 
x_axis = linspace(axis["start"], axis["stop"], axis["count"])
axis = config["y_axis"] 
y_axis = linspace(axis["start"], axis["stop"], axis["count"])

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
