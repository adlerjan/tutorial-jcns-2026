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


# Link device and vehicle by a 3GPP TDL type D channel


# Configure a simplex link (transmitting and receiving modem) with
# a root-raised cosine waveform, perfect channel knowledge, and zero-forcing equalization


# Generate a single scenario drop (all devices transit and receive once)
# Visualize transmission, reception, and equalized symbol constellation


# Display plots
plt.show()
 