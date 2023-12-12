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

def create_window():
    sg.theme('DarkTeal5')
    layout = [
        [sg.Text('Connection Status: '), sg.Text('○', text_color='red', key='-LED-', font=('Helvetica', 16))],
        [sg.Button('Start Sending Data', font=('Helvetica', 14)), sg.Button('Disconnect', font=('Helvetica', 14))],
        [sg.Button('Exit', font=('Helvetica', 14))]
    ]
    return sg.Window('Client', layout, finalize=True, size=(500, 300))

def send_data(server_socket, window, stop_event):
    for iteration in range(1, 51):
        if stop_event.is_set():
            break
        cpu_frequency = get_cpu_clock_frequency()
        data = {
            "core_voltage": f"{1.2 + iteration * 0.01}V",
            "core_temp": f"{55 + iteration * 0.1}°C",
            "arm_memory": f"{512 + iteration}MB",
            "gpu_memory": f"{256 + iteration}MB",
            "cpu_frequency": cpu_frequency,
            "iteration": iteration
        }
        server_socket.sendall(json.dumps(data).encode())
        time.sleep(2)

def main():
    window = create_window()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    data_thread = None
    stop_event = threading.Event()

    try:
        server_socket.connect(('127.0.0.1', 1500))  # Replace with server IP if different
        window['-LED-'].update(text_color='green')
        connected = True
        print("Connected to the server.")

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            if event == 'Start Sending Data' and connected and not data_thread:
                stop_event.clear()
                data_thread = threading.Thread(target=send_data, args=(server_socket, window, stop_event), daemon=True)
                data_thread.start()

            if event == 'Disconnect' and connected:
                stop_event.set()
                if data_thread:
                    data_thread.join()
                server_socket.close()
                window['-LED-'].update(text_color='red')
                connected = False
                data_thread = None
                print("Disconnected from the server.")

    except Exception as e:
        sg.popup_error("Error:", e)
    finally:
        if connected:
            server_socket.close()
        window.close()

if __name__ == '__main__':
    main()


