# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from hermespy.hardware_loop import HardwareLoop, UsrpDevice, UsrpSystem, ReceivedConstellationPlot, RadarRangePlot, PhysicalDeviceDummy, PhysicalScenarioDummy, DeviceReceptionPlot
from hermespy.jcas import MatchedFilterJcas
from hermespy.modem import ReceivingModem

from nr_waveform import NRSubframe

# Add USRP device
loop = HardwareLoop[UsrpSystem, UsrpDevice](UsrpSystem())
base_station = loop.new_device(ip='10.11.58.81', carrier_frequency=5e8)

# Configure 5G NR-like OFDM waveform
waveform = NRSubframe(synchronize=True)
jcas_dsp = MatchedFilterJcas(200.0, waveform)
rx_modem = ReceivingModem(waveform=waveform)
base_station.transmitters.add(jcas_dsp)
base_station.receivers.add(rx_modem)
#vehicle.add_dsp(rx_modem)

# Add visualization hooks
# loop.add_plot(ReceivedConstellationPlot(rx_modem, 'Vehicle Rx'))
# loop.add_plot(DeviceReceptionPlot(base_station, 'BS Reception'))
# loop.add_plot(RadarRangePlot(jcas_dsp, 'BS JCAS Range'))

loop.num_drops = 100
loop.run()
