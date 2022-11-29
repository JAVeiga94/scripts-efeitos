import os,numpy as np, global_settings
from termcolor import colored
import getch

if os.name=='nt': os.system('color')

#for i in range(0, 1000000): print('|'+' '*(i%3) +colored("x","red")+' '*(3-i%3)+'|',end='\r')

note_names="A A#/Bb B C C#/Db D D#/Eb E F F#/Gb G G#/Ab".split()

class Tuner():
    def __init__(self):
        self.samplerate=global_settings.samplerate
        self.dt=1./self.samplerate
        octaves_below=-4
        octaves_above=1
        self.per_semitone=20
        
        self.f=2**(np.linspace(octaves_below,
                               octaves_above,
                               int(1+self.per_semitone*12*(octaves_above-octaves_below))))*440
        self.omega2=(2*np.pi*self.f)**2
        self.m=(-0.2+2*np.pi*1j)*self.f-0.2*self.f*(self.f>440)
        self.a=0j*np.zeros(len(self.f))
        self.mr=np.array([mi.real for mi in self.m])
        #print(self.f)
    def callback(self,indata, outdata, frames, time, status):
        #pass
        #print(len(indata[:,0]))
        for i in range(frames):
            y=indata[i,0]
            self.a+=(-y+self.a)*self.m*self.dt
        max_a=0
        f_at_max=0
        i_at_max=0
        for i in range(len(self.f)):
            if abs(self.a[i])>max_a:
                max_a=abs(self.a[i])
                f_at_max = self.f[i]
                i_at_max = i
        note_name=note_names[((i_at_max+self.per_semitone//2)//self.per_semitone)%12]
        if len(note_name)==1:
            note_name+="    "
        bar=(i_at_max+self.per_semitone//2)%self.per_semitone
        if bar==self.per_semitone//2:
            line="|"+" "*(self.per_semitone//2)+colored("|","white") + " "*(self.per_semitone//2) + "|     " + note_name + " %.1f    "%f_at_max
        elif bar<=self.per_semitone//2:
            line="|"+" "*bar+colored("|", "red") + " "*(self.per_semitone//2-bar-1)+"|"+\
                " "*(self.per_semitone//2)+ "|     " + note_name + " %.1f    "%f_at_max
        elif bar>=self.per_semitone//2:
            line="|"+" "*(self.per_semitone//2)+"|" + " "*(bar-self.per_semitone//2-1)+colored("|","red")+\
                " "*(self.per_semitone-bar)+ "|     " + note_name + " %.1f    "%f_at_max
        #line="|"+" "*bar+"|" + " "*(self.per_semitone-bar) + "|     " + note_name + "  "+str(f_at_max)
        
        
        print(line, end="\r")
        #outdata[:]=indata
