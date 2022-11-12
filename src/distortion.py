import numpy as np

class AdaptiveClip:
    def __init__(self):
        self.name="adaptive_clip"
        self.parameters=dict(clip=0.3)
    def apply_effect(self, indata, outdata):
        clip = self.parameters['clip']
        mx=np.std(indata)*clip
        outdata[:] = indata*(abs(indata)<mx)+mx*np.sign(indata)*(abs(indata)>=mx)
