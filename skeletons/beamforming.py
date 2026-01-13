# -*- coding: utf-8 -*-

from scipy.constants import speed_of_light as c0
import matplotlib.pyplot as plt

from hermespy.beamforming import ConventionalBeamformer
from hermespy.core import Transformation
from hermespy.channel import UrbanMacrocells, O2IState
from hermespy.modem import SimplexLink, BitErrorEvaluator, ThroughputEvaluator
from hermespy.simulation import SimulationScenario, DeviceFocus, StaticTrajectory, LinearTrajectory, SimulatedPatchAntenna, SimulatedUniformArray, Simulation, ThermalNoise

from nr_waveform import NRSubframe


# Scenario parameters
numerology_bandwidths = [12 * 15e3 * 2 ** n for n in range(0, 7)]
device_params = {
    'carrier_frequency': 6e9,
    'bandwidth': numerology_bandwidths[1],
    'oversampling_factor': 16,
    'noise_level': ThermalNoise(290),
}

# Build a custom uniform 4x4 MIMO antenna array
array = SimulatedUniformArray(
    SimulatedPatchAntenna,
    .5 * c0 / device_params['carrier_frequency'],
    [1, 4, 4],
)

# Initialize a simulation scenario with two devices representing base station and vehicle


# Specify device trajectories (i.e spatial scenario assumptions)


# Link the by a 3GPP geometry-base stochastic channel model
# with urban macrocell characteristics and line of sight conditions


# Configure a conventional beamformer illuminating the vehicle from the base station


# Configure a simplex link (transmitting and receiving modem) with
# a 5G NR-like subframe waveform


# Generate a single scenario drop (all devices transit and receive once)
# Visualize transmission, reception, and equalized symbol constellation


# Display plots
plt.show()
