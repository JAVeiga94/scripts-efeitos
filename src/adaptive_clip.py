import numpy as np

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    clip=0.3
    mx=np.std(indata)*clip
    outdata[:] = indata*(abs(indata)<mx)+mx*np.sign(indata)*(abs(indata)>=mx)
