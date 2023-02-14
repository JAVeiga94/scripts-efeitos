import effect_chain, numpy as np, global_settings
from math import sin
class Tremelo(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="tremelo"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(period=0.3, depth=0.2)
        self.t0=0
    def apply_effect(self, indata, outdata):
        frames=len(indata)

        dt=1/self.samplerate
        omega=2*np.pi/self.parameters['period']
        depth=self.parameters['depth']
        t=self.t0
        for i in range(len(outdata)):
            t+=dt
            s=sin(omega*t)*depth
            outdata[i,0] = indata[i,0]*(1+s*depth)
        self.t0+=frames*dt
