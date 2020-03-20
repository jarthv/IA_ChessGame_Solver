from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class LoadFile(Tk):
    def __init__(self):
        super(LoadFile, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(100, 100)

        self.Path = ''

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)

        self.button1()
        self.button2()

    def set_Path(self, thisPath):
        self.Path = thisPath

    def get_path(self):
        return self.Path

    def button1(self):
        self.button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.button.grid(column=1, row=1)

    def button2(self):
        self.button = ttk.Button(self.labelFrame, text="Ok", command=self.salir)
        self.button.grid(column=2, row=1)

    def salir(self):
        self.destroy()

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=
        (("text files", "*.txt"), ("all files", "*.*")))
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)
        self.set_Path(self.filename)
