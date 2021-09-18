from numpy import array, linspace, arange, meshgrid, empty, transpose, min, max, mean, median
import matplotlib.pyplot as pl
import yaml
import sys
from typing import Tuple

from lamp_area import LampArea, LampPlacement, Point3D


def initialze_from_yaml(config_path) -> Tuple[LampArea, array, array]:

    print(f"Loading configuration from \"{config_path}\"")
    config = yaml.load(open(config_path), Loader=yaml.SafeLoader)

    lamp_placements = [
        LampPlacement(Point3D(item["x"], item["y"], item["z"]), item["azimut"], item["elevation"]) 
        for item in config["lamp_placements"]
        ]
    lamp_area = LampArea(config["ldt_path"], lamp_placements)

    axis = config["x_axis"] 
    x_axis = linspace(axis["start"], axis["stop"], axis["count"])

    axis = config["y_axis"] 
    y_axis = linspace(axis["start"], axis["stop"], axis["count"])
    
    axis = config["illumination_axis"] 
    illumination_axis = linspace(axis["start"], axis["stop"], axis["count"])

    return lamp_area, x_axis, y_axis, illumination_axis


def plot_illuminance(lamp_area: LampPlacement, x_axis: array, y_axis: array, illumination_axis: array):

    x_grid, y_grid = meshgrid(x_axis, y_axis) 
    illuminancies = empty((len(x_axis), len(y_axis)))

    for x_index, x in enumerate(x_axis):
        for y_index, y in enumerate(y_axis):
            illuminance = lamp_area.illuminance(x, y)
            illuminancies[x_index, y_index] = illuminance / 2.0 # TODO - why?

    pl.contourf(
        transpose(x_grid), 
        transpose(y_grid), 
        illuminancies, 
        illumination_axis,
        cmap=pl.cm.get_cmap("jet")
    )

    def get_param_string(illuminancies: array) -> str:
        min_value = int(min(illuminancies))
        max_value = int(max(illuminancies))
        mean_value = int(mean(illuminancies))
        median_value = int(median(illuminancies))
        return f"min={min_value} max={max_value} mean={mean_value} median={median_value}"

    pl.colorbar()
    pl.title(f"Illuminance [lux] ({get_param_string(illuminancies)})")
    pl.xlabel("x [m]")
    pl.ylabel("y [m]")


def print_help():
    print(f"{__file__} [configuration_file]")
    print(f"\tComputes ground light illumination map generated by light source placed in space.")
    print(f"\tconfiguration_file ... lamp and space configuration [default=\"config.yaml\"]")


if len(sys.argv) == 0 or len(sys.argv) > 1:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print_help()
        exit()
    else:
        config_path = sys.argv[1]  

lamp_area, x_axis, y_axis, illumination_axis = initialze_from_yaml(config_path)
plot_illuminance(lamp_area, x_axis, y_axis, illumination_axis)
pl.show()
