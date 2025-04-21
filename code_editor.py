import tkinter as tk
import keyword
import builtins

class CodeEditor(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Line numbers panel
        self.line_numbers = tk.Text(self, width=3, padx=5, takefocus=0, border=0,
                                    background="white", state="disabled", wrap="none",
                                    highlightthickness=0, relief="flat", font=("JetBrains Mono", 12),
                                    fg="#777777")
        self.line_numbers.tag_configure("right", justify="right")
        self.line_numbers.pack(side="left", fill="y")

        # Code editor
        self.text = tk.Text(self, font=("JetBrains Mono", 12), wrap="none", undo=True,
                            bg="white", fg="#444444", insertbackground="black",
                            highlightthickness=0, relief="flat")
        self.text.pack(side="right", fill="both", expand=True)

        # Tags
        self.text.tag_configure("keyword", foreground="#800080")
        self.text.tag_configure("builtin", foreground="#C78A00")
        self.text.tag_configure("comment", foreground="#3E5F27") 
        self.text.tag_configure("string", foreground="#a42107")
        self.text.tag_configure("primitive", foreground="blue")

        # Events
        self.text.bind("<KeyRelease>", self.on_key_release)
        self.text.bind("<<Paste>>", self.on_key_release)
        self.text.bind("<MouseWheel>", self.sync_scroll)
        self.text.bind("<Configure>", self.update_line_numbers)
        self.text.bind("<Any-KeyPress>", self.update_line_numbers)

        # Init
        self.highlight_syntax()
        self.update_line_numbers()

    def on_key_release(self, event=None):
        self.highlight_syntax()
        self.update_line_numbers()

    def sync_scroll(self, event=None):
        self.line_numbers.yview_moveto(self.text.yview()[0])
        return "break"

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")

        line_count = int(self.text.index('end-1c').split('.')[0])
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))

        self.line_numbers.insert("1.0", line_numbers_text, "right")
        self.line_numbers.config(state="disabled")

        self.line_numbers.yview_moveto(self.text.yview()[0])

    def highlight_syntax(self):
        self.text.tag_remove("keyword", "1.0", "end")
        self.text.tag_remove("builtin", "1.0", "end")
        self.text.tag_remove("comment", "1.0", "end")
        self.text.tag_remove("string", "1.0", "end")
        self.text.tag_remove("primitive", "1.0", "end")

        content = self.text.get("1.0", "end-1c")
        tokens = content.replace("(", " ").replace(")", " ").replace(":", " ").split()
        builtin_names = set(dir(builtins))

        # Comments
        start_index = "1.0"
        while True:
            pos = self.text.search("#", start_index, stopindex="end")
            if not pos:
                break
            line_end = self.text.search("\n", pos, stopindex="end")
            if not line_end:
                line_end = "end-1c"
            self.text.tag_add("comment", pos, line_end)
            start_index = line_end

        # Strings - double quotes
        start_index = "1.0"
        while True:
            pos = self.text.search("\"", start_index, stopindex="end")
            if not pos:
                break
            end_pos = self.text.search("\"", f"{pos}+1c", stopindex="end")
            if not end_pos:
                break
            end_index = f"{end_pos}+1c"
            self.text.tag_add("string", pos, end_index)
            start_index = end_index

        # Strings - single quotes
        start_index = "1.0"
        while True:
            pos = self.text.search("'", start_index, stopindex="end")
            if not pos:
                break
            end_pos = self.text.search("'", f"{pos}+1c", stopindex="end")
            if not end_pos:
                break
            end_index = f"{end_pos}+1c"
            self.text.tag_add("string", pos, end_index)
            start_index = end_index

        # Primitives
        for const in ["True", "False", "None"]:
            start_index = "1.0"
            while True:
                pos = self.text.search(const, start_index, stopindex="end")
                if not pos:
                    break
                end_index = f"{pos}+{len(const)}c"
                matched = self.text.get(pos, end_index)
                if matched == const:
                    self.text.tag_add("primitive", pos, end_index)
                start_index = end_index

        # Numbers
        start_index = "1.0"
        while True:
            pos = self.text.search(r'\d+', start_index, stopindex="end", regexp=True)
            if not pos:
                break
            end_index = self.text.index(f"{pos} wordend")
            self.text.tag_add("primitive", pos, end_index)
            start_index = end_index

        # Keywords and built-ins
        for token in set(tokens):
            start_index = "1.0"
            while True:
                pos = self.text.search(token, start_index, stopindex="end")
                if not pos:
                    break
                end_index = f"{pos}+{len(token)}c"
                matched = self.text.get(pos, end_index)

                if matched == token:
                    if token in keyword.kwlist:
                        self.text.tag_add("keyword", pos, end_index)
                    elif token in builtin_names:
                        self.text.tag_add("builtin", pos, end_index)

                start_index = end_index

def create_code_editor(canvas):
    tk_canvas = canvas.TKCanvas
    editor = CodeEditor(tk_canvas.master)
    tk_canvas.create_window((0, 0), window=editor, anchor="nw")
    return editor