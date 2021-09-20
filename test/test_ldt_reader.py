import sys
import os

if __name__ == "__main__":
    sys.path.append(os.getcwd())

import matplotlib.pyplot as pl
import numpy as np
import unittest
from ldt_reader import LdtReader

#LDT_PATH = './ldt/el-lumen/NITYA XL T5A 47k6 840.LDT'
LDT_PATH = './ldt/cz-modus/CZ-LDT_RX120C90W.ldt'


class TestLdtReader(unittest.TestCase):

    def test_visual(self):
        reader = LdtReader(LDT_PATH)

        grid_azimuts, grid_elevations = np.meshgrid(reader.azimuts, reader.elevations)
        pl.contourf(np.transpose(grid_elevations), np.transpose(grid_azimuts), reader.intenzities)

        pl.colorbar()
        pl.title("Luminous intenzity [cd]")
        pl.xlabel("elevation")
        pl.ylabel("azimut")

        if __name__ == "__main__":
            pl.show()

    def test_azimut_symetry(self):
        """ test symetrie azimutu komem nuly """
        reader = LdtReader(LDT_PATH)
        for azim_index in range(1, len(reader.azimuts)):
            azimut = reader.azimuts[azim_index]
            symetric_azim_index = reader.azimuts.tolist().index(-azimut)
            elevation_index = int(len(reader.elevations) / 2)
            value = reader.intenzities[azim_index, elevation_index]
            symetric_value = reader.intenzities[symetric_azim_index, elevation_index]
            self.assertEqual(value, symetric_value)

if __name__ == '__main__':
    unittest.main()
