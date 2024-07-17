""" Main window and class to display the markdown text in the window """
import json
import logging
import tkinter as tk
from tkinter import font as tkFont
from tkinter import filedialog

# based on https://stackoverflow.com/questions/63099026/fomatted-text-in-tkinter
class RichText(tk.Text):
    """ Class to display the markdown text in the window """
    def __init__(self, *args, **kwargs):
        """Init rich text field in TK"""
        super().__init__(*args, **kwargs)
        # fonts
        default = tkFont.nametofont(self.cget("font"))
        default_size = default.cget("size")
        bold = tkFont.Font(**default.configure())
        bold.configure(weight="bold")
        self.tag_configure("bold", font=bold)
        italic = tkFont.Font(**default.configure())
        italic.configure(slant="italic")
        self.tag_configure("italic", font=italic)
        h1 = tkFont.Font(**default.configure())
        h1.configure(size=int(default_size * 1.5), weight="bold")
        self.tag_configure("h1", font=h1, spacing3=default_size)
        # bullet lists
        em = default.measure("m")
        lmargin2 = em + default.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)


    def insert_item(self, text: str, index: str = "end") -> None:
        """insert an item to the bullet point list

        Args:
          text (str): text to add
          index (str): location where to add
        """
        self.insert(index, f"\u2022 {text}\n", "bullet")


    def insert_text(self, text: str, style: str = "", index: str = "end") -> None:
        """insert rich text into window

        Args:
          text (str): text to add
          style (str): its style or format
          index (str): location where to add
        """
        self.insert(index, text, style)


    def parse_markdown(self, text: str) -> None:
        """Poor mans markdown parser by SB
        Markdown features understood:
        - headline #
        - items -
        - bold **text**
        - italics *text*
        - comments <--- text --->

        Args:
          text (str): markdown text
        """
        for line in text.split("\n"):
            if line.startswith("<!---") and line.endswith("-->"):  # comment
                continue
            style = ""
            if line.startswith("# "):
                style = "h1"
                line = line[2:]
            elif line.startswith("**") and line.endswith("**"):
                style = "bold"
                line = line[2:-2]
            elif line.startswith("*") and line.endswith("*"):
                style = "italic"
                line = line[1:-1]
            if line.startswith("- "):
                self.insert_item(f"{line[2:]}")
            else:
                self.insert_text(f"{line}\n", style)


def main_window(text, parameter_all, param):
    """ Main window

    Args:
      text (str): text in the text area
      parameter_all (dict): all parameters
      param (dict): specific parameter

    Returns:
      tuple of file name, parameter
    """
    window = tk.Tk()
    window.geometry("340x500")  # set starting size of window
    window.maxsize(1000, 1000)  # width x height
    widget = RichText(window, width=40, height=15)
    widget.parse_markdown(text)
    widget.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    # question fields below
    padding = {"ipadx": 10, "ipady": 10, "padx": 5, "pady": 5, "sticky": "ew"}
    text_fields = []
    parameter_all |= param
    file_name = ''
    metadata = {}

    def done():
        nonlocal metadata
        metadata = dict(parameter_all)
        for idx, key in enumerate(parameter_all):
            if key == 'file_name':
                continue
            metadata[key] = text_fields[idx].get()
        file_name = "" if "file_name" not in metadata else metadata.pop("file_name")
        logging.info("Save step file-name:%s  metadata:\n%s", file_name,
                     json.dumps(metadata, indent=2))
        window.destroy()
        return file_name, metadata

    def select_file():
        reply = filedialog.askopenfilename()
        if reply is not None:
            nonlocal file_name
            file_name = reply

    for idx, (key, value) in enumerate(parameter_all.items()):
        name = tk.Label(window, text=key)
        name.grid(**padding, row=1 + idx, column=0)  # type: ignore[arg-type]
        if key == 'file_name':
            file_button = tk.Button(window, text="select file", command=select_file)
            file_button.grid(**padding, row=1 + idx, column=1)
        else:
            text_fields.append(tk.Entry(window))
            text_fields[-1].insert(10, str(value))
            text_fields[-1].grid(**padding, row=1 + idx, column=1)  # type: ignore[arg-type]

    button = tk.Button(window, text="done", command=done)
    button.grid(**padding, row=4, column=1)  # type: ignore[arg-type]
    window.mainloop()
    return file_name, metadata
