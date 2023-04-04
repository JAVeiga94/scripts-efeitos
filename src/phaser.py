import global_settings, effect_chain
#import numba
import numpy as np

from scipy.signal import butter, lfilter, freqz

class Phaser(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="phaser"
        self.parameters=dict(N=10, f0=100., mix=0.5, fLFO=2., depth=0.5, f1=5000.)
        self.t=0
        self.zi=[[0]]*self.parameters['N']
        self.freqs=np.geomspace(self.parameters['f0'], self.parameters['f1'],self.parameters["N"])
    def set_parameter(self, name, val):
        self.parameters[name]=type(self.parameters[name])(val)
        if name == "N":
            self.zi=[[0]]*self.parameters["N"]
        self.freqs=np.geomspace(self.parameters['f0'], self.parameters['f1'],self.parameters["N"])
    def apply_effect(self, indata, outdata):
        dt=1/global_settings.samplerate
        outdata[:]=indata
        N=self.parameters["N"]
        mix=self.parameters['mix']
        
        for j in range(N):
            omega = self.freqs[j]*2*np.pi*\
                (1+self.parameters['depth']*np.sin(2*np.pi*self.t*self.parameters['fLFO']))
            if j %2:
                omega*=-1
            a=(1,-1+omega*dt)
            b=(1,-1-omega*dt)
            outdata[:,0], self.zi[j] = lfilter(b,a, outdata[:,0], zi=self.zi[j])
        outdata[:] = indata*(1-mix)+outdata*mix
        
        self.t+=len(outdata)*dt


