# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 14:25:30 2021

@author: sdesnoo
"""
import copy
from pulse_lib.segments.utility.template_base import pulse_template

class ReadoutTemplate(pulse_template):
    def __init__(self, measurement_func, measurement, **func_kwargs):
        self.measurement = measurement
        self.measurement_func = measurement_func
        self.func_kwargs = func_kwargs

    def replace(self, **kwargs):
        cpy = copy.copy(self)
        meas = cpy.measurement
        kwargs_func = cpy.func_kwargs.copy()
        for key, value in kwargs.items():
            if hasattr(meas, key):
                meas = meas.replace(**{key:value})
            else:
                kwargs_func[key] = value
        cpy.measurement = meas
        cpy.func_kwargs = kwargs_func
        return cpy

    def build(self, segment, reset=False, **kwargs):

        kwargs_func = self.func_kwargs.copy()
        meas = self.measurement
        for key, value in kwargs.items():
            if hasattr(meas, key):
                meas = meas.replace(**{key:value})
            else:
                kwargs_func[key] = value
        self.measurement_func(segment, meas=self.measurement, **kwargs_func)


class FunctionTemplate(pulse_template):
    def __init__(self, func, **func_kwargs):
        self.func = func
        self.func_kwargs = func_kwargs

    def replace(self, **kwargs):
        cpy = copy.copy(self)
        meas = cpy.measurement
        kwargs_func = cpy.func_kwargs.copy()
        for key, value in kwargs.items():
            if hasattr(meas, key):
                meas = meas.replace(**{key:value})
            else:
                kwargs_func[key] = value
        cpy.measurement = meas
        cpy.func_kwargs = kwargs_func
        return cpy

    def build(self, segment, reset=False, **kwargs):

        kwargs_func = self.func_kwargs.copy()
        self.func(segment, **kwargs_func)