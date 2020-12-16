"""
The main file to start with.
Responsible for interface.
"""
from tkinter import Tk, ttk, filedialog, Text, END
from preparation import get_raw_path, read_all_txt_from_dir


class Root(Tk):
    """
    A class for new window painting.
    """
    def __init__(self):
        super(Root, self).__init__()
        self.title("Concordancer3000")
        self.minsize(640, 6)

        self.style = ttk.Style()
        self.style.configure('W.TLabelframe.Label')
        self.style.configure('W.TButton')

        self.labelFrame = ttk.LabelFrame(self, text="Open Directory",
                                         style='W.TLabelframe')
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)
        self.filename = None

        self.display_browse_button()

    def display_browse_button(self):
        self.browse_button = ttk.Button(
            self.labelFrame, text="Browse A Directory To Read",
            command=self.read_file_dialog, style='W.TButton')
        self.browse_button.grid(column=1, row=1)

    def read_file_dialog(self):
        self.filename = filedialog.askdirectory(title="Select A File")
        self.label = ttk.Label(self.labelFrame, text="",
                               style='W.TLabelframe.Label')
        self.label.grid(column=1, row=2)
        self.label.configure(text=f'From: {self.filename}')

        self.filename = get_raw_path(self.filename)
        self.files_list = read_all_txt_from_dir(self.filename)

        self.word_label = ttk.Label(text="Please, input words: ",
                                    style='W.TLabelframe.Label')
        self.word_label.grid(column=0, row=3)

        self.entry_word = ttk.Entry(self)
        self.entry_word.config(width=50)
        self.entry_word.grid(column=0, row=4)
        self.entry_button = ttk.Button(self,
                                       text="Press to display result",
                                       command=self.display_result)
        self.entry_button.grid(column=1, row=5)

        self.window_text = ttk.Label(
            text="Please, choose context width:")
        self.window_text.grid(column=1, row=3)
        self.window_spin = ttk.Spinbox(self, from_=25, to=200, width=5)
        self.window_spin.grid(column=1, row=4)

    def display_result(self):
        self.entered_str = self.entry_word.get()


# Starting the application by drawing the new window
root = Root()
root.mainloop()
