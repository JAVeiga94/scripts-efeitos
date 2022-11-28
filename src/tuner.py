import os,numpy as np
from termcolor import colored
import getch

if os.name=='nt': os.system('color')

#for i in range(0, 1000000): print('|'+' '*(i%3) +colored("x","red")+' '*(3-i%3)+'|',end='\r')


class Tuner():
    def __init__(self):
        self.framerate=48000
        self.dt=1./self.framerate
        self.f=2**(np.linspace(-5,0, 61))*440
        self.omega2=(2*np.pi*self.f)**2
        self.m=(-0.2+2*np.pi*1j)*self.f
        self.a=0j*np.zeros(len(self.f))+1
        self.mr=np.array([mi.real for mi in self.m])
    def callback(self,indata, outdata, frames, time, status):
        #pass
        #print(len(indata[:,0]))
        for i in range(frames):
            y=indata[i,0]
            self.a+=(-y+self.a)*self.m*self.dt
        max_a=0
        f_at_max=0
        for i in range(len(self.f)):
            if abs(self.a[i])>max_a:
                max_a=abs(self.a[i])
                f_at_max = self.f[i]
        #line="| "+colored("x","red") + "   |"
        #line = "   " + str(abs(self.a[-1]))
        line = "   " + str(f_at_max)
        print(line, end="\r")
        #outdata[:]=indata
