#!/usr/bin/python3

import PCPanel

if __name__ == "__main__":
    p = PCPanel.PCPanel()
    try:
        while True:
            p.loop()
    except KeyboardInterrupt:
        exit()
