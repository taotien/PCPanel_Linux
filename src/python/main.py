#!/usr/bin/python3

import PCPanel
import config

if __name__ == "__main__":
    p = PCPanel.PCPanel(config.inputs)
    try:
        while True:
            p.loop()
    except KeyboardInterrupt:
        exit()
