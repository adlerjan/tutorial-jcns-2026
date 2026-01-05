import matplotlib.pyplot as plt

from hermespy.channel import TDL
from hermespy.simulation import SimulationScenario, SCIdealChannelEstimation
from hermespy.modem import SimplexLink, RootRaisedCosineWaveform, SCZeroForcingChannelEqualization

# Simulation parameters
cf = 6e9
bw = 1e9

# Create a simulation scenario
scenario = SimulationScenario()

# Add a new device
base_station = scenario.new_device(carrier_frequency=cf, bandwidth=bw)
vehicle = scenario.new_device(carrier_frequency=cf, bandwidth=bw)

# Configure channel
channel = TDL()
scenario.set_channel(base_station, vehicle, channel)

# Add DSP
waveform = RootRaisedCosineWaveform(roll_off=.9)
waveform.channel_estimation = SCIdealChannelEstimation(channel, base_station, vehicle)
waveform.channel_equalization = SCZeroForcingChannelEqualization()
dsp = SimplexLink(waveform=waveform)
dsp.connect(base_station, vehicle)


# Generate & visualize a single drop
drop = scenario.drop()
drop.device_transmissions[0].mixed_signal.plot(title='BS Tx')
drop.device_receptions[1].impinging_signals[0].plot(title='Vehicle Rx')
drop.device_receptions[1].operator_receptions[0].equalized_symbols.plot_constellation(title='Vehicle Rx')

plt.show()