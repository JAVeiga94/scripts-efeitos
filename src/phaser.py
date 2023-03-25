import global_settings, effect_chain
#import numba
import numpy as np
class Phaser(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="phaser"
        self.parameters=dict(mix=0.5,f0=100.,depth=.5, fLFO=1.)
        self.N=5
        self.y=[0]*self.N
        self.samplerate=global_settings.samplerate
        self.xprev=[0]*self.N
        self.t=0
    #@numba.jit()  #supposed to make things faster by using just-in-time compilation
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        mix = self.parameters['mix']
        dt=1/self.samplerate

        
        #cx=1
        #cxprev=-1-omega*dt

        #cyprev=1-omega*dt

        outdata[:]=indata
        for j in range(self.N):
            omega = self.parameters['f0']*\
                 (1+self.parameters['depth']*np.sin(2*np.pi*self.t*self.parameters['fLFO']))*2*np.pi*(j+1)
        
            y=self.y[j]
            xprev=self.xprev[j]
            a=(-1-omega*dt)
            b=(1-omega*dt)
            for i in range(outdata):
                x=outdata[i,0]
                y=x+a*xprev+b*y
                outdata[i,0] = y
                xprev=x
            self.y[j]=y
            self.xprev[j]=xprev
            
            
        outdata[:]=outdata*mix+indata*(1-mix)
        self.t+=dt*frames
