import readline, os
import tuner, getch

class Effect:
    def __init__(self):
        self.name="effect"
        self.parameters={}
        self.on=True

class EffectChain:
    def __init__(self):
        self.effects=[]
        self.tuner_active=False
        self.tuner=tuner.Tuner()
        self.mute=False
        self.input_gain=1
        self.output_gain=1
    def apply_effects(self, indata, outdata):

        effects=self.effects
        allOff=True


        if self.input_gain !=1:
            indata[:]=self.input_gain*indata
        
        for effect in effects:
            if effect.on==True:
                allOff=False
                break
            
        if allOff:
            outdata[:]=indata
            return
        first=True
        for i in range(len(effects)):
            effect = effects[i]
            if effect.on == False:
                continue
            if first:
                effect.apply_effect(indata,outdata)
                first=False
            else:
                effect.apply_effect(outdata,outdata)
        if self.output_gain !=1:
            outdata[:]=self.output_gain*outdata
        #outdata[:]=indata
        #for effect in self.effects:
        #    effect.apply_effect(outdata,outdata)
            
    def __call__(self,indata, outdata, frames, time, status):
        if status:
            print(status)
        if self.tuner_active:
            self.tuner.callback(indata,outdata,frames, time,status)
        self.apply_effects(indata,outdata)
        if self.mute:
            outdata *=0
    def parse_line(self, line):
        if(len(line)==0):
            return
        if line[0] == '#':
            return
        if line[0] == '!':
            os.system(line[1:])
            return
        line = line.split()
        if line[0] == "edit":
            if len(line) != 4:
                print("syntax:  edit effect param value")
                return
            found = False
            for effect in self.effects:
                if effect.name == line[1]:
                    if not line[2] in effect.parameters.keys():
                        print(f"effect '{line[1]}' does not have a parameter '{line[2]}'")
                        return
                    # parse it to the class that the previous value of the parameter was.
                    # ie, autodetect what type should be used.  
                    effect.parameters[line[2]] =  type(effect.parameters[line[2]])(line[3])
                    found=True
                    return
            if not found:
                print("no effect named '" + line[1] + "' found in chain")
                return
        elif line[0] == "list":
            for i in range(len(self.effects)):
                print(i, self.effects[i].name, "on" if self.effects[i].on else "off")
                for key in self.effects[i].parameters.keys():
                    print("  ",key, self.effects[i].parameters[key])
        elif line[0] == "mute":
            self.mute=True
        elif line[0] == "unmute":
            self.mute=False
        elif line[0] == "remove":
            if len(line) != 2:
                print("syntax:  remove effect")
                return
            tmp=self.effects.copy()
            found = False
            for effect in self.effects:
                if effect.name == line[1]:
                    tmp.remove(effect)
                    found=True
            if not found:
                print("no effect named '"+line[1]+"' in chain")
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
        elif line[0] == 'toggle':
            if len(line) != 2:
                print("syntax:  toggle effectname")
                return
            found = False
            for effect in self.effects:
                if line[1] == effect.name:
                    effect.on ^= True
                    found=True
            if not found:
                print("no effect named '"+line[1]+"'")
        elif line[0] == 'off':
            if len(line) != 2:
                print("syntax:  off effectname")
                return
            if line[1]=='all':
                for effect in self.effects:
                    effect.on = False
                return
            found = False
            for effect in self.effects:
                if line[1] == effect.name:
                    effect.on = False
                    found=True
            if not found:
                print("no effect named '"+line[1]+"'")
        elif line[0] ==	'on':
            if len(line) != 2:
                print("syntax:  on effectname")
                return
            if line[1] == 'all':
                for effect in self.effects:
                    effect.on = True
                return
            found = False
            for effect in self.effects:
                if line[1] == effect.name:
                    effect.on =	True
                    found=True
            if not found:
                print("no effect named '"+line[1]+"'")
        elif line[0] == 'save':
            if len(line) != 2:
                print("syntax: save filename")
                return
            with open(line[1],"w") as f:
                for effect in self.effects:
                    f.write("append "+ str(type(effect)).replace("<class '", "").replace("'>","")+"\n")
                    if not effect.on:
                        f.write(f"off {effect.name}\n")
                    for key in effect.parameters.keys():
                        f.write("edit " + effect.name + " " + key + " " + str(effect.parameters[key])+"\n")
        elif line[0] == "exit":
            exit()
        elif line[0] == "tuner":
            self.tuner_active=True
            print("Press the enter key to exit the tuner")
            input()
            self.tuner_active=False
            print("\r                       ")
        elif line[0] == "gain":
            if len(line) !=3:
                print("syntax:  gain [input or output] value")
            if line[1] == "input":
                self.input_gain=float(line[2])
            if line[1] == "output":
                self.output_gain=float(line[2])
        elif line[0] == "help":
            print("list of commands: \nappend \ninsert \nremove \nlist \nedit"+
            "\non \noff \ntoggle \nload \nsave \nhelp \nexit \nmute \nunmute \ntuner")
        else :
            print(f"command not found: '{line[0]}'")

    #autocomplete_list=["append", "insert", "on", "toggle", "edit","off", "all", "help", "exit", "remove", "list", "load", "save"]

    # for autocompleting in the CLI

    def traverse(self,tokens,tree):
        if tree is None:
            return []
        elif len(tokens) == 0:
            return []
        if len(tokens) == 1:
            return [x+' ' for x in tree.keys() if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
                return self.traverse(tokens[1:],tree[tokens[0]])
            else:
                return []
        return []
    
    def complete(self, text,state):
        #create a tree of possible autocomplete
        effect_catalog=None
        effects_tree = {effect.name:None for effect in self.effects}
        tree = {"load": None,
                "save": None,
                "help": None,
                "exit": None,
                "list": None,
                "tuner":None,
                "mute": None,
                "unmute":None,
                "append": effect_catalog,
                "insert": effect_catalog,
                "toggle": effects_tree,
                "on" : effects_tree,
                "off" : effects_tree,
                "remove" : effects_tree,
                "edit" : {effect.name:{par: None for par in effect.parameters.keys()} for effect in self.effects},
                "gain" : {"input" : None, "output" : None}
                } 
        #try:
        tokens = readline.get_line_buffer().split()
        if not tokens or readline.get_line_buffer()[-1] == ' ':
            tokens.append("")
        results = self.traverse(tokens,tree) + [None]
        return results[state]
        #except Exception as e:
        #    print(e)
        
    def cli(self):
        import readline
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)
        while True:
            line = input()
            try:
                self.parse_line(line)
            except Exception as err:
                print(f"Unexpected {err}, {type(err)}")
            
    def load(self, filename):
        with open(filename, "r") as f:
            for line in f.readlines():
                self.parse_line(line)
                
