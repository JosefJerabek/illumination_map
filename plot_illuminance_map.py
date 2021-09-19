from typing import Callable, Optional
from numpy import array, meshgrid, empty, transpose
import matplotlib.pyplot as pl


def plot_illuminance_map(
    illum_function: Callable[[float, float], float], 
    x_distances: array, 
    y_distances: array,
    color_levels: Optional[array] = None,
    show: bool = False,
    ):
    """ Plots illuminance map in X, Y plane
    @param illum_function - illum_function(x, y) -> illuminance
    """
    grid_x_distances, grid_y_distances = meshgrid(x_distances, y_distances)
    illuminancies = empty((len(x_distances), len(y_distances)))
    for y_index, y_distance in enumerate(y_distances):
        for x_index, x_distance in enumerate(x_distances):
            illuminance = illum_function(x_distance, y_distance)
            illuminancies[x_index, y_index] = illuminance
    if color_levels is not None:
        pl.contourf(
            grid_x_distances, 
            grid_y_distances, 
            transpose(illuminancies),
            color_levels,
            cmap=pl.cm.get_cmap("jet")
            )
    else:
        pl.contourf(
            grid_x_distances, 
            grid_y_distances, 
            transpose(illuminancies),
            cmap=pl.cm.get_cmap("jet")
            )
    pl.colorbar()
    pl.xlabel("x [m]")
    pl.ylabel("y [m]")
    pl.title("Illuminance [lux]")

    if show:
        pl.show()

