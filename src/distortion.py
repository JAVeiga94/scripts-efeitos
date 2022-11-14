import numpy as np

class AdaptiveClip:
    def __init__(self):
        self.name="adaptive_clip"
        self.parameters=dict(clip=0.3)
        self.parameter_types=dict(clip=float)
    def apply_effect(self, indata, outdata):
        clip = self.parameters['clip']
        rms = np.std(indata)
        mx=rms*clip
        outdata[:] = indata*(abs(indata)<mx)+mx*np.sign(indata)*(abs(indata)>=mx)

class AdaptiveCubic:
    def __init__(self):
        self.name="adaptive_cubic"
        self.parameters=dict(a=0.5)
        self.parameter_types=dict(a=float)
    def apply_effect(self, indata, outdata):
        a = self.parameters['a']
        rms=np.std(indata)

        a*=1/rms**2


        #x-a x^3
        #1-3 a x^2
        x=np.sqrt(1/(3*a))
        c = x-a*x**3
        
        outdata[:] = (indata-a*indata**3)*(indata**2<1/(3*a))+(indata**2>=1/(3*a))*c*np.sign(indata)
