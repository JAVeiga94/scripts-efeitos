class Effect:
    def __init__(self):
        name=""
        parameters={}
        parameter_types={}

class EffectChain:
    def __init__(self):
        self.effects=[]
    def apply_effects(self, indata, outdata):

        outdata[:]=indata
        for effect in self.effects:
            effect.apply_effect(outdata,outdata)
            
    def __call__(self,indata, outdata, frames, time, status):
        if status:
            print(status)
        self.apply_effects(indata,outdata)

    def parse_line(self, line):
        if(len(line)==0):
            return
        if line[0] == '#':
            return
        line = line.split()
        if line[0] == "edit":
            if len(line) != 4:
                print("syntax:  edit effect param value")
                return
            for effect in self.effects:
                if effect.name == line[1]:
                    effect.parameters[line[2]] =  effect.parameter_types[line[2]](line[3])
        elif line[0] == "list":
            for i in range(len(self.effects)):
                print(i, self.effects[i].name)
                for key in self.effects[i].parameters.keys():
                    print("  ",key, self.effects[i].parameters[key])
        elif line[0] == "remove":
            if len(line) != 2:
                print("syntax:  remove effect#")
                return
            tmp=self.effects.copy()
            for effect in self.effects:
                if effect.name == line[1]:
                    tmp.remove(effect)
            self.effects = tmp
        elif line[0] == "insert":
            if len(line) != 3:
                print("syntax:  insert module.class position")
                return
            tmp=self.effects.copy()
            split2 = line[1].split(".")
            modulename=split2[0]
            classname=split2[1]
            module = __import__(modulename)
            effect = getattr(module, classname)()
            tmp.insert(int(line[2]),effect)
            self.effects = tmp
        elif line[0] == 'append':
            if len(line) != 2:
                print("syntax:  append module.class")
                return
            tmp=self.effects.copy()
            split2 = line[1].split(".")
            modulename=split2[0]
            classname=split2[1]
            module = __import__(modulename)
            effect = getattr(module, classname)()
            tmp.append(effect)
            self.effects = tmp
        elif line[0] == 'load':
            if len(line) != 2:
                print("syntax:  load filename")
                return
            self.load(line[1])
        elif line[0] == 'save':
            if len(line) != 2:
                print("syntax: save filename")
                return
            with open(line[1],"w") as f:
                for effect in self.effects:
                    f.write("append "+ str(type(effect)).replace("<class '", "").replace("'>","")+"\n")
                    for key in effect.parameters.keys():
                        f.write("edit " + effect.name + " " + key + " " + str(effect.parameters[key])+"\n")
        elif line == ["exit"]:
            exit()
        
    def cli(self):
        while True:
            line = input()
            self.parse_line(line)
            
    def load(self, filename):
        with open(filename, "r") as f:
            for line in f.readlines():
                self.parse_line(line)
                
