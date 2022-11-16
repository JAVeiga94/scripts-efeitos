import numpy as np, effect_chain

#base class for all delay/reverb type effects
class DelayBase(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="delay"
        self.hist_buffer=None
        channels=1; samplerate=48000;buffer_duration=1
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(dt=0.10, amp=0.3)
        self.parameter_types=dict(dt=float, amp=float)
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        #move data back
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata
        n=int(self.parameters['dt']*self.samplerate)
        outdata[:] = indata+self.parameters['amp']*self.hist_buffer[-frames-n:-n]

    def format(self, channels=1, samplerate=48000,buffer_duration=1):
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))

class Flange(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="flange"
        self.hist_buffer=None
        channels=1; samplerate=48000; buffer_duration=0.1
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(period=0.1, delay=0.010, depth=0.005, mix=0.5)
        self.parameter_types={a : type(self.parameters[a]) for a in self.parameters.keys()}
        self.t0 = 0
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        #move data back                                                                                                          
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata
        
        samplerate=self.samplerate
        
        
        omega=2*np.pi/self.parameters['period']
        depth=self.parameters['depth']
        mix = self.parameters['mix']
        delay=self.parameters['delay']
        for i in range(len(outdata)):
            dt=np.sin(omega*(self.t0+i/samplerate))*depth+delay
            outdata[i,0] = indata[i,0]*(1-mix)+mix*self.hist_buffer[-frames+i-int(dt*samplerate),0] 
        self.t0+=frames/samplerate

    def format(self, channels=1, samplerate=48000,buffer_duration=1):
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))        
