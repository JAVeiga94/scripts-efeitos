import numpy as np, effect_chain

class AdaptiveClip(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="adaptive_clip"
        self.parameters=dict(clip=0.3)
    def apply_effect(self, indata, outdata):
        clip = self.parameters['clip']
        rms = np.std(indata)
        mx=rms*clip
        outdata[:] = indata*(abs(indata)<mx)+mx*np.sign(indata)*(abs(indata)>=mx)

class AdaptiveCubic(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="adaptive_cubic"
        self.parameters=dict(a=0.5)
    def apply_effect(self, indata, outdata):
        a = self.parameters['a']
        rms=np.std(indata)

        a*=1/max(rms,.00001)**2

        #x-a x^3
        #1-3 a x^2
        x=np.sqrt(1/(3*a))
        c = x-a*x**3
        
        outdata[:] = (indata-a*indata**3)*(indata**2<1/(3*a))+(indata**2>=1/(3*a))*c*np.sign(indata)

class SimpleCubic(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="cubic"
        self.parameters=dict(thresh=0.01)
    def apply_effect(self, indata, outdata):
        thresh = self.parameters['thresh']
        #rms=np.std(indata)

        #a*=1/max(rms,.00001)**2

        #x-a x^3                                                                                                                            
        #1-3 a x^2


        a=1/(3*thresh**2)
        x=thresh  #np.sqrt(1/(3*a))
        c = x-a*x**3


        
        outdata[:] = (indata-a*indata**3)*(indata**2<1/(3*a))+(indata**2>=1/(3*a))*c*np.sign(indata)
