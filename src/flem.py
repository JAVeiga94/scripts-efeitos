# Creates a flange effect with tremelo on the delayed signal
import effect_chain, numpy as np, global_settings
class Flem(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="flem"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=0.1
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(flange_period=0.5, delay=0.010, flange_depth=0.003, mix=0.4, trem_period=0.0397,
           trem_depth=0.7)
        self.t0 = 0
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        #move data back
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata
        
        samplerate=self.samplerate
        
        
        flange_omega=2*np.pi/self.parameters['flange_period']
        flange_depth=self.parameters['flange_depth']
        trem_omega=2*np.pi/self.parameters['trem_period']
        trem_depth=self.parameters['trem_depth']
        mix = self.parameters['mix']
        delay=self.parameters['delay']
        for i in range(len(outdata)):
            dt=np.sin(flange_omega*(self.t0+i/samplerate))*flange_depth+delay
            outdata[i,0] = indata[i,0]*(1-mix)+mix*(1+trem_depth*np.sin(trem_omega*(self.t0+i/samplerate)))*self.hist_buffer[-frames+i-int(dt*samplerate),0]
        self.t0+=frames/samplerate

    def format(self, channels=1, samplerate=48000,buffer_duration=1):
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
