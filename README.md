# spin-qubit-operations

This is library that generates commonly used pulses/shapes for spin qubit experiments.

The idea is to make templated functions that should make it easy to pick modules that fit your experiments and customize where needed.

All the templates a few build in functions that make life easy,
* add information to the segment about what has been added to the pulse (not implemented in segment, so just printing)
* contain a debug variable, this can be used to sample with the digitizer the effect of this pulse
