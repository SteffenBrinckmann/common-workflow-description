import logging, json
import tkinter as tk
from tkinter import font as tkFont

# based on https://stackoverflow.com/questions/63099026/fomatted-text-in-tkinter
class RichText(tk.Text):
    def __init__(self, *args, **kwargs):
        """Init rich text field in TK"""
        super().__init__(*args, **kwargs)
        # fonts
        default = tkFont.nametofont(self.cget("font"))
        defaultSize = default.cget("size")
        bold = tkFont.Font(**default.configure())
        bold.configure(weight="bold")
        self.tag_configure("bold", font=bold)
        italic = tkFont.Font(**default.configure())
        italic.configure(slant="italic")
        self.tag_configure("italic", font=italic)
        h1 = tkFont.Font(**default.configure())
        h1.configure(size=int(defaultSize * 1.5), weight="bold")
        self.tag_configure("h1", font=h1, spacing3=defaultSize)
        # bullet lists
        em = default.measure("m")
        lmargin2 = em + default.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insertItem(self, text: str, index: str = "end") -> None:
        """insert an item to the bullet point list

        Args:
          text (str): text to add
          index (str): location where to add
        """
        self.insert(index, f"\u2022 {text}\n", "bullet")
        return

    def insertText(self, text: str, style: str = "", index: str = "end") -> None:
        """insert rich text into window

        Args:
          text (str): text to add
          style (str): its style or format
          index (str): location where to add
        """
        self.insert(index, text, style)
        return

    def parseMD(self, text: str) -> None:
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
                self.insertItem(f"{line[2:]}")
            else:
                self.insertText(f"{line}\n", style)
        return


def window(text, paramAll, param):
    window = tk.Tk()
    window.geometry("340x500")  # set starting size of window
    window.maxsize(1000, 1000)  # width x height
    widget = RichText(window, width=40, height=15)
    widget.parseMD(text)
    widget.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    # question fields below
    ipadding = {"ipadx": 10, "ipady": 10, "padx": 5, "pady": 5, "sticky": "ew"}
    textFields = []
    paramAll |= param
    for idx, (key, value) in enumerate(paramAll.items()):
        nameF = tk.Label(window, text=key)
        nameF.grid(**ipadding, row=1 + idx, column=0)  # type: ignore[arg-type]
        textFields.append(tk.Entry(window))
        textFields[-1].insert(10, str(value))
        textFields[-1].grid(**ipadding, row=1 + idx, column=1)  # type: ignore[arg-type]

    fileName = ''
    metadata = {}
    def done():
        nonlocal fileName
        nonlocal metadata
        metadata = dict(paramAll)
        for idx, key in enumerate(paramAll):
            metadata[key] = textFields[idx].get()
        fileName = "" if "filename" not in metadata else metadata.pop("filename")
        logging.info(f"Save step file-name:{fileName}  metadata:\n{json.dumps(metadata, indent=2)}")
        window.quit()
        return fileName, metadata

    button = tk.Button(window, text="done", command=done)
    button.grid(**ipadding, row=4, column=1)  # type: ignore[arg-type]
    window.mainloop()
    return fileName, metadata