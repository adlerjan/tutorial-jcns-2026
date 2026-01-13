# -*- coding: utf-8 -*-

from hermespy.modem import (
    ElementType,
    OFDMWaveform,
    SymbolSection, 
    PrefixType,
    GridElement,
    GridResource,
    OrthogonalLeastSquaresChannelEstimation,
    OrthogonalZeroForcingChannelEqualization,
    SchmidlCoxPilotSection,
    SchmidlCoxSynchronization
)


class NRSubframe(OFDMWaveform):
    """Mock of the a 5G New Radio (NR) numerology."""

    __DEFAULT_NUM_SUBCARRIERS = 12
    __DEFAULT_CYCLIC_PREFIX_RATIO = 4.76e-2  # Normal CP
    __DEFAULT_NUM_FRAME_SYMBOLS = 14  # 10 ms frame with 1 ms subframes and 14 symbols per subframe

    def __init__(self, synchronize: bool = False) -> None:

        # Build a frame structure
        grid_resources = [GridResource(
            4,
            PrefixType.CYCLIC,
            self.__DEFAULT_CYCLIC_PREFIX_RATIO,
            [
                GridElement(ElementType.DATA, 2),
                GridElement(ElementType.REFERENCE, 1),
            ],
        )]
        grid_structure = [SymbolSection(self.__DEFAULT_NUM_FRAME_SYMBOLS, [0])]

        OFDMWaveform.__init__(
            self,
            grid_resources,
            grid_structure,
            num_subcarriers=self.__DEFAULT_NUM_SUBCARRIERS,
            dc_suppression=False,
        )

        # Add channel estimation & equalization
        self.channel_estimation = OrthogonalLeastSquaresChannelEstimation()
        self.channel_equalization = OrthogonalZeroForcingChannelEqualization()
        
        # Add synchronization if requested
        if synchronize:
            self.synchronization = SchmidlCoxSynchronization()
            self.pilot_section = SchmidlCoxPilotSection()
