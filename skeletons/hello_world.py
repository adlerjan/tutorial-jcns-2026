import matplotlib.pyplot as plt

from hermespy.simulation import SimulatedDevice
from hermespy.modem import TransmittingModem, RootRaisedCosineWaveform


# Simulation parameters
device_params = {
    'oversampling_factor': 4,
    'carrier_frequency': 6e9,
    'bandwidth': 960e6,
}

# Add a single new device
device = SimulatedDevice(**device_params)

# Configure transmitting modem generating a root-raised cosine waveform
waveform = RootRaisedCosineWaveform()
dsp = TransmittingModem(waveform=waveform)
device.add_dsp(dsp)

# Generate a single transmission base-band signal
transmission = device.transmit()
transmission.mixed_signal.plot(title='Base Station Tx')

# Display plots
plt.show()
