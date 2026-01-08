# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from hermespy.beamforming import ConventionalBeamformer
from hermespy.core import AntennaMode
from hermespy.channel import SingleTargetRadarChannel
from hermespy.radar import Radar
from hermespy.simulation import SimulationScenario, SimulatedCustomArray, SimulatedPatchAntenna, ThermalNoise
from hermespy.simulation.rf.presets.ti.xwr1843 import TIXWR1843

# Configure the device antennas as a 3x4 patch antenna array
antennas = SimulatedCustomArray()
for _ in range(3):
    antennas.add_antenna(SimulatedPatchAntenna(AntennaMode.TX))
for _ in range(4):
    antennas.add_antenna(SimulatedPatchAntenna(AntennaMode.RX))

# Simulation parameters
device_params = {
    'carrier_frequency': 77.5e9,
    'bandwidth': 3e9,
    'antennas': antennas,
    'rf': TIXWR1843(),
    'noise_level': ThermalNoise(290),
}

simulation = SimulationScenario(seed=42)

# Add devices
vehicle = simulation.new_device(**device_params)

# Configure DSP
radar = Radar(device_params['rf'], ConventionalBeamformer())
vehicle.transmitters.add(radar)
vehicle.receivers.add(radar)

# Configure radar channel
radar_channel = SingleTargetRadarChannel(8.0, 1.0, velocity=-10.0)
simulation.set_channel(vehicle, vehicle, radar_channel)

# Generate & visualize a single drop
drop = simulation.drop()
drop.device_transmissions[0].mixed_signal.plot(title='Vehicle Tx RF')
drop.device_receptions[0].baseband_signal.plot(title='Vehicle Rx BB')
drop.device_receptions[0].operator_receptions[0].cube.plot_range_velocity()

plt.show()
