"""server.py 
### KHARI WALLACE, 100807131, TPRG 2131 ###

TPRG 2131 Fall 2023 Project 2
December 14th, 2023
Khari Wallace <khari.wallace@dcmail.ca>

# This server runs on Pi and Pc, the server acts as a central node that receives,
processes, and displays data from the connected client
"""

import socket
import json
import PySimpleGUI as sg
import threading

def create_window():
    sg.theme('DarkTeal5')
    layout = [
        [sg.Text('Connection Status: '), sg.Text('○', text_color='green', key='-LED-', font=('Helvetica', 16))],
        [sg.Text('Core Voltage:', font=('Helvetica', 14)), sg.Text('', key='-CORE_VOLTAGE-', font=('Helvetica', 14))],
        [sg.Text('Core Temperature:', font=('Helvetica', 14)), sg.Text('', key='-CORE_TEMP-', font=('Helvetica', 14))],
        [sg.Text('ARM Memory:', font=('Helvetica', 14)), sg.Text('', key='-ARM_MEMORY-', font=('Helvetica', 14))],
        [sg.Text('GPU Memory:', font=('Helvetica', 14)), sg.Text('', key='-GPU_MEMORY-', font=('Helvetica', 14))],
        [sg.Text('CPU Frequency:', font=('Helvetica', 14)), sg.Text('', key='-CPU_FREQUENCY-', font=('Helvetica', 14))],
        [sg.Text('Iteration:', font=('Helvetica', 14)), sg.Text('', key='-ITERATION-', font=('Helvetica', 14))],
        [sg.Button('Exit', font=('Helvetica', 14))]
    ]
    return sg.Window('Server', layout, finaliz e=True, size=(500, 300))

def handle_client(client_socket, window):
    led_on = True
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Toggle the LED color
            led_on = not led_on
            window.write_event_value('-TOGGLE_LED-', led_on)

            data = json.loads(data)
            window.write_event_value('-UPDATE_GUI-', data)
    except socket.error:
        pass
    finally:
        client_socket.close()



