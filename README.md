# PCPanel Linux

This is a WIP utility to have your PCPanel control PulseAudio application and
device volumes on Linux, written in Python.

I don't know how to use PA's API (if there is one), so instead this calls
`pactl` to get application names and set volumes.

Haven't touched Python in a while, so excuse the nasty code.

## TODO

- RGB (OpenRGB)
- GUI

## Depends

- PulseAudio
- hidapi

## Issues

- On my system, adjusting volume causes certain media to fast forward a frame?
