import PySimpleGUI as sg
import json
from phone import phone
import time
from datetime import datetime, timedelta
from threading import Thread

# Define the default settings
settings = {
    "testLoopCount" : 1,
    'setting2': 'value2',
    'setting3': 'value3'
}

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

    device = None

    # Check if the settings file exists
    try:
        # If the file exists, read the existing settings from the file
        with open('./src/settings.json', 'r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create it and write the default settings to the file
        with open('./src/settings.json', 'w') as f:
            json.dump(settings, f)

    layout = [[sg.Button('Init Device')],
            [sg.Output(size=(80, 20), key='output')],
            [sg.Button('Start Benchmarks'), sg.Button('Benchmark Count')],
            [sg.Button('Close')]]

    window = sg.Window('Window Title', layout)

    while True:
        
        event, values = window.read()
        if event == 'Close':
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

    # Save the updated settings to the file
    with open('./src/settings.json', 'w') as f:
        json.dump(settings, f)


if __name__ == '__main__':
    main()
