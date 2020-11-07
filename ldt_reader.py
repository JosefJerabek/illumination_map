import numpy as np

class LdtReader:
    """ Lumminous intenzity reader 
        reads lumminous intenzity [cd] according to azimut and elevation from LDT format
        provide:
            azimuts [deg]: np.array     - horizontální natočení (do stran) [stupně] rozsah <0, 360)
            elevations [deg]: np.array  - vertikální natočení [stupně] rozsah <0, 90> (0 - pod sebe, 90 - vodorovně)
            intenzity [cd]: np.array    - matice hodnot intezity osvětlení [azimut_index, elevation_index] 
    """
    def __init__(self, filepath):
        rows = LdtReader._load_file(filepath)
        self._interpret_elumdat(rows)

    def _interpret_elumdat(self, lines):
        """ Interpretuje soubor ALUMDAT
        naplní proměnné:
        """
        azimut_count = int(lines[3])
        elevation_count = int(lines[5])
        power = float(lines[28])

        # azimut_axis, elevation_axis, values
        numbers = np.array([float(item) for item in lines[42:]])

        azimuts = numbers[0:azimut_count]
        elevations = numbers[azimut_count:azimut_count+elevation_count]
        values = numbers[azimut_count+elevation_count:]

        meas_azimut_count = int(len(values) / elevation_count)
        matrix = values.reshape((meas_azimut_count, elevation_count))

        if meas_azimut_count != azimut_count:
            # určení typu symetrie
            is_half_symetry = (meas_azimut_count - 1) * 2 == azimut_count
            if is_half_symetry:
                matrix_full = np.zeros((azimut_count, elevation_count))
                # <0, 180>
                matrix_full[:meas_azimut_count] = matrix
                # <180+step, 360-step>
                matrix_full[meas_azimut_count:] = np.flipud(matrix[1:-1])
            else:
                raise Exception("Unknown data symetry")

        self.azimuts = azimuts - 180.0  # TODO why?
        self.elevations = elevations
        self.intenzities = power * matrix_full / 1000.0

    @staticmethod
    def _load_file(path) -> list:
        """ Načte obsah souboru po řádkách do listu """
        with open(path, encoding='cp1250') as f:
            lines = f.read().splitlines()
        lines = [item for item in lines if item]
        return lines