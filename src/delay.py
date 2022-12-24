import numpy as np, effect_chain, global_settings

#base class for all delay/reverb type effects
class BasicDelay(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="delay"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=2
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(dt=0.10, amp=0.3)
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        #move data back
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata
        n=int(self.parameters['dt']*self.samplerate)
        outdata[:] = indata+self.parameters['amp']*self.hist_buffer[-frames-n:-n]

    def format(self, channels=1, samplerate=48000,buffer_duration=1):
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))

# similar to BasicDelay, but mixing the delayed signal into the history buffer
# in order to get multiple echos
class Echo(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="echo"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=2
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(dt=0.3, mix=0.2)
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        mix = self.parameters['mix']
        dt = self.parameters['dt']
        samplerate=self.samplerate
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        n = int(dt*samplerate)
        self.hist_buffer[-frames:]=(1-mix)*indata+mix*self.hist_buffer[-frames-n:-n]
        outdata[:] = self.hist_buffer[-frames:]

    def format(self, channels=1, samplerate=48000,buffer_duration=1):
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))

#similar to echo but with multiple different delays happening at the same time
phi=(np.sqrt(5)+1)/2
class Reverb(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="reverb"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=2
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(dt=0.3, mix=0.2)
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        mix = self.parameters['mix']
        dt = self.parameters['dt']
        samplerate=self.samplerate
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        n = int(dt*samplerate)
        n2 = int(n*phi)
        n3 = int(n*phi*phi)
        self.hist_buffer[-frames:]=(1-mix)*indata+\
                           (mix*self.hist_buffer[-frames-n:-n]+\
                           mix*self.hist_buffer[-frames-n2:-n2]/phi+\
                            mix*self.hist_buffer[-frames-n3:-n3]/phi/phi)/3
        outdata[:] = self.hist_buffer[-frames:]

    def format(self, channels=1, samplerate=48000,buffer_duration=1):
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))


        
class Flange(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="flange"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=0.1
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(period=0.5, delay=0.010, depth=0.005, mix=0.5)
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

class EvenHarmonicSuppressor(effect_chain.Effect):
    def __init__(self):
        super().__init__()
        self.name="ehs"
        self.hist_buffer=None
        channels=global_settings.channels
        samplerate=global_settings.samplerate
        buffer_duration=0.1
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
        self.samplerate=samplerate
        self.channels=channels
        self.parameters=dict(mix=0.5,mix2=0.3, low=100, high=1100)
        self.parameter_types={a : type(self.parameters[a]) for a in self.parameters.keys()}
        self.t0 = 0
    def apply_effect(self, indata, outdata):
        frames=len(indata)
        #move data back                                                                                                           
        self.hist_buffer[:-frames]=self.hist_buffer[frames:]
        self.hist_buffer[-frames:]=indata

        samplerate=self.samplerate        

        mix = self.parameters['mix']
        low = self.parameters['low']
        high= self.parameters['high']
        
        F=440

        #determine the frequency to use:
        #delta_f = (high - low) / (args.columns - 1)
        #fftsize = math.ceil(samplerate / delta_f)
        #low_bin = math.floor(low / delta_f)

    
        #magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
        

        
        for i in range(len(outdata)):
            dt=1/(2*F)
            outdata[i,0] = indata[i,0]*(1-mix)-mix*self.hist_buffer[-frames+i-int(dt*samplerate),0]
        

    def format(self, channels=1, samplerate=48000,buffer_duration=1):
        self.hist_buffer=np.zeros((int(samplerate*buffer_duration), channels))
