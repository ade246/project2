"""server.py 
### KHARI WALLACE, 100807131, TPRG 2131 ###

TPRG 2131 Fall 2023 Project 2
December 14th, 2023
Khari Wallace <khari.wallace@dcmail.ca>

# This server runs on Pi, the server acts as a central node that receives, processes,
and displays data from connected clients
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
    return sg.Window('Server', layout, finalize=True, size=(500, 300))

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

def main():
    window = create_window()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 1500))
    server_socket.listen(1)

    client_thread = None

    try:
        while True:
            event, values = window.read(timeout=10)

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            if event == '-TOGGLE_LED-':
                window['-LED-'].update(text_color='green' if values['-TOGGLE_LED-'] else 'white')

            if event == '-UPDATE_GUI-':
                data = values['-UPDATE_GUI-']
                window['-CORE_VOLTAGE-'].update(data["core_voltage"])
                window['-CORE_TEMP-'].update(data["core_temp"])
                window['-ARM_MEMORY-'].update(data["arm_memory"])
                window['-GPU_MEMORY-'].update(data["gpu_memory"])
                window['-CPU_FREQUENCY-'].update(data["cpu_frequency"])
                window['-ITERATION-'].update(str(data["iteration"]))

            if not client_thread:
                client_socket, addr = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, window), daemon=True)
                client_thread.start()

    except Exception as e:
        sg.popup_error("Error:", e)
    finally:
        server_socket.close()
        window.close()

if __name__ == '__main__':
    main()

