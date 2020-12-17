"""
The main file to start with.
Responsible for interface.
"""
from tkinter import Tk, ttk, filedialog, END
from preparation import get_raw_path, read_all_txt_from_dir
from customtext import CustomText


INVALID_WORD_MESSAGE = 'Please, input correct word!'
NO_FILE_RESULTS_MESSAGE = 'NO MATCHES \n\n\n\n'
WORDS_COLORS = ("Pink", "Blue", "Green")


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
        self.entry_button.grid(column=0, row=5)

    def display_result(self):
        self.result_text = CustomText(self)
        self.result_text.tag_configure(WORDS_COLORS[0], foreground="#ff087f")
        self.result_text.tag_configure(WORDS_COLORS[1], foreground="blue")
        self.result_text.tag_configure(WORDS_COLORS[2], foreground="green")
        self.result_text.config(width=90, height=30)
        self.result_text.grid(column=0, row=6, columnspan=2,
                              padx=20, pady=20)

        self.text_scroll = ttk.Scrollbar(self,
            command=self.result_text.yview, orient="vertical")
        self.text_scroll.grid(row=6, column=1, sticky='nse',
                              padx=5, pady=20)

        self.result_text.configure(yscrollcommand=self.text_scroll.set)

        entered_str_list = self.entry_word.get().strip().split()
        if not entered_str_list:
            # displaying corresponding message if input is empty
            self.result_text.insert(END, INVALID_WORD_MESSAGE)
        else:
            entered_words_list = [' ' + entered_str[:-1].lower()
                if entered_str[-1] == '*' else ' ' + entered_str.lower()
                for entered_str in entered_str_list]

            for file in self.files_list:
                self.result_text.insert(END, file + '\n' * 3)
                has_results = False

                with open(file, encoding="utf8") as f:
                    line_num = 1
                    for line in f:
                        if all([word in line.lower()
                                for word in entered_words_list]):
                            line_result = f'Line #{line_num}:\n{line}' + '\n' * 2
                            self.result_text.insert(END, line_result)
                            has_results = True
                        line_num += 1

                if not has_results:
                    self.result_text.insert(END, NO_FILE_RESULTS_MESSAGE)

            for i, word_str in enumerate(entered_str_list):
                word_regex = r'(?i){}'.format(entered_words_list[i])
                if word_str[-1] == '*':
                    word_regex += r'\w*'
                else:
                    word_regex += ' '
                self.result_text.highlight_pattern(word_regex, WORDS_COLORS[i])


# Starting the application by drawing the new window
root = Root()
root.resizable(False, False)
root.mainloop()
