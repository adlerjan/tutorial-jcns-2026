# -*- coding: utf-8 -*-

from scipy.constants import speed_of_light as c0
import matplotlib.pyplot as plt

from hermespy.beamforming import ConventionalBeamformer
from hermespy.core import Transformation
from hermespy.channel import UrbanMacrocells, O2IState
from hermespy.modem import SimplexLink, BitErrorEvaluator, ThroughputEvaluator
from hermespy.simulation import DeviceFocus, StaticTrajectory, LinearTrajectory, SimulatedPatchAntenna, SimulatedUniformArray, Simulation, ThermalNoise

from nr_waveform import NRSubframe


# Simulation parameters
numerology_bandwidths = [12 * 15e3 * 2 ** n for n in range(1, 7)]
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

# Initialize a simulation with two devices representing base station and vehicle
simulation = Simulation(num_actors=4)
base_station = simulation.new_device(**device_params, antennas=array)
vehicle = simulation.new_device(**device_params)

# Specify device trajectories (i.e spatial scenario assumptions)
base_station.trajectory = StaticTrajectory(Transformation.From_Translation([0.0, 0.0, 10.0]))
vehicle.trajectory = LinearTrajectory(
    Transformation.From_Translation([100, -25, 1.]),
    Transformation.From_Translation([100, 25, 0.75]),
    4.0,
)

# Link the by a 3GPP geometry-base stochastic channel model
# with urban macrocell characteristics and line of sight conditions
channel = UrbanMacrocells(expected_state=O2IState.LOS)

# Configure a conventional beamformer illuminating the vehicle from the base station
beamformer = ConventionalBeamformer()
beamformer.transmit_focus = DeviceFocus(vehicle)
base_station.transmit_coding[0] = beamformer

# Configure a simplex link (transmitting and receiving modem) with
# a 5G NR-like subframe waveform
waveform = NRSubframe()
link = SimplexLink(waveform=waveform)
link.connect(base_station, vehicle)

# Configure a parameter sweep over all numerology- and order-candidates
simulation.new_dimension('bandwidth', numerology_bandwidths, *simulation.devices, plot_scale='log')
simulation.new_dimension('modulation_order', [4, 16, 64], waveform)

# Evaluate throughput over the parameter sweep
drx = ThroughputEvaluator(link, link, plot_surface=False)
ber = BitErrorEvaluator(link, link, plot_surface=False)
simulation.add_evaluator(drx)
simulation.add_evaluator(ber)

# Run the simulation every .1 seconds
simulation.drop_interval = 1.0
simulation.num_samples = 100
simulation.plot_results = True
simulation.results_dir = simulation.default_results_dir('tutorial', True)
simulation.run()
