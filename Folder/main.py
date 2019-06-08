'''
main.py
главный файл проекта, управление виджетами tk, запуск расчета.

Shirmankina Ekaterina - Final_Main_v8 - 5/6/2019 - 20:08
Versions:
v8.11 - 5/6/2019 - 19:30 : отлажено разбиение на 2 модуля, устранены перекрестные ссылки.
Fixed:
+ bug: после расчета и кнопки Отменить исчезают кнопки Рабочие, Календарные
+ bug: после кнопки Отменить (без расчета) прыгают кнопки '?'
+ todo: Кнопка выхода


- todo: прописать в placeWidget() все позиционирование и сброс для clean()
- todo  Protect against incorrect user input. Прописать решения для всех возможных ошибок пользователя. смотреть функцию - start = Андрей 
- todo All IO or network operations should be written in try-except blocks
- todo после нажатия кнопки  "Рассчитать", а затем кнопки "Отмена" происходит глюк программы - почему?
- todo На Mac при нажатии кнопки "Рассчитать"поле "Поля ввода не заполнены" наезажает на лэйблы, в Wind - все хорошо
- todo первый прогон программы -- "Рассчитать" -- Выводят ошибку-- вводят в поля цифры и программа крашится
- todo - ? Bug or feature? при нажатии clean имя файла не очищается. Сделать, чтобы оба файла очищались.
'''

from tkinter import *
from tkinter import filedialog as fd
# import os
from platform import system
import re
from tkinter.filedialog import askopenfilename
from chardet.universaldetector import UniversalDetector

# Our project files:
from calculation import mainCalc

Working_Days = False
output_file_name = 'out.doc'  # This variable is the name of the output file
file_name = '1.csv'  # This variable is the name of the inputed file

class HoverInfo(Menu):
    '''
    text-подсказка для пользователя. строчки разделены символом  '\n'.
    Пример использования:
    h = HoverInfo(bnt_question_1, text='Введите \n целое \n число')
    '''

    def __init__(self, parent, text, command=None):
        self._com = command
        Menu.__init__(self, parent, tearoff=0)
        if not isinstance(text, str):
            raise TypeError('Trying to initialise a Hover Menu with a non string type: ' + text.__class__.__name__)
        # self.configure(activebackground='SystemMenu', activeborderwidth=10, activeforeground='SystemMenuText')
        toktext = re.split('\n', text)
        for t in toktext:
            self.add_command(label=t)
            self._displayed = False
            self.master.bind("<Enter>", self.Display)
            self.master.bind("<Leave>", self.Remove)

    '''
    def __del__(self):
       self.master.unbind("<Enter>")
       self.master.unbind("<Leave>")
    '''

    def Display(self, event):
        if not self._displayed:
            self._displayed = True
            self.post(event.x_root, event.y_root)
        if self._com != None:
            self.master.unbind_all("<Return>")
            self.master.bind_all("<Return>", self.Click)

    def Remove(self, event):
        if self._displayed:
            self._displayed = False
            self.unpost()
        if self._com != None:
            self.unbind_all("<Return>")

    def Click(self, event):
        self._com()


def insert_file():  # This fuction need to find the name of the file
    global file_name  # This variable is the name of the inputed file
    file_name = fd.askopenfilename()
    button_File.config(text=file_name)


def calendar_days():
    global calendar_d
    calendar_d = True
    bnt_calendar_days.config()
    return (0)


# Метод кнопки выбора выходного файла.
def output_file_fun():  # This function is need to find the name of output file
    global output_file_name  # This variable is the name of the output file
    output_file_name = fd.asksaveasfilename() + '.doc'  # WHY .doc for .txt файл?
    button_Output_File.config(text=output_file_name)
    return 0

def start(percent, time):  # The main function from which all other functions are started
    label_Error.config(text='')  # The label for errors to the user
    label_Percent.place(x=30, y=130)
    label_Error.place_forget()
    label_Time.place(x=30, y=200)
    entry_Percent.config(bg='white', fg='black')
    entry_Time.config(bg='white', fg='black')
    # label_Error.place(x = 30, y = 320)
    # bnt_question_4.place_forget()
    # button_Output_File.place_forget()
    start = True  # The variable to check if the progrma can start or not
    point_in_percent = False  # Checking for point in percent
    Percent = percent  # From the user entered percent to the main progrem
    late_time = time  # From the user entered how many days shoul be waited before the fees started
    if Percent == '' or late_time == '':
        entry_Percent.config(bg='red', fg='white')
        entry_Time.config(bg='red', fg='white')
        label_Time.place_forget()
        label_Percent.place_forget()
        label_Error.config(text='   Поля ввода не    \nзаполнены!', bg='grey', fg='white')
        label_Error.place(x=30, y=170)
        start = False
    for i in range(0, len(Percent)):
        if Percent[i].isdigit() == False and start:
            if Percent[i] != '.' or i == 0 or point_in_percent:
                start = False
                label_Error.config(text=f'{Percent} это не число с    \nразделительной точкой', bg='grey', fg='white')
                label_Error.place(x=30, y=130)
                label_Percent.place_forget()
                entry_Percent.config(bg='red', fg='white')
            if Percent[i] == '.':
                point_in_percent = True

    """
    def code_checking(file_name):
        detector = UniversalDetector()
        with open(file_name, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        det = detector.result
        det1 = det.get('encoding')
        return det1
    det = code_checking('Data2.csv')
    #if det == 'UTF-8-SIG':
    """
    if start:
        for i in range(0, len(late_time)):
            if late_time[i].isdigit() == False:
                start = False
                label_Error.config(text=f'{late_time} это не целое число ', bg='grey', fg='white')
                label_Error.place(x=30, y=200)
                label_Time.place_forget()
                entry_Time.config(bg='red', fg='white')
                break
    if start:
        bnt_question_1.place_forget()
        bnt_question_2.place_forget()
        bnt_question_3.place_forget()
        bnt_question_4.place_forget()
        bnt_working_days.place_forget()
        bnt_calendar_days.place_forget()
        label_Percent.place_forget()
        label_Time.place_forget()
        entry_Percent.place_forget()
        entry_Time.place_forget()
        button_File.place_forget()
        button_Output_File.place_forget()
        lable_choose_file.place_forget()
        lable_place_output.place_forget()
        mainCalc(float(Percent) / 100, int(late_time), Working_Days, file_name, output_file_name)  # Call main calculation program
    return 0


# Center the window with given width and height.
def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def placeWidget():
    entry_Percent.config(bg='white', fg='black')
    entry_Time.config(bg='white', fg='black')
    entry_Percent.place(x=400, y=140)
    entry_Time.place(x=400, y=210)

    bnt_calendar_days.place(x=400, y=280)
    bnt_working_days.place(x=200, y=280)
    button_Exit.place(x=30, y=420)
    button_Main.place(x=280, y=420)
    btn_clean.place(x=530, y=420)


def clean():
    entry_Percent.delete(0, len(entry_Percent.get()))
    entry_Percent.config(bg='white', fg='black')

    entry_Time.config(bg='white', fg='black')
    entry_Time.delete(0, len(entry_Time.get()))

    label_Error.config(text='', bg='lightgrey', fg='lightgrey')
    label_Error.place_forget()

    lable_place_output.config(bg='grey', fg='white')
    placeWidget()


def button_colour_change_gc(event=None):
    # print('button_colour_change')
    bnt_calendar_days['fg'] = "green"
    bnt_calendar_days['activeforeground'] = "green"
    # bnt_calendar_days['selectbackground'] = "red"
    bnt_working_days['fg'] = "red"
    bnt_working_days['activeforeground'] = "red"
    global Working_Days
    Working_Days = False


def button_colour_change_gw(event=None):
    bnt_working_days['fg'] = "green"
    bnt_working_days['activeforeground'] = "green"
    bnt_calendar_days['fg'] = "red"
    bnt_calendar_days['activeforeground'] = "red"
    global Working_Days
    Working_Days = True


root = Tk()

root.title('Калькулятор задолжности')  # name of the window application.
# root.iconbitmap(r'final.png') # НЕ ОТОБРАЖАЕТСЯ
root.resizable(False, False)

center_window(root, 700, 500)  # window size.

canvas = Canvas(root, width=700, height=500, bg='lightgrey')
canvas.pack()

# Icons for different platforms
platformD = system()
if platformD == 'Darwin':
    img = Image("photo", file="icon.gif")  # GIF
    root.call('wm', 'iconphoto', root._w, img)
elif platformD == 'Windows':
    logo_image = 'icon.ico'
    root.iconbitmap(logo_image)
else:
    logo_image = '@icon.xbm'
    root.iconbitmap(logo_image)

# Image for window
original_photo = PhotoImage(file='final.png')
display_photo = original_photo.subsample(9, 9)
canvas.create_image(330, 10, anchor=NW, image=display_photo)

# Lables of the window application
lable_choose_file = Label(root, text='Выберите файл:      ', bg='grey', fg='white',
                          font='Courier 20')  # 20 symbols in a line
lable_choose_file.place(x=30, y=70)
label_Percent = Label(root, text='Введите размер пени:\n ', bg='grey', fg='white', font='Courier 20')
label_Percent.place(x=30, y=130)
label_Time = Label(root, text='Введите количество  \n'
                              'дней на оплату: ', bg='grey', fg='white', font='Courier 20')
label_Time.place(x=30, y=200)
lable_place_output = Label(root, text='Выберите место для  \nсохранения файла:', bg='grey', fg='white',
                           font='Courier 20')
lable_place_output.place(x=30, y=320)

label_Error = Label(root, text='', bg='lightgrey', fg='lightgrey', font='Courier 20')
label_Error.place()
# label_File = Label(root, text='', bg='lightgrey', fg='lightgrey')
# label_File.place(x=50, y=100)

# Text boxes of the window application
entry_Percent = Entry(root, width=11, font=('Ubuntu', 30))
entry_Percent.place(x=400, y=140)
entry_Time = Entry(root, width=11, font=('Ubuntu', 30))
entry_Time.place(x=400, y=210)

# Buttons of the window application
button_Main = Button(root, text='Рассчитать', bg='white', fg='black', font='15')
button_Main.bind('<Button-1>', lambda event: start(entry_Percent.get(), entry_Time.get()))

button_File = Button(root, text='Выбор файла: ', font='Times 11', command=insert_file)
button_File.bind('<Button-2>')
button_File.place(x=400, y=75)

button_Output_File = Button(root, text='Выберите файл:', font='Times 11', command=output_file_fun)
button_Output_File.bind('<Button-3>')
button_Output_File.place(x=400, y=335)

btn_clean = Button(root, text='Отменить', bg='white', fg='black', font='15', command=clean)
btn_clean.bind('<Button-4>')

bnt_calendar_days = Button(text='Календарные дни', command=button_colour_change_gc)
bnt_calendar_days.bind('<Button-5>')
bnt_calendar_days.place(x=400, y=280)

bnt_working_days = Button(root, text='Рабочие дни', bg='grey', fg='black', command=button_colour_change_gw)
bnt_calendar_days.bind('<Button-6>')
bnt_working_days.place(x=200, y=280)

button_Exit = Button(root, text='Выход', bg='white', fg='black', font='15', command=exit)
button_Exit.bind('<Button-7>')

# Image for Button '?'
or_bnt_photo = PhotoImage(file='question.png')
re_bnt_photo = or_bnt_photo.subsample(20, 20)

# Button '?'
bnt_question_1 = Button(root)
bnt_question_1.config(image=re_bnt_photo, height=25, width=25)
bnt_question_1.place(x=660, y=150)
h1 = HoverInfo(bnt_question_1, text='Введите целое число/\nчисло с разделительной точкой')

bnt_question_2 = Button(root)
bnt_question_2.config(image=re_bnt_photo, height=25, width=25)
bnt_question_2.place(x=660, y=215)
h2 = HoverInfo(bnt_question_2, text='Введите целое число')

bnt_question_3 = Button(root)
bnt_question_3.config(image=re_bnt_photo, height=25, width=25)
bnt_question_3.place(x=660, y=275)
h3 = HoverInfo(bnt_question_3, text='Выберите по каким дням\nбудет считаться отстрочка')

bnt_question_4 = Button(root)
bnt_question_4.config(image=re_bnt_photo, height=25, width=25)
bnt_question_4.place(x=660, y=335)

placeWidget() # Позиционировать кнопки
h4 = HoverInfo(bnt_question_4, text='Выберите файл\nдля вывода данных')
root.mainloop()
