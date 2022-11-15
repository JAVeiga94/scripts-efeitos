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
        self.channels=1
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

        
