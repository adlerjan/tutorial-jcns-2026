import matplotlib.pyplot as plt

from hermespy.simulation import SimulatedDevice
from hermespy.modem import TransmittingModem, RootRaisedCosineWaveform

# Simulation parameters
cf = 26e9
bw = 1e9

# Add a new device
base_station = SimulatedDevice(carrier_frequency=cf, bandwidth=bw)

# Add DSP
waveform = RootRaisedCosineWaveform()
dsp = TransmittingModem(waveform=waveform)
base_station.add_dsp(dsp)

# Generate & visualize a single transmit frame
dsp.seed = 42
transmission = base_station.transmit()
transmission.mixed_signal.plot(title='BS Tx')

# Modify some parameters and re-run
dsp.seed = 42
waveform.roll_off = 1.0
base_station.oversampling_factor = 4
modified_transmission = base_station.transmit()
modified_transmission.mixed_signal.plot(title='BS Tx (Modified)')

plt.show()