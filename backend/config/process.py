from process.traffic_gen import TraficGeneration
from process.coordinator import Coordinator
from process.lights import lights

PROCESS_FCT = [
    TraficGeneration,
    Coordinator,
    lights,
]