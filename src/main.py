from threading import Thread
import PySimpleGUI as sg
from pathlib import Path
import json
import os


from datetime import datetime, timedelta
import time

from phone import phone

def log(message: str) -> str:
    return print(f'{datetime.now().strftime("%H:%M:%S")} --- ' + message)

def connectPhone(device) -> None or phone:
    try:
        device = phone()
        log("Device Connected")
        return device
    except AttributeError:
        sg.popup_error("Device Not Connected")
        log("Connection Error")
        return None
    

def main():
    settingDirect = Path("./settings.json")
    settings = {
        "testLoopCount" : 1,
        'setting2': 'value2',
        'setting3': 'value3'
    }

    device = None

    try:
        with open("settings.json", 'r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        with open(settingDirect, 'w') as f:
            json.dump(settings, f)

    layout = [[sg.Button('Init Device')],
            [sg.Output(size=(80, 20), key='output')],
            [sg.Button('Start Benchmarks'), sg.Button('Benchmark Count')],
            [sg.Button('Close')]]

    window = sg.Window('Window Title', layout)

    while True:
        
        event, values = window.read()

        if event == 'Close' or event == sg.WIN_CLOSED:
            break

        elif event == 'Benchmark Count':
            try:
                temp = int(sg.popup_get_text('How many times to repeat benchmark?', 'Tests'))
                log(f"Benchmark will run {temp} times")
                settings['testLoopCount'] = temp
            except ValueError:
                sg.popup_error("Invalid Number: Please enter a whole number")
        
        elif event == 'Start Benchmarks':
            if device == None:
                log("Device not connected(Connect the Device and click Init Device)")
            else:
                Thread(target=device.repeatTestAntutu, daemon = True, args=([settings['testLoopCount']])).start()

        elif event == 'Init Device':
            device = connectPhone(device)

    window.close()

    with open(settingDirect, 'w') as f:
        json.dump(settings, f)


if __name__ == '__main__':
    main()
