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

## Depends

- PulseAudio
- hidapi
