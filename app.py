import PySimpleGUI as sg
import json

# Define the default settings
settings = {
    "testLoopCount" : 1,
    'setting2': 'value2',
    'setting3': 'value3'
}

def main():
    # Check if the settings file exists
    try:
        # If the file exists, read the existing settings from the file
        with open('settings.json', 'r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create it and write the default settings to the file
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    layout = [[sg.Text('Enter your name:'), sg.Input()],
            [sg.Button('Ok'), sg.Button('Change Amount'), sg.Text(settings["testLoopCount"])],
            [sg.Button('Close')]]

    window = sg.Window('Window Title', layout)
    save = ""
    while True:
        
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        if event == 'Change Amount':
            try:
                temp = int(sg.popup_get_text('How many times to repeat benchmark?', 'Tests'))
                settings['testLoopCount'] = temp
            except ValueError:
                sg.popup_error("Invalid Number: Please enter a whole number")

        else:
            print('You entered', values[0], settings["testLoopCount"])

    window.close()

    # Save the updated settings to the file
    with open('settings.json', 'w') as f:
        json.dump(settings, f)


if __name__ == '__main__':
    main()
