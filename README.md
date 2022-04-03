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

## Depends

- PulseAudio
- hidapi

## Issues

- On my system, adjusting volume causes certain media (firefox) to fast forward
  a frame?

