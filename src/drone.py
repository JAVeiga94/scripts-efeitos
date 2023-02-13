# Creates a drone note that follows and accompanies the player
import effect_chain, numpy as np, global_settings
class Drone(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="drone"
        
        self.samplerate=global_settings.samplerate
        self.parameters=dict(freq=110.0, attack=0.1, decay=0.5, mix=0.2)
        self.t0 = 0
        self.y=0
    def apply_effect(self, indata, outdata):
        frames=len(indata)
                
        samplerate=self.samplerate
        
        freq=self.parameters['freq']
        period=1/freq
        mix = self.parameters['mix']
        decay=self.parameters['decay']
        attack=self.parameters['attack']
        y=self.y
        #t0=self.t0
        for i in range(len(outdata)):
            x=indata[i,0]
            y+=(x*x-y)/(samplerate*(decay if y>x*x else attack))
            a=y**.5
            t=self.t0+i/samplerate
            saw=2*(t%period)/period-1
            outdata[i,0] = indata[i,0]*(1-mix)+a*mix*saw
        self.t0+=frames/samplerate
        self.y=y


