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
scenario = SimulationScenario(seed=42)
base_station = scenario.new_device(**device_params)
vehicle = scenario.new_device(**device_params)

# Specify device trajectories (i.e spatial scenario assumptions)
base_station.trajectory = StaticTrajectory(Transformation.From_Translation([0, 0, 10]))
vehicle.trajectory = StaticTrajectory(Transformation.From_Translation([25, 0, 0]))

# Link the by a 3GPP geometry-base stochastic channel model
# with urban microcell characteristics and line of sight conditions
com_channel = UrbanMicrocells(expected_state=O2IState.LOS)
scenario.set_channel(base_station, vehicle, com_channel)

# Configure a self-interference radar channel on the base station with the vehicle as a target
radar_channel = MultiTargetRadarChannel()
radar_channel.make_target(vehicle, FixedCrossSection(10.0))
scenario.set_channel(base_station, base_station, radar_channel)

# Configure a receiving modem with a 5G NR-like subframe waveform at the vehicle
vehicle_modem = ReceivingModem(waveform=NRSubframe())
vehicle.add_dsp(vehicle_modem)

# Configure a matched filter JCAS DSP at the base station with the same waveform
matched_filter = MatchedFilterJcas(50.0, waveform=NRSubframe(False))
base_station.add_dsp(matched_filter)

# Generate a single scenario drop (all devices transit and receive once)
# Visualize radar range-power profile and equalized symbol constellation at the base station
drop = scenario.drop()
drop.device_receptions[1].operator_receptions[0].equalized_symbols.plot_constellation()
drop.device_receptions[0].operator_receptions[0].cube.plot_range()

# Display plots
plt.show()
