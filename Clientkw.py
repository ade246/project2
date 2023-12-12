"""client.py 
### KHARI WALLACE, 100807131, TPRG 2131 ###

TPRG 2131 Fall 2023 Project 2
December 14th, 2023
Khari Wallace <khari.wallace@dcmail.ca>

# This client runs on Pi, sends Pi's 5 arguments from the vcgencmds, plus 50 iterations
of the data set. sent as Json object.
"""


import socket
import json
import PySimpleGUI as sg
import time
import os
import threading

def get_cpu_clock_frequency():
    frequency = os.popen('vcgencmd measure_clock arm').readline()
    return frequency.strip()

