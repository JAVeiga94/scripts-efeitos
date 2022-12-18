import numpy as np, effect_chain, global_settings

#base class for all delay/reverb type effects
class Octave(effect_chain.Effect):
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
        self.parameters=dict(period=0.05, mix=0.5, r=1.0)
        self.frame=0
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        #move data back
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata

        N = int(self.parameters['period']*self.samplerate)
        mix = self.parameters['mix']
        j=self.frame
        r=self.parameters['r']
        for i in range(len(outdata)):
            j+=1
            if j>N:
                j=0
            x=j/N
            w1=mix*np.sin(x*np.pi)
            w2=mix*abs(np.cos(x*np.pi))


            #dn1 = -N+int(j*r)
            #dn2 = -N+int((j+N/2)*r)
            #dn2-=N*(dn2>0)
            if r>=0:
                dn1 = int((j-N)*r)
                dn2 = int((j-N/2)*r)
                dn2-=int(N*r)*(dn2>0)
            else:
                dn1 = int(j*r)
                dn2 = int((j-N/2)*r)
                dn2+= int(N*r)*(dn2>0)

            
            outdata[i,:] = self.hist_buffer[-frames+i,:]*(1-mix) +\
                       w1*self.hist_buffer[-frames+i+dn1,:]+\
                       w2*self.hist_buffer[-frames+i+dn2,:]
        self.frame=j

        self.frame=j



