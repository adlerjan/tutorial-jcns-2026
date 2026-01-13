# -*- coding: utf-8 -*-

from hermespy.hardware_loop import HardwareLoop, UsrpDevice, UsrpSystem, ReceivedConstellationPlot, RadarRangePlot, DeviceReceptionPlot
from hermespy.jcas import MatchedFilterJcas
from hermespy.modem import ReceivingModem

from nr_waveform import NRSubframe


# Hardware loop parameters
device_params = {
    'ip': '192.168.199.48',
    'carrier_frequency': 1e9,
    'oversampling_factor': 8,
    'sampling_rate': 1e9,
    'selected_transmit_ports': [0],
    'selected_receive_ports': [0,1],
    'num_prepended_zeros': 3000,
    'num_appended_zeros': 3000,
    'max_receive_delay': 5e-7,
}

# Add USRP device
loop = HardwareLoop[UsrpSystem, UsrpDevice](UsrpSystem())
usrp = loop.new_device(**device_params)

# Configure a simplex link (transmitting and receiving modem) with
# a 5G NR-like subframe waveform
waveform = NRSubframe(synchronize=True)
waveform.modulation_order = 4
jcas_dsp = MatchedFilterJcas(
    2.0,
    waveform,
    selected_transmit_ports=[0],
    selected_receive_ports=[0],
)
rx_modem = ReceivingModem(
    waveform=waveform,
    selected_receive_ports=[1],
)
usrp.transmitters.add(jcas_dsp)
usrp.receivers.add(jcas_dsp)
usrp.receivers.add(rx_modem)

# Add visualization hooks
loop.add_plot(DeviceReceptionPlot(usrp, 'USRP Reception'))
loop.add_plot(ReceivedConstellationPlot(rx_modem, 'Vehicle Rx'))
loop.add_plot(RadarRangePlot(jcas_dsp, 'USRP JCAS Range'))

# Run loop
loop.num_drops = 100
loop.run()
