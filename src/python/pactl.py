import subprocess
from collections import defaultdict

def list_sink_inputs(option='a'):
    """
    TODO
    - is limiting calls to this necessary
    """
    arg = 'media.name' if option=='m' else 'application.name'
    try:
        pactl = subprocess.check_output(['pactl', 'list', 'sink-inputs']).decode('utf-8')
    except subprocess.CalledProcessError as ex:
        raise
        return

    lines = [i.strip() for i in pactl.splitlines() if 'Sink Input' in i or arg in i]

    if option == 'm':
        names = [i[14:-1] for i in lines[1::2]]
    else:
        names = [i[20:-1] for i in lines[1::2]]
        
    nums = [i[12:] for i in lines[::2]]
    return names, nums

    
def dict_apps():
    """
    Returns a defaultdict of application names for keys and sink numbers for
    values.

    For example:
    >>> dict_apps()
    defaultdict(<class 'list'>, {'WEBRTC VoiceEngine': [5], 'java': [2828], 'Firefox': [5168, 5175]})
    
    There can be multiple id's per application, such as for Firefox, where each
    tab has its own audio stream.
    """
    sinks = defaultdict(list)
    names, nums = list_sink_inputs('a')
    for i in range(len(names)):
        sinks[names[i]].append(nums[i])
    return sinks


def set_sink_input_vol(sink, vol):
    subprocess.call(['pactl', 'set-sink-input-volume', sink, str(vol)+'%'])
    

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
    

def set_active_sink_input_vol(vol):
    try:
        win_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode('utf-8')
        win_info = subprocess.check_output(['xwininfo', '-id', win_id]).decode('utf-8')
    except subprocess.CalledProcessError as ex:
        raise
        return
    
    win_name = win_info.splitlines()[1][32:-1]
    try:
        win_name = win_name[:win_name.rindex(' — ')]
    except ValueError as ex:
        raise
    
    names, nums = list_sink_inputs('m')
    try:
        i = names.index(win_name)
    except ValueError as ex:
        raise
    set_sink_input_vol(nums[i], vol)
