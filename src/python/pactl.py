import subprocess as subprocess
from collections import defaultdict

def list_sink_inputs():
    """
    Returns a defaultdict of application names for keys and sink numbers for
    values.

    For example:
    >>> list_sink_inputs()
    defaultdict(<class 'list'>, {'WEBRTC VoiceEngine': [5], 'java': [2828], 'Firefox': [5168, 5175]})
    
    There can be multiple id's per application, such as for Firefox, where each
    tab has its own audio stream.
    """
    sinks = defaultdict(list)
    pactl = subprocess.Popen(['pactl', 'list', 'sink-inputs'], stdout=subprocess.PIPE)
    outval = pactl.communicate()[0].decode('utf-8')
    lines = [i.strip() for i in outval.splitlines() if 'Sink Input' in i or 'application.name' in i]
    names = lines[1::2]
    numbs = lines[::2]
    for i in range(len(names)):
        sinks[names[i][20:-1]].append(numbs[i][12:])
    return sinks


def set_sink_input_vol(sink, vol):
    subprocess.Popen(['pactl', 'set-sink-input-volume', sink, str(vol)+'%'], stdout=subprocess.PIPE)
    

def set_sink_default_mute(action):
    action = ('0' if action == False else
              '1' if action == True else
              'toggle'
              )
    subprocess.Popen(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', action])


def set_source_default_mute(action):
    action = ('0' if action == False else
              '1' if action == True else
              'toggle'
              )
    subprocess.Popen(['pactl', 'set-source-mute', '@DEFAULT_SOURCE@', action])
