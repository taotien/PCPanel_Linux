import hid
import pactl
from collections import defaultdict

class PCPanel:
    def __init__(self):
        self.pcpanel = hid.device()
        self.pcpanel.open(0x0483,0xa3c5)
        self.pcpanel.set_nonblocking(1)
        self.K1 = input() 
        self.B1 = input() 
        self.K2 = input() 
        self.B2 = input() 
        self.K3 = input() 
        self.B3 = input() 
        self.K4 = input() 
        self.B4 = input() 
        self.K5 = input() 
        self.B5 = input() 
        self.S1 = input(['WEBRTC VoiceEngine']) 
        self.S2 = input(['Firefox']) 
        self.S3 = input() 
        self.S4 = input(active = True) 
        self.widgets = {
                1: {0: self.K1,
                    1: self.K2,
                    2: self.K3,
                    3: self.K4,
                    4: self.K5,
                    5: self.S1,
                    6: self.S2,
                    7: self.S3,
                    8: self.S4,
                    },
                2: {0: self.B1,
                    1: self.B2,
                    2: self.B3,
                    3: self.B4,
                    4: self.B5}
                }
    

    def __del__(self):
        self.pcpanel.close()
    

    def _data(self):
        data = []
        try: 
            data = self.pcpanel.read(3,250)
        except IOError as ex:
            print(ex)
        return data
    

    def loop(self):
        data = self._data()
        
        if not data:
            return
        
        try:
            self.widgets.get(data[0]).get(data[1]).adjust(data[2])
        except TypeError as ex:
            raise


class input:
    """

    TODO
    - auto release (unmute after 10 sec, etc)
    """
    def __init__(self, apps = [], devs = [], active = False):
        self.apps = apps
        self.devs = devs
        self.active = active
        self.min = 0
        self.max = 100
        self.log = False

    def set_range(self, minimum, maximum, logarithmic):
        self.min = minimum
        self.max = maximum
        self.log = logarithmic

    def adjust(self, val):
        if self.log:
            pass
        else:
            val = int(val/255*100)
            
        if self.active:
            pactl.set_active_sink_input_vol(val)
            return

        try:
            for app in self.apps:
                for iden in pactl.dict_apps().get(app):
                    pactl.set_sink_input_vol(iden, val)
        except KeyError:
            pass

        try:
            for dev in self.devs:
                pass
        except KeyError:
            raise
        
    def press(self):
        pass
    def release(self):
        pass
    def double_press(self):
        pass
    def hold(self):
        pass
