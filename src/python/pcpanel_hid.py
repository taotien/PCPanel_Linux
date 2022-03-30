#!/usr/bin/python3

import hid
import subprocess as sp
import time


_pactl_sinks_dict_fresh = False
_pactl_sinks_dict_time = time.time() - 1
_pactl_sinks = {}
def pactl_sinks_dict():
    global _pactl_sinks_dict_fresh
    global _pactl_sinks_dict_time
    global _pactl_sinks
    

    if (_pactl_sinks_dict_time + 2) < time.time():
        _pactl_sinks_dict_time = time.time()
        _pactl_sinks_dict_fresh = False
        return _pactl_sinks
        
    sinks = _pactl_sinks
    if not _pactl_sinks_dict_fresh:
        pactl = sp.Popen(['pactl', 'list', 'sink-inputs'], stdout=sp.PIPE)
        outval = pactl.communicate()[0].decode('utf-8')
        lines = [i.strip() for i in outval.splitlines() if 'Sink Input' in i or 'application.name' in i]
        sinks = {'Firefox': [], 'Discord': []}
        for i in range(int(len(lines)/2)):
            sinks[lines[i*2+1].strip('application.name = "').strip('"')].append(int(lines[i*2].strip('Sink Input #')))
        _pactl_sinks_dict_fresh = True

    _pactl_sinks = sinks
    return sinks

def pactl_set(sink, vol):
    __ = sp.Popen(['pactl', 'set-sink-input-volume', str(sink), str(vol)+'%'], stdout=sp.PIPE)


class PCPanel:
    
    def __init__(self):
        self.pcpanel = hid.device()
        self.pcpanel.open(0x0483,0xa3c5)
        self.pcpanel.set_nonblocking(1)
        self.K1 = ''
        self.K2 = ''
        self.K3 = 'Mic'
        self.K4 = ''
        self.K5 = ''
        self.S1 = 'Discord'
        self.S2 = 'Firefox'
        self.S3 = ''
        self.S4 = 'Game'
    def __del__(self):
        self.pcpanel.close()
    def __data(self):
        data = []
        try: 
            data = self.pcpanel.read(3,250)
        except IOError as ex:
            print(ex)
        return data
    def loop(self):
        def switch_dials(arg):
            switch = {
                    0: self.K1, 
                    1: self.K2, 
                    2: self.K3, 
                    3: self.K4, 
                    4: self.K5, 
                    5: self.S1, 
                    6: self.S2, 
                    7: self.S3, 
                    8: self.S4, 
                    }
            return switch.get(arg)

        data = self.__data()
        
        if (data == []):
            return
        
        if (data[0] == 1):
            dial = switch_dials(data[1])
            val = data[2]
            if (dial == ''):
                dial == 'Other'
            for sink in pactl_sinks_dict().get(dial):
                pactl_set(sink, int(val/255*100))



if __name__ == "__main__":
    __ = pactl_sinks_dict()
    p = PCPanel()
    while(True):
        try:
            p.loop()
        except KeyboardInterrupt:
            del p

    pactl_sinks_dict()
  
