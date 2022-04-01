#!/usr/bin/python3

import hid
import pactl

class PCPanel:
    
    def __init__(self):
        self.pcpanel = hid.device()
        self.pcpanel.open(0x0483,0xa3c5)
        self.pcpanel.set_nonblocking(1)
        self.K1 = ''
        self.K2 = ''
        self.K3 = ''
        self.K4 = ''
        self.K5 = ''
        self.S1 = 'WEBRTC VoiceEngine'
        self.S2 = 'Firefox'
        self.S3 = ''
        self.S4 = ''
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
            for sink in pactl.dict_apps().get(dial):
                pactl.set_sink_input_vol(sink, int(val/255*100))



if __name__ == "__main__":
    p = PCPanel()
    while True:
        p.loop()
