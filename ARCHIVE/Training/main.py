from unit_library import UNIT
from mpod_library import MPOD
from gizmo_library import GIZMO

mpod0 = MPOD("module0", "mpod0", ['Voltage', 'Current'], "/miblib")
gizmo = GIZMO("module0", "gizmo", ["Resistance", "Temperature"])
print(mpod0.get_unit_name())
print(gizmo.get_unit_name())
print(mpod0.get_measurements())
print(gizmo.get_measurements())