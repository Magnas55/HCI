import PySimpleGUI as sg
from ui import create_layout
from events import handle_events
from code_editor import create_code_editor
from execution import list_named_versions


def main():
    layout = create_layout()
    window = sg.Window("Glide - Hybrid IDE", layout, resizable=True, finalize=True)
    window["-SAVED_LIST-"].update(list_named_versions())

    
    # Create and attach the custom CodeEditor into the Canvas
    if "-CODE_CANVAS-" in window.AllKeysDict:
        editor = create_code_editor(window["-CODE_CANVAS-"])
        window.TKEditor = editor  # This makes it available to events.py

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        handle_events(event, values, window)
    window.close()

if __name__ == "__main__":
    main()