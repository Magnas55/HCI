import PySimpleGUI as sg
from toolbox import toolbox_commands
import os
from execution import  run_code, list_named_versions, load_named_version, delete_named_version, save_named_version

def handle_events(event, values, window):
    if event == "Run Code":
        run_code(window.TKEditor.text.get("1.0", "end-1c"), window["-OUTPUT-"], window["-VARS-"])

    if event == "Reset":
        window["-OUTPUT-"].update("")
        window["-VARS-"].update("")
        window.TKEditor.text.delete("1.0", "end")

    if event == "-TOOLBOX-" and values["-TOOLBOX-"]:
        selected_item = values["-TOOLBOX-"][0]
        for category, items in toolbox_commands.items():
            if selected_item in items:
                new_code = f"# Insert a comment here\n{items[selected_item]}\n"
                current_code = window.TKEditor.text.get("1.0", "end-1c").rstrip()
                updated_code = (current_code + "\n\n" + new_code).strip()
                window.TKEditor.text.delete("1.0", "end")
                window.TKEditor.text.insert("1.0", updated_code)
                window.TKEditor.highlight_syntax()

    elif event == "Save Version":
        code = window.TKEditor.text.get("1.0", "end-1c")
        filename = sg.popup_get_text("Enter version name (no extension):", "Save Code Version")
        if filename:
            success, message = save_named_version(code, filename)
            sg.popup(message)
            window["-SAVED_LIST-"].update(list_named_versions())

    elif event == "Load Version":
        selected = values["-SAVED_LIST-"]
        if selected:
            code = load_named_version(selected[0])
            window.TKEditor.text.delete("1.0", "end")
            window.TKEditor.text.insert("1.0", code)
            window.TKEditor.highlight_syntax()


    elif event == "Delete Version":
        selected = values["-SAVED_LIST-"]
        if selected:
            confirm = sg.popup_yes_no(f"Are you sure you want to delete '{selected[0]}'?")
            if confirm == "Yes":
                deleted = delete_named_version(selected[0])
                if deleted:
                    sg.popup("Deleted successfully.")
                    window["-SAVED_LIST-"].update(list_named_versions())
                else:
                    sg.popup_error("Could not delete the file.")