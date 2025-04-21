import PySimpleGUI as sg
from toolbox import get_toolbox_tree

def create_layout():
    toolbox_tree = get_toolbox_tree()

    # Toolbox pane
    toolbox_pane = [
        [sg.Text("Toolbox", font=("Arial", 12, "bold"))],
        [sg.Tree(data=toolbox_tree, headings=[], select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                 key="-TOOLBOX-", enable_events=True, show_expanded=False,
                 col0_width=20, expand_x=True, expand_y=True)]
    ]

    # Saved versions panel
    saved_versions_panel = [
        [sg.Text("Saved Versions", font=("Arial", 12, "bold"))],
        [sg.Listbox(values=[], size=(25, 10), key="-SAVED_LIST-", enable_events=True)],
        [sg.Button("Load Version", button_color=("black", "yellow")),
        sg.Button("Delete Version", button_color=("white", "red"))]

    ]

    # Combine both in a single left column
    left_column = sg.Column(toolbox_pane + saved_versions_panel, expand_y=True)

    # Code and output widgets
    code_canvas = sg.Canvas(key="-CODE_CANVAS-", size=(600, 400))
    var_display = sg.Multiline(size=(40, 4), key="-VARS-", disabled=True, expand_x=True)
    output_panel = sg.Multiline(size=(30, 15), key="-OUTPUT-", disabled=True, expand_x=True, expand_y=True)

    layout = [
        [sg.Pane([
            left_column,
            sg.Column([
                [sg.Text("Code Editor")],
                [code_canvas],
                [sg.Button("Run Code"), sg.Button("Reset"), sg.Button("Save Version", button_color=("white", "green"))],
                [sg.Text("Variables:")],
                [var_display]
            ], expand_x=True, expand_y=True),
            sg.Column([
                [sg.Text("Output:")],
                [output_panel]
            ], expand_x=True, expand_y=True)
        ], orientation="h", handle_size=10, expand_x=True, expand_y=True)]
    ]

    return layout
