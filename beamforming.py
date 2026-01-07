# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

from hermespy.core import Transformation
from hermespy.channel import RuralMacrocells
from hermespy.simulation import StaticTrajectory, LinearTrajectory, SimulationScenario, SimulatedPatchAntenna, SimulatedUniformArray


# Simulation parameters
cf = 26e9
lam = 3e8 / cf
bw = 1e9


# Build custom antenna array
array = SimulatedUniformArray(
    SimulatedPatchAntenna,
    .5 * lam,
    [1, 4, 4],
    Transformation.From_RPY(np.array([0, -.5, 0]), np.zeros(3)),
)
array.plot_topology()

scenario = SimulationScenario()

# Add devices
base_station = scenario.new_device(carrier_frequency=cf, bandwidth=bw, antennas=array)
vehicle = scenario.new_device(carrier_frequency=cf, bandwidth=bw)

# Configure spatial scenario
base_station.trajectory = StaticTrajectory(Transformation.From_Translation([0, 0, 10]))
vehicle.trajectory = LinearTrajectory(
    Transformation.From_Translation([100, 0, 0]),
    Transformation.From_Translation([50, 0, 0]),
    1.0,
)

# Configure channel
scenario.set_channel(base_station, vehicle, RuralMacrocells())




plt.show()