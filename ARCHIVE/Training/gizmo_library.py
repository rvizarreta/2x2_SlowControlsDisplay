from unit_library import UNIT

class GIZMO(UNIT):

    def __init__(self,module_name, unit_name, measurements):
        self.measurements = measurements
        super().__init__(module_name, unit_name)

    # GET METHODS
    def get_measurements(self):
        return self.measurements