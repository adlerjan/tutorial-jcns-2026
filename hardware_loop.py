# -*- coding: utf-8 -*-

from hermespy.hardware_loop import HardwareLoop, UsrpDevice, UsrpSystem, ReceivedConstellationPlot, RadarRangePlot, PhysicalDeviceDummy, PhysicalScenarioDummy
from hermespy.jcas import MatchedFilterJcas
from hermespy.modem import ReceivingModem

from nr_waveform import NRSubframe

#loop = HardwareLoop[UsrpSystem, UsrpDevice](UsrpSystem())
loop = HardwareLoop[PhysicalScenarioDummy, PhysicalDeviceDummy](PhysicalScenarioDummy())
numerology_bandwidths = [12 * 15e3 * 2 ** n for n in range(0, 7)]
device_params = {
    'carrier_frequency': 6e9,
    'bandwidth': numerology_bandwidths[6],
    'oversampling_factor': 16,
}

# Add USRP devices
base_station = loop.new_device(**device_params)
vehicle = loop.new_device(**device_params)

# Configure 5G NR-like OFDM waveform
waveform = NRSubframe()
jcas_dsp = MatchedFilterJcas(200.0, waveform)
rx_modem = ReceivingModem(waveform=waveform)
base_station.add_dsp(jcas_dsp)
vehicle.add_dsp(rx_modem)

# Add visualization hooks
loop.add_plot(ReceivedConstellationPlot(rx_modem, 'Vehicle Rx'))
loop.add_plot(RadarRangePlot(jcas_dsp, 'BS JCAS Range'))

loop.num_drops = 100
loop.run()
