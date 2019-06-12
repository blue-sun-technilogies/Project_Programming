from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import os.path
from platform import system
import re
from tkinter.filedialog import askopenfilename
from chardet.universaldetector import UniversalDetector
from calculation import mainCalc


ENTRY_BG_CLEAN = '#FFFFFF'
ENTRY_BG_ERROR = 'orange'
FRM_BG = '#d9d9d9'
LBL_BG_CLEAN = FRM_BG
LBL_BG_ERROR = 'orange'


class HoverInfo(Menu):
    def __init__(self, parent, text, command=None):
        self._com = command
        Menu.__init__(self, parent, tearoff=0)
        if not isinstance(text, str):
            raise TypeError('Trying to initialise a Hover Menu with a non \
            string type: ' + text.__class__.__name__)
        toktext = re.split('\n', text)
        for t in toktext:
            self.add_command(label=t)
            self._displayed = False
            self.master.bind("<Enter>", self.display)
            self.master.bind("<Leave>", self.remove)

    def display(self, event):
        if not self._displayed:
            self._displayed = True
            self.post(event.x_root, event.y_root)
        if self._com is not None:
            self.master.unbind_all("<Return>")
            self.master.bind_all("<Return>", self.click)

    def remove(self, event):
        if self._displayed:
            self._displayed = False
            self.unpost()
        if self._com is not None:
            self.unbind_all("<Return>")

    def click(self, event):
        self._com()


# This function finds the file name.
def insert_file():
    global file_name  # Inputted file name.
    file_name = fd.askopenfilename()
    if file_name:
        detector = UniversalDetector()
        with open(file_name, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        if detector.result['encoding'] != 'UTF-8-SIG':
            file_name = ''
            btn_file['text'] = 'Выберите файл..'
            messagebox.showerror('Неверная кодировка файла',
                                 'Неверная кодировка\
                                  файла.Требуется UTF-8-SIG,\
                                   обнаружена ' + detector.result['encoding'])
        else:
            lbl_file['bg'] = LBL_BG_CLEAN
            btn_file['text'] = file_name


# Method button for selecting the output file.
def output_file_fun():
    global output_file_name  # Outputted file name.
    output_file_name = fd.asksaveasfilename() + '.doc'  # create .doc file.
    if output_file_name:
        btn_outfile['text'] = output_file_name
        lbl_outfile['bg'] = LBL_BG_CLEAN


# Clean entered values and file paths
def clean():
    global output_file_name, file_name, type_days_only_work
    output_file_name = ''
    file_name = ''
    type_days_only_work = True
    data_size.set('')
    data_days.set('')
    lbl_size['text'] = 'Пени (вещественное положительное значение)'
    lbl_days['text'] = 'Количество дней без штрафа (целое положительное значение)'
    lbl_size['bg'] = LBL_BG_CLEAN
    lbl_days['bg'] = LBL_BG_CLEAN
    type_days_only_work = False
    change_type_days()
    ent_size['bg'] = ENTRY_BG_CLEAN
    ent_days['bg'] = ENTRY_BG_CLEAN
    btn_file['text'] = 'Выберите файл...'
    btn_outfile['text'] = 'Выберите файл...'
    lbl_outfile['bg'] = LBL_BG_CLEAN
    lbl_file['bg'] = LBL_BG_CLEAN


# Allow to change days type
def change_type_days():
    global type_days_only_work
    type_days_only_work = not type_days_only_work
    if type_days_only_work:
        btn_type_days['text'] = 'Рабочие дни'
    else:
        btn_type_days['text'] = 'Календарные дни'


# Protect against incorrect user input
def check_and_calc():
    data_size_str = data_size.get()
    data_size_str = data_size_str.replace(',', '.')
    data_days_str = data_days.get()
    check = True
    try:
        cleaned_data_size = float(data_size_str)
        lbl_size['text'] = 'Размер (данные корректны)'
        ent_size['bg'] = ENTRY_BG_CLEAN
    except:
        check = False
        lbl_size['text'] = 'Введите положительное вещественное значение'
        ent_size['bg'] = ENTRY_BG_ERROR

    try:
        cleaned_data_days = int(data_days_str)
        lbl_days['text'] = 'Количества дней (данные корректны)'
        ent_days['bg'] = ENTRY_BG_CLEAN
    except:
        check = False
        lbl_days['text'] = 'Введите натуральное число'
        ent_days['bg'] = ENTRY_BG_ERROR

    if not os.path.exists(file_name):
        check = False
        lbl_file['bg'] = LBL_BG_ERROR
    else:
        lbl_file['bg'] = LBL_BG_CLEAN

    if not output_file_name:
        check = False
        lbl_outfile['bg'] = LBL_BG_ERROR
    else:
        lbl_outfile['bg'] = LBL_BG_CLEAN

    if check:
        print('данные верны, запускаю расчет')
        mainCalc(cleaned_data_size / 100,
                 cleaned_data_days,
                 type_days_only_work,
                 file_name,
                 output_file_name)  # Call main calculation program
        messagebox.showinfo('', 'Расчет выполнен')
    else:
        print('данные некорректны')


# GUI - graphical user interface
root = Tk()
# root.geometry('800x600')
root.title('Калькулятор задолжности')  # name of the window application.
root.resizable(False, False)
root['bg'] = FRM_BG

data_size = StringVar()
data_days = StringVar()


photoimage = PhotoImage(file='final.png')
img = photoimage
cnv_image = Canvas(root, width=64, height=64, bg='#d9d9d9')
cnv_image.create_image(32, 32, image=img)
cnv_image.grid(row=0, column=0, columnspan=3)

# Image for Button '?'
or_bnt_photo = PhotoImage(file='question.png')
re_bnt_photo = or_bnt_photo.subsample(20, 20)


lbl_file = Label(root, text='Данные для расчета')
lbl_file.grid(row=1, column=0, pady=20, sticky=E, padx=20)
btn_file = Button(root, command=insert_file)
btn_file.grid(row=1, column=1, pady=20, sticky=W, padx=20)

lbl_size = Label(root)
lbl_size.grid(row=2, column=0, pady=20, sticky=E, padx=20)
ent_size = Entry(root, textvariable=data_size)
ent_size.grid(row=2, column=1, pady=20, sticky=W, padx=20)


lbl_days = Label(root)
lbl_days.grid(row=3, column=0, pady=20, sticky=E, padx=20)
ent_days = Entry(root, textvariable=data_days)
ent_days.grid(row=3, column=1, pady=20, sticky=W, padx=20)


lbl_type_days = Label(root, text='Тип дней')
lbl_type_days.grid(row=4, column=0, pady=20, sticky=E, padx=20)
btn_type_days = Button(text='Переключить рабочие/\
календарные дни', command=change_type_days)
btn_type_days.grid(row=4, column=1, sticky=W, padx=20)


lbl_outfile = Label(root, text='Выходные данные')
lbl_outfile.grid(row=5, column=0, pady=20, sticky=E, padx=20)
btn_outfile = Button(root, command=output_file_fun)
btn_outfile.grid(row=5, column=1, pady=20, sticky=W, padx=20)


btn_days = Button(root, text='Выход', command=exit)
btn_days.grid(row=6, column=0)
btn_days = Button(root, text='Рассчитать', command=check_and_calc)
btn_days.grid(row=6, column=1)
btn_days = Button(root, text='Очистить', comman=clean)
btn_days.grid(row=6, column=2)

lbl_size_form1 = Label(root, width=50, bg=FRM_BG)
lbl_size_form1.grid(row=7, column=0)

lbl_size_form2 = Label(root, width=40, bg=FRM_BG)
lbl_size_form2.grid(row=7, column=1)


clean()


# Icons for different platforms
platformD = system()
if platformD == 'Darwin':
    img = Image("photo", file="icon.gif")
    root.call('wm', 'iconphoto', root._w, img)
elif platformD == 'Windows':
    logo_image = 'icon.ico'
    root.iconbitmap(logo_image)
else:
    logo_image = '@icon.xbm'
    root.iconbitmap(logo_image)

# Button '?'
btn_help1 = Button(root)
btn_help1.config(image=re_bnt_photo, height=25, width=25)
btn_help1.grid(row=2, column=3, sticky=W, padx=20)
h1 = HoverInfo(btn_help1, text='Введите целое число/\nчисло\
с разделительной точкой')

btn_help2 = Button(root)
btn_help2.config(image=re_bnt_photo, height=25, width=25)
btn_help2.grid(row=3, column=3, sticky=W, padx=20)
h2 = HoverInfo(btn_help2, text='Введите целое число')

btn_help3 = Button(root)
btn_help3.config(image=re_bnt_photo, height=25, width=25)
btn_help3.grid(row=4, column=3, sticky=W, padx=20)
h3 = HoverInfo(btn_help3, text='Выберите по каким дням\nбудет считаться\
отстрочка')

btn_help4 = Button(root)
btn_help4.config(image=re_bnt_photo, height=25, width=25)
btn_help4.grid(row=5, column=3, sticky=W, padx=20)
h4 = HoverInfo(btn_help4, text='Выберите файл\nдля вывода данных')


root.mainloop()
