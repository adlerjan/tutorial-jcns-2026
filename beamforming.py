# -*- coding: utf-8 -*-

from scipy.constants import speed_of_light as c0
import matplotlib.pyplot as plt

from hermespy.beamforming import ConventionalBeamformer
from hermespy.fec import RepetitionEncoder, Scrambler3GPP
from hermespy.core import dB, Transformation
from hermespy.channel import UrbanMacrocells, O2IState
from hermespy.modem import SimplexLink, BitErrorEvaluator, ThroughputEvaluator
from hermespy.simulation import DeviceFocus, StaticTrajectory, LinearTrajectory, SimulationScenario, SimulatedPatchAntenna, SimulatedUniformArray, Simulation, ThermalNoise

from nr_waveform import NRSubframe

# Simulation parameters
numerology_bandwidths = [12 * 15e3 * 2 ** n for n in range(0, 7)]
device_params = {
    'carrier_frequency': 6e9,
    'bandwidth': numerology_bandwidths[1],
    'oversampling_factor': 16,
    'noise_level': ThermalNoise(290),
}

# Build custom antenna array
array = SimulatedUniformArray(
    SimulatedPatchAntenna,
    .5 * c0 / device_params['carrier_frequency'],
    [1, 4, 4],
)
# array.plot_topology()
# plt.show()

simulation = Simulation(seed=42)

# Add devices
base_station = simulation.new_device(**device_params, antennas=array)
vehicle = simulation.new_device(**device_params)

# Configure spatial scenario
base_station.trajectory = StaticTrajectory(Transformation.From_Translation([0, 0, 10]))
vehicle.trajectory = LinearTrajectory(
    Transformation.From_Translation([100, -25, 0]),
    Transformation.From_Translation([100, 25, 0]),
    4.0,
)
# simulation.scenario.visualize()
# plt.show()
# exit()

# Configure channel
channel = UrbanMacrocells(expected_state=O2IState.LOS)
simulation.set_channel(base_station, vehicle, channel)

# Configure 5G NR-like OFDM waveform
waveform = NRSubframe()
link = SimplexLink(waveform=waveform)
link.encoder_manager.add_encoder(RepetitionEncoder())
link.encoder_manager.add_encoder(Scrambler3GPP())
link.connect(base_station, vehicle)

# Configure beamforming as a digital transmit beamformer at the BS
beamformer = ConventionalBeamformer()
beamformer.transmit_focus = DeviceFocus(vehicle)
base_station.transmit_coding[0] = beamformer

# Generate & visualize a single drop
#drop = simulation.drop()
#drop.device_transmissions[0].mixed_signal.plot(title='BS Tx')
#drop.device_receptions[1].impinging_signals[0].plot(title='Vehicle Rx')
#drop.device_receptions[1].operator_receptions[0].equalized_symbols.plot_constellation(title='Vehicle Rx')

#plt.show()
#exit()

# Configure a parameter sweep over all numerology- and order-candidates
simulation.new_dimension('bandwidth', numerology_bandwidths, *simulation.devices, plot_scale='log')
simulation.new_dimension('modulation_order', [4, 16, 64], waveform)

# Evaluate throughput over the parameter sweep
drx = ThroughputEvaluator(link, link, plot_surface=False)
ber = BitErrorEvaluator(link, link, plot_surface=False)

simulation.add_evaluator(drx)
simulation.add_evaluator(ber)

# Run the simulation every .1 seconds
simulation.drop_interval = 0.25
simulation.num_samples = 100
result = simulation.run()

# Visualize the throughput results
result.plot()
plt.show()
