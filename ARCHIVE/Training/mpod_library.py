from unit_library import UNIT

class MPOD(UNIT):

    def __init__(self,module_name, unit_name, measurements, miblib_path):
        self.measurements = measurements
        self.miblib_path = miblib_path
        super().__init__(module_name, unit_name)

    # GET METHODS
    def get_measurements(self):
        return self.measurements