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
base_statoion = scenario.new_device(**device_params)
vehicle = scenario.new_device(**device_params)

# Link device and vehicle by a 3GPP TDL type D channel
channel = TDL(TDLType.D, doppler_frequency=14/6e9)
scenario.set_channel(base_statoion, vehicle, channel)

# Configure a simplex link (transmitting and receiving modem) with
# a root-raised cosine waveform, perfect channel knowledge, and zero-forcing equalization
waveform = RootRaisedCosineWaveform()
waveform.channel_estimation = SCIdealChannelEstimation(channel, base_statoion, vehicle)
waveform.channel_equalization = SCZeroForcingChannelEqualization()
link = SimplexLink(waveform=waveform)
link.connect(base_statoion, vehicle)

# Generate a single scenario drop (all devices transit and receive once)
# Visualize transmission, reception, and equalized symbol constellation
drop = scenario.drop()
drop.device_transmissions[0].mixed_signal.plot(title='BS Tx')
drop.device_receptions[1].impinging_signals[0].plot(title='Device Rx')
drop.device_receptions[1].operator_receptions[0].equalized_symbols.plot_constellation(title='Device Rx')

# Display plots
plt.show()
