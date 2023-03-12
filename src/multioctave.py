import numpy as np, effect_chain, global_settings
from math import sin, cos
#base class for all delay/reverb type effects
class OctaveUp(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="octave"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=2
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.fn = np.ogrid[0:48,0:0][0]
        
        self.parameters=dict(mix=0.5)
        self.frame=0
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        #move data back
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata

        mix = self.parameters['mix']
        j=self.frame
        
        dn1=-2048+j%2048
        dn2=-2048+(j+1024)%2048
        outdata[:]=(1-mix)*indata+mix*(np.sin((j+self.fn)*np.pi/2048)*self.hist_buffer[-2*frames+dn1:dn1:2]+\
                       np.cos((j+self.fn)*np.pi/2048)*self.hist_buffer[-frames*2+dn2:dn2:2])
        
        self.frame+=frames
        
class OctaveDown(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="octave"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=2
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.fn = np.ogrid[0:48,0:0][0]

        self.parameters=dict(mix=0.5)
        self.frame=0
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        #move data back                                                                                                                       
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata

        
        mix = self.parameters['mix']
        j=self.frame
        dn1=-2048-((j+2048)%2048)//2
        dn2=-2048-((j+1024)%2048)//2

        
        outdata[::]=(1-mix)*indata
        outdata[::2]+=mix*(np.sin((j+self.fn[::2])*np.pi/2048)*self.hist_buffer[-frames//2+dn1:dn1:]+\
                       np.cos((j+self.fn[::2])*np.pi/2048)*self.hist_buffer[-frames//2+dn2:dn2:])
        outdata[1::2]+=mix*(np.sin((j+self.fn[1::2])*np.pi/2048)*self.hist_buffer[-frames//2+dn1:dn1:]+\
                       np.cos((j+self.fn[1::2])*np.pi/2048)*self.hist_buffer[-frames//2+dn2:dn2:])

        self.frame+=frames
        
class OctaveUpDown(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="octave"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=2
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.fn = np.ogrid[0:48,0:0][0]

        self.parameters=dict(mix_up=0.2, mix_down=0.2)
        self.frame=0
    def apply_effect(self, indata, outdata):
        frames=len(indata)
                                                                                                                                             
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata

	
        mix_up = self.parameters['mix_up']
        mix_down = self.parameters['mix_down']
        j=self.frame
        dn1=-1024-((j+2048)%2048)//2
        dn2=-1024-((j+1024)%2048)//2


        outdata[::]=(1-mix_up-mix_down)*indata
        outdata[::2]+=mix_down*(np.sin((j+self.fn[::2])*np.pi/2048)*self.hist_buffer[-frames//2+dn1:dn1:]+\
                       np.cos((j+self.fn[::2])*np.pi/2048)*self.hist_buffer[-frames//2+dn2:dn2:])
        outdata[1::2]+=mix_down*(np.sin((j+self.fn[1::2])*np.pi/2048)*self.hist_buffer[-frames//2+dn1:dn1:]+\
                       np.cos((j+self.fn[1::2])*np.pi/2048)*self.hist_buffer[-frames//2+dn2:dn2:])

        dn1=-2048+j%2048
        dn2=-2048+(j+1024)%2048
        outdata[:]+=mix_up*(np.sin((j+self.fn)*np.pi/2048)*self.hist_buffer[-2*frames+dn1:dn1:2]+\
                       np.cos((j+self.fn)*np.pi/2048)*self.hist_buffer[-frames*2+dn2:dn2:2])
        self.frame+=frames


