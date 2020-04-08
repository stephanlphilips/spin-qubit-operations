# Short intro

Simple set of functions that allows one to easily generate a virtual pulse library. This can come in handy if you want to test the pulses on a system that is different from the system where you will actually run it.

Usage : 
```python 
from demo_pulse_lib.virtual_awg import get_demo_lib

pulse = get_demo_lib('quad')
```
