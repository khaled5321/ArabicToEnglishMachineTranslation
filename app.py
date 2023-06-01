import requests
import threading
from tkinter import *


DATA = []

def get_data(text):
    global DATA
    response = requests.post("https://khaled5321-artoen.hf.space/run/predict", json={
        "data": [
            text,
        ]
    }).json()
    DATA.append(response['data'][0])


class Lingolin:
    def __init__(self):
        self.language = 'english'
        self.mainWindow = Tk()
        self.title = Label(self.mainWindow, 
                           text='Translate Arabic to English', 
                           font=('Helvetica', 24, 'bold'))

        self.ar_label = Label(self.mainWindow, text='Enter Arabic text', font=("Helvetica", 16, "bold"))
        self.en_label = Label(self.mainWindow, text='Enter English text', font=("Helvetica", 16, "bold"))

        self.txt_ar = Text(self.mainWindow, height=10, width=35)
        self.txt_en = Text(self.mainWindow, height=10, width=35, state=DISABLED)

        self.status = Label(self.mainWindow,
                            text='', 
                            foreground="red", 
                            font=("Helvetica", 16, "bold"))

        self.change_language_button = Button(self.mainWindow,
                                             text='Arabic',
                                             foreground='white',
                                             bg='black',
                                             padx=5,
                                             pady=5,
                                             font=("Helvetica", 12, "bold"),
                                             command=self.change_language)
        
        self.translate_btn = Button(self.mainWindow,
                                    text="Translate",
                                    bg='blue',
                                    padx=5,
                                    pady=5,
                                    foreground='white',
                                    font=("Helvetica", 12, "bold"),
                                    command=self.translate)

        self.setup()
        self.mainWindow.mainloop()  

    def setup(self):
        self.mainWindow.title('Lingolin')
        self.mainWindow.geometry('700x450')
        self.mainWindow.grid_columnconfigure(0, weight=1)

        self.title.grid(row=0, columnspan=2, pady=(10, 20))
        self.ar_label.grid(row=1, column=0)
        self.en_label.grid(row=1, column=1)

        self.txt_ar.grid(row=2, column=0)
        self.txt_en.grid(row=2, column=1, padx=(0, 20))

        self.status.grid(row=3, columnspan=2, pady=10)

        self.translate_btn.grid(row=4, columnspan=2, pady=10)
        self.change_language_button.grid(row=5, columnspan=2)


    def swap(self):
        x1 = self.ar_label.grid_info()
        x2 = self.en_label.grid_info()

        self.ar_label.grid_configure(x2)
        self.en_label.grid_configure(x1)

        x1 = self.txt_ar.grid_info()
        x2 = self.txt_en.grid_info()
        
        self.txt_ar.grid_configure(x2)
        self.txt_en.grid_configure(x1)


    def change_language(self):
        self.status.config(text='')

        if self.language == 'english':
            self.language = 'arabic'
            self.title.config(text='ترجم من العربية إلى الإنجليزية')
            self.ar_label.config(text='أدخل النص العربي')
            self.en_label.config(text='أدخل النص الإنجليزي')
            self.change_language_button.config(text='إنجليزي')
            self.translate_btn.config(text="ترجم")
            self.swap()

        else:
            self.language = 'english'
            self.title.config(text='Translate Arabic to English')
            self.ar_label.config(text='Enter Arabic text')
            self.en_label.config(text='Enter English text')
            self.change_language_button.config(text='Arabic')
            self.translate_btn.config(text="Translate")
            self.swap()


    def translate(self):
        self.translate_btn.config(state=DISABLED)
        self.change_language_button.config(state=DISABLED)
        self.txt_ar.config(state=DISABLED)
        text = self.txt_ar.get("1.0", 'end-1c')

        if text:
            if self.language == 'arabic':
                self.status.config(text='جاري الترجمة', foreground='green')
            else:
                self.status.config(text='Translating...', foreground='green')
            
            self.mainWindow.after(500, lambda:threading.Thread(target=get_data, args=(text,)).start())

            self.check_data()

        else:
            if self.language == 'arabic':
                self.status.config(text='أدخل النص المراد ترجمته أولا')
            else:
                self.status.config(text='Please enter text to translate first')


    def check_data(self):
        global DATA
        if not DATA:
            self.mainWindow.after(500, self.check_data)
        else:
            self.txt_en.config(state = NORMAL)
            self.txt_en.delete('1.0', END)
            self.txt_en.insert(END, DATA[0])
            self.txt_en.config(state=DISABLED)
            self.translate_btn.config(state=NORMAL)
            self.change_language_button.config(state=NORMAL)
            self.txt_ar.config(state=NORMAL)


            if self.language == 'arabic':
                self.status.config(text='تم', foreground='green')
            else:
                self.status.config(text='Done', foreground='green')
        
            DATA = []


app = Lingolin()