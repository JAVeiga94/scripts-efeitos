# Creates a drone note that follows and accompanies the player
import effect_chain, numpy as np, global_settings
from math import sin, log


intervals_from_C={"Cb":-1,"C":0,"C#":1,
           "Db":1, "D":2, "D#":3,
           "Eb":3, "E":4, "E#":5,
           "Fb":4, "F":5, "F#":6,
	   "Gb":6, "G":7, "G#":8,
           "Ab":8, "A":9, "A#":10,
           "Bb":10, "B":11, "B#":12}
def get_freq(s):
    return 220*2**((intervals_from_C[s]-9)/12)

def get_name(f):
    n=12*log(f/220)/log(2)+9
    for name in intervals_from_C:
        if int((n+48+1/2)%12)==intervals_from_C[name]:
            return name

class Drone(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="drone"
        
        self.samplerate=global_settings.samplerate
        self.parameters=dict(freq=110.0, attack=0.1, decay=0.5, mix=0.3, lp_omega=1000,
                             vib_depth=0.002, vib_omega=2.0, note="A")
        self.t0 = 0
        self.y=0
        self.lp_saw=0
    #override
    def set_parameter(self, name, val):
        if name not in ("note", "freq"):
            self.parameters[name]=type(self.parameters[name])(val)
        elif name=="freq":
            self.parameters['freq']=float(val)
            self.parameters['note']=get_name(float(val))
        elif name=="note":
            self.parameters['freq']=get_freq(val)
            self.parameters['note']=val
        
    def apply_effect(self, indata, outdata):
        frames=len(indata)
                
        samplerate=self.samplerate
        
        freq=self.parameters['freq']
        period=1/freq
        mix = self.parameters['mix']
        decay=self.parameters['decay']
        attack=self.parameters['attack']
        lp_omega_dt=self.parameters['lp_omega']/samplerate
        vib_depth = self.parameters['vib_depth']
        vib_omega = self.parameters['vib_omega']
        y=self.y
        lp_saw=self.lp_saw
        t=self.t0
        
        for i in range(len(outdata)):
            x=indata[i,0]
            y+=(x*x-y)/(samplerate*(decay if y>x*x else attack))
            a=y**.5
            t+=1/samplerate
            shift=vib_depth*sin(t*vib_omega)
            saw=2*((t+shift)%period)/period-1
            lp_saw+=lp_omega_dt*(saw-lp_saw)
            outdata[i,0] = indata[i,0]*(1-mix)+a*mix*lp_saw
        self.t0+=frames/samplerate
        self.y=y
        self.lp_saw=lp_saw


