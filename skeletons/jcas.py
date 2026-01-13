# -*- coding: utf-8 -*-

from scipy.constants import speed_of_light as c0
import matplotlib.pyplot as plt

from hermespy.core import Transformation
from hermespy.channel import UrbanMicrocells, O2IState, MultiTargetRadarChannel, FixedCrossSection
from hermespy.modem import ReceivingModem
from hermespy.simulation import StaticTrajectory, SimulationScenario, ThermalNoise
from hermespy.jcas import MatchedFilterJcas

from nr_waveform import NRSubframe

# Scenario parameters
numerology_bandwidths = [12 * 15e3 * 2 ** n for n in range(0, 7)]
device_params = {
    'carrier_frequency': 6e9,
    'bandwidth': numerology_bandwidths[3],
    'oversampling_factor': 16,
    'noise_level': ThermalNoise(290),
}

# Initialize a simulation scenario with two devices representing base station and vehicle


# Specify device trajectories (i.e spatial scenario assumptions)


# Link the by a 3GPP geometry-base stochastic channel model
# with urban microcell characteristics and line of sight conditions


# Configure a self-interference radar channel on the base station with the vehicle as a target


# Configure a receiving modem with a 5G NR-like subframe waveform at the vehicle


# Configure a matched filter JCAS DSP at the base station with the same waveform


# Generate a single scenario drop (all devices transit and receive once)
# Visualize radar range-power profile and equalized symbol constellation at the base station


# Display plots
plt.show()
