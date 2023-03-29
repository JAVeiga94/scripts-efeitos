import global_settings, effect_chain
#import numba
import numpy as np

from scipy.signal import butter, lfilter, freqz

class LowPass(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="low_pass"
        self.parameters=dict(order=1,cutoff=8000.)
        self.set_parameter("order",1)
        
    def set_parameter(self, name, val):
        self.parameters[name]=type(self.parameters[name])(val)
        order=self.parameters['order']
        cutoff=self.parameters['cutoff']
        fs=global_settings.samplerate
        #determine coefficients for a butterworth low-pass filter
        self.b, self.a=butter(order,cutoff, fs=fs, btype='low', analog=False)
        #initial conditions
        self.zi=[0]*(max(len(self.a), len(self.b))-1)
    def apply_effect(self, indata, outdata):
        outdata[:,0], self.zi = lfilter(self.b,self.a, indata[:,0], zi=self.zi)

class HighPass(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="high_pass"
        self.parameters=dict(order=1,cutoff=100.)
        self.set_parameter("order",1)

    def set_parameter(self, name, val):
        self.parameters[name]=type(self.parameters[name])(val)
        order=self.parameters['order']
        cutoff=self.parameters['cutoff']
        fs=global_settings.samplerate
        #determine coefficients for a butterworth high-pass filter
        self.b, self.a=butter(order,cutoff, fs=fs, btype='high', analog=False)
        #initial conditions
        self.zi=[0]*(max(len(self.a), len(self.b)) - 1)
    def apply_effect(self, indata, outdata):
        outdata[:,0],self.zi=lfilter(self.b,self.a, indata[:,0], zi=self.zi)
