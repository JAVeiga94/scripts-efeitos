import numpy as np, effect_chain, global_settings

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
        self.parameters=dict(thresh=0.1, ingain=3)
    def apply_effect(self, indata, outdata):
        thresh = self.parameters['thresh']
        #rms=np.std(indata)

        #a*=1/max(rms,.00001)**2

        #x-a x^3                                                                                                                            
        #1-3 a x^2


        a=1/(3*thresh**2)
        x=thresh  #np.sqrt(1/(3*a))
        c = x-a*x**3
        indata[:]=self.parameters['ingain']*indata

        
        outdata[:] = (indata-a*indata**3)*(indata**2<1/(3*a))+(indata**2>=1/(3*a))*c*np.sign(indata)


#use the tanh function to create soft clipping
class TanH(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="tanh"
        self.parameters=dict(thresh=0.1, ingain=3)
    def apply_effect(self, indata, outdata):
        thresh = self.parameters['thresh']
        gain = self.parameters['ingain']
        outdata[:] = thresh*np.tanh((indata*gain)/thresh)

        
#Similar to the TanH, but introduce asymmetry in the thresholds to mimic a tube amp
class Asym(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="asym"
        self.parameters=dict(thresh1=0.1, thresh2=0.3, ingain=3)
    def apply_effect(self, indata, outdata):
        thresh1 = self.parameters['thresh1']
        thresh2 = self.parameters['thresh2']
        thresh = np.sign(indata)*(thresh1/2-thresh2/2)+(thresh1+thresh2)/2
        gain = self.parameters['ingain']
        outdata[:] = thresh*np.tanh((indata*gain)/thresh)

#binary fuzz mixed with clean signal
class Fuzz(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="fuzz"
        self.parameters=dict(volume=0.001, tau=0.05)
        self.y=0
    def apply_effect(self, indata, outdata):
        volume = self.parameters['volume']
        #outdata[:] = (2*(indata>0)-1)
        y=self.y
        tau = self.parameters['tau']
        samplerate=global_settings.samplerate
        samplerate_tau=samplerate*tau

        for i in range(len(indata)):
            x=indata[i,0]
            
            y+=(x**2-y)/samplerate_tau
            outdata[i,0] = y**.5*(2*(x>0)-1)

        self.y=y

class DynaDrive(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="dyna"
        self.parameters=dict(thresh_a=1., thresh_b=1., tau=0.005, asym=0.)
        self.y=0
    def apply_effect(self, indata, outdata):
        a = self.parameters['thresh_a']
        b = self.parameters['thresh_b']
        tau = self.parameters['tau']
        samplerate=global_settings.samplerate
        samplerate_tau=samplerate*tau
        asym=self.parameters['asym']
        y=self.y
        for i in range(len(indata)):
            x=indata[i,0]
            y+=(x**2-y)/samplerate_tau
            thresh=min(a*y**0.5, b)*(1+asym*np.sign(x))
            
            outdata[i,0] = thresh*(np.tanh(x/thresh) if thresh else 0)
            
        self.y=y
        
class LowPass(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="low_pass"
        self.parameters=dict(omega=20000)
        self.y=0
        self.samplerate=global_settings.samplerate

    def apply_effect(self, indata, outdata):
        frames=len(indata)
        omega = self.parameters['omega']
        dt=1/self.samplerate
        omega_dt=omega*dt
        y=self.y
        for i in range(frames):
            y+=omega_dt*(indata[i,0]-y)
            outdata[i,0] = y
        self.y=y
class HighPass(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="high_pass"
        self.parameters=dict(omega=50)
        self.y=0
        self.samplerate=global_settings.samplerate
        self.xprev=None

    def apply_effect(self, indata, outdata):
        frames=len(indata)
        omega = self.parameters['omega']
        dt=1/self.samplerate
        omega_dt=omega*dt
        y=self.y
        xprev=self.xprev
        if xprev==None:
            xprev=indata[0,0]
        for i in range(frames):
            y+=indata[i,0]-xprev-omega_dt*y
            outdata[i,0] = y
            xprev=indata[i,0]
        self.y=y
        self.xprev=xprev
