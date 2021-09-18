import sys
import os

if __name__ == "__main__":
    sys.path.append(os.getcwd())

import matplotlib.pyplot as pl
# import unittest

from numpy import array, linspace, transpose, meshgrid, empty, amax

from ldt_reader import LdtReader
from light import Light

#LDT_PATH = './ldt/el-lumen/NITYA XL T5A 47k6 840.LDT'
LDT_PATH = './ldt/portland/FLD153-D1.ldt'
#LDT_PATH = './ldt/cz-modus/CZ-LDT_RX120C90W.ldt'


class TestLight:#(unittest.TestCase):

    def test_visual_fullranges(self):
        """
        Visual test in over full range. 
        """
        COL_COUNT = 30

        azimuts = linspace(-360, 360, 200)
        elevations = linspace(-180, 180, 120)
        intenzities = self._intenzity_matrix(azimuts, elevations)
        color_levels = linspace(0, amax(intenzities), COL_COUNT)
        grid_azimuts, grid_elevations = meshgrid(azimuts, elevations)
        pl.contourf(transpose(grid_elevations), transpose(grid_azimuts), intenzities, color_levels)

        pl.colorbar()
        pl.title("Luminous intenzity on the ground [cd] (full range)")
        pl.xlabel("elevation [deg]")
        pl.ylabel("azimut [deg]")
        #if __name__ == '__main__':
        pl.show()

    def test_azimut_symetry(self):
        azimut = 53
        symetric_azimut = -azimut
        elevation = 10
        
        reader = LdtReader(LDT_PATH)
        light = Light(reader.azimuts, reader.elevations, reader.intenzities)
        
        intenzity = light.intenzity(azimut, elevation)
        symetric_intenzity = light.intenzity(symetric_azimut, elevation)
        self.assertEqual(intenzity, symetric_intenzity)

    def test_different(self):
        azimut = 53
        other_azimut = 180
        elevation = 10
        
        reader = LdtReader(LDT_PATH)
        light = Light(reader.azimuts, reader.elevations, reader.intenzities)
        
        intenzity = light.intenzity(azimut, elevation)
        other_intenzity = light.intenzity(other_azimut, elevation)
        self.assertNotEqual(intenzity, other_intenzity)
    
    @staticmethod
    def _intenzity_matrix(azimuts: array, elevations: array) -> array:
        """ :return intenzity[azimut, elevation]: [lux] """
        reader = LdtReader(LDT_PATH)
        light = Light(reader.azimuts, reader.elevations, reader.intenzities)
        
        intenzities = empty((len(azimuts), len(elevations)))
        for az_index, azimut in enumerate(azimuts):
            for el_index, elevation in enumerate(elevations):
                intenzity = light.intenzity(azimut, elevation)
                intenzities[az_index, el_index] = intenzity
        
        return intenzities

if __name__ == '__main__':
    test = TestLight()
    test.test_visual_fullranges()
    #unittest.main()
    