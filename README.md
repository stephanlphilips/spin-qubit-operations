# spin-qubit-operations

This is library that generates commonly used pulses/shapes for spin qubit experiments.

The idea is to make templated functions that should make it easy to pick modules that fit your experiments and customize where needed.

All the templates a few build in functions that make life easy,
* add information to the segment about what has been added to the pulse (not implemented in segment, so just printing)
* contain a debug variable, this can be used to sample with the digitizer the effect of this pulse

To keep things organised, some syntax rules:
* If you want to make template that defines a time it should start with 't_'
* In case you want to define multiple inputs at one (e.g. coordinates of two plunger, this should be done with a tuple)
* The last argrument is always debug. This is automatically incorporated, so does not need to be defined by the user.


General note:
* how to make debug functionality univeral

## Install
Just go in a shell to the downloaded folder and excecute the setup file.
```python 
python setup.py develop
```

## dependecies
Curently (bound to change)
* pulse-lib
* V2_software
* si-prefix
