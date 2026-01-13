import matplotlib.pyplot as plt

from hermespy.channel import TDL, TDLType
from hermespy.simulation import SimulationScenario, SCIdealChannelEstimation
from hermespy.modem import SimplexLink, RootRaisedCosineWaveform, SCZeroForcingChannelEqualization


# Simulation parameters
device_params = {
    'oversampling_factor': 4,
    'carrier_frequency': 6e9,
    'bandwidth': 960e6,
}

# Initialize a simulation scenario with two devices representing base station and vehicle
scenario = SimulationScenario()
base_station = scenario.new_device(**device_params)
vehicle = scenario.new_device(**device_params)

# Link device and vehicle by a 3GPP TDL type D channel
tdl = TDL(TDLType.D)
scenario.set_channel(base_station, vehicle, tdl)

# Configure a simplex link (transmitting and receiving modem) with
# a root-raised cosine waveform, perfect channel knowledge, and zero-forcing equalization
waveform = RootRaisedCosineWaveform()
waveform.channel_estimation = SCIdealChannelEstimation(tdl, base_station, vehicle)
waveform.channel_equalization = SCZeroForcingChannelEqualization()
link = SimplexLink(waveform=waveform)
link.connect(base_station, vehicle)

# Generate a single scenario drop (all devices transit and receive once)
# Visualize transmission, reception, and equalized symbol constellation
drop = scenario.drop()
drop.device_transmissions[0].mixed_signal.plot(title='Base Station Transmission')
drop.device_receptions[1].impinging_signals[0].plot(title='Vehicle Reception')
drop.device_receptions[1].operator_receptions[0].equalized_symbols.plot_constellation(title='Equalized Symbols')

# Display plots
plt.show()
 