import platform as pt
import subprocess as sp
import importlib.metadata as meta
#import Gui

class App:
    def __init__(self):

        Ls = [dist.metadata['Name'] for dist in meta.distributions()]

        self.Plt = pt.system()
        if self.Plt == 'Windows':

            with open('Requirements.txt', 'r') as Rn:
                for l in Rn.read().split('\n')[: -1]:
                    if l in Ls:
                        continue
                    else:
                        sp.run('pip install -r Requirements.txt')
                        break
            
                   
                




App()

