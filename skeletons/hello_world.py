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


# Configure transmitting modem generating a root-raised cosine waveform


# Generate a single transmission base-band signal


# Display plots
plt.show()
