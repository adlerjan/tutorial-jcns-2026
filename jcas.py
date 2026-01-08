# -*- coding: utf-8 -*-

from copy import deepcopy
from scipy.constants import speed_of_light as c0
import matplotlib.pyplot as plt

from hermespy.core import Transformation
from hermespy.channel import UrbanMacrocells, O2IState, MultiTargetRadarChannel, PhysicalRadarTarget, FixedCrossSection
from hermespy.modem import ReceivingModem
from hermespy.simulation import StaticTrajectory, LinearTrajectory, SimulationScenario, ThermalNoise
from hermespy.jcas import MatchedFilterJcas

from nr_waveform import NRSubframe

# Simulation parameters
numerology_bandwidths = [12 * 15e3 * 2 ** n for n in range(0, 7)]
device_params = {
    'carrier_frequency': 6e9,
    'bandwidth': numerology_bandwidths[6],
    'oversampling_factor': 16,
    'noise_level': ThermalNoise(290),
}

simulation = SimulationScenario(seed=42)

# Add devices
base_station = simulation.new_device(**device_params)
vehicle = simulation.new_device(**device_params)

# Configure spatial scenario
base_station.trajectory = StaticTrajectory(Transformation.From_Translation([0, 0, 10]))
vehicle.trajectory = StaticTrajectory(Transformation.From_Translation([25, 0, 0]))

# Configure channel
channel = UrbanMacrocells(expected_state=O2IState.LOS)
radar_channel = MultiTargetRadarChannel()
radar_channel.make_target(vehicle, FixedCrossSection(10.0))

simulation.set_channel(base_station, vehicle, channel)
simulation.set_channel(base_station, base_station, radar_channel)

# Configure 5G NR-like OFDM waveform
waveform = NRSubframe()
jcas_dsp = MatchedFilterJcas(200.0, waveform)
rx_modem = ReceivingModem(waveform=waveform)
base_station.add_dsp(jcas_dsp)
vehicle.add_dsp(rx_modem)

# Generate & visualize a single drop
drop = simulation.drop()
drop.device_transmissions[0].mixed_signal.plot(title='BS Tx')
drop.device_receptions[0].operator_receptions[0].cube.plot_range()
drop.device_receptions[1].impinging_signals[0].plot(title='Vehicle Rx')
drop.device_receptions[1].operator_receptions[0].equalized_symbols.plot_constellation(title='Vehicle Rx')

plt.show()
exit()