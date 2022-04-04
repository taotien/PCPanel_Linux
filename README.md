# PCPanel Linux

This is a WIP utility to have your PCPanel control PulseAudio application and
device volumes on Linux, written in Python.

I don't know how to use PA's API (if there is one), so instead this calls
`pactl` to get application names and set volumes.

Haven't touched Python in a while, so excuse the nasty code.

## How it works

What the knobs and buttons on the PCPanel do is simply spit out 3 bytes of raw
data over HID, like:

`01, 05, 87`

1st byte: 01 = slider/knob; 02 = button

2nd byte: 00-04 = knobs; 05-08 = sliders

3rd byte: 00-FF = 256 values, or 00/01 for unpress/press of button

## TODO

- PipeWire!!!

- maybe create fake pulseaudio devices to get around volume control conflicts
- background polling to constantly set volume?
- actually handle exceptions
- make pactl list call own func with opt name or application
- wayland and pipewire, currently only x and pulseaudio
- RGB (OpenRGB)
- GUI
- check out pacmd options
- daemonize?
- this gets active window
  - xdotool getactivewindow | xargs xwininfo -id
  - figure if x window name doesn't match pa names, do fuzzy?
- fork/exec?
- change Popen to check_output and catch exceptions
- OBS integration and other feature parity
- non-pro pcpanels
- multiple pcpanels
- investigate error on close
- media controls

```shell
python3: /var/tmp/portage/dev-libs/libusb-1.0.25/work/libusb-1.0.25/libusb/os/threads_posix.h:46: usbi_mutex_lock: Assertion `pthread_mutex_lock(mutex) == 0' failed.
fish: Job 1, './main.py' terminated by signal SIGABRT (Abort)
```
Seems to be because I'm using ctrl-c to stop the loop, terminating from a
process manager avoids it. Doesn't seem to have any real consequences

## Depends

- PulseAudio
- hidapi

## Known Issues

- volume adjustment causes glitches like crackling and/or fast forwarding

Done further research, this seems to be a PulseAudio issue? Also, effect differs
based on `resample-method` set in `/etc/pulse/daemon.conf`. soxr-vhq causes the
ff, speex-float-10 only crackles. [pulseaudio gitlab](https://gitlab.freedesktop.org/pulseaudio/pulseaudio/-/issues/981)

- certain applications don't report the same things for audio and window name,
  thus we are unable to be detected for the active window feature

- YouTube's player volume conflicts with app volume, and overrides it causing
  it to be suddenly loud when playback changes
