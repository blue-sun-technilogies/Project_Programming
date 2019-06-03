from tkinter import *
from tkinter import filedialog as fd
import os
import codecs
import io
from platform import system
import re
from tkinter.filedialog import askopenfilename
import requests
from chardet.universaldetector import UniversalDetector


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
    global button_File
    file_name = fd.askopenfilename()
    button_File.config(text=file_name)



#calend = calendar(2019)
#print(calend)



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
        main(float(Percent) / 100, int(late_time), file_name)  # The beggining ot the program
    return (0)


def main(percent, late_time, file_name):
    def first_data_check(data):  # This function check the position of th einformation in the fike
        if data[0][0] == '':
            for i in range(0, len(data) + 1):
                data[i][0] = data[i][6]
                data[i][1] = data[i][7]
                data[i][3] = data[i][9]
                data[i][5] = data[i][11]
        return (data)
    

    url = 'https://isdayoff.ru/api/getdata?year=' #Исплользуем API для выходных дней
    def calendar(calendar_year):
        calend = []
        calendar_year = str(calendar_year)
        path = url + calendar_year
        r = requests.get(path)
        data = r.content
        for elements in data:
            if elements == 49:
                calend.append(1)
            elif elements == 48:
                calend.append(0)
            else:
                calend.append(2)
        return calend

    def read_info(file_name):  # Add check of all lines
        data = []
        file_name = codecs.open(file_name, 'r', 'utf-8')  # We should check the coding sistem
        chec_to_sit_in_end = False  # Finding the place of data
        for line in file_name:
            if (line[0].isdigit() and line[1].isdigit() and line[2] == '.') or chec_to_sit_in_end:
                part = line.split(',')
                row = [
                    part[0], part[1], part[2], part[3],
                    part[4], part[5], part[6], part[7],
                    part[8], part[9], part[10],
                    part[11], part[12], part[12],
                    part[13]
                ]
                data.append(row)
            elif (chec_to_sit_in_end == False):
                part = line.split(',')
                if part[0] == '' and len(part) > 6:
                    if len(part[6]) >= 3:
                        if part[6][0].isdigit() and part[6][1].isdigit and part[6][2] == '.':
                            row = [
                                part[0], part[1], part[2], part[3],
                                part[4], part[5], part[6], part[7],
                                part[8], part[9], part[10],
                                part[11], part[12], part[12],
                                part[13]
                            ]
                            data.append(row)
                            chec_to_sit_in_end = True
        file_name.close()  #######
        return data


    global Working_Days
    Working_Days = True 
    def update_outcomes(outcomes):  # Special for calculation, this function united information from one day
        outcomes_updated = []
        i = 0
        while i < len(outcomes):
            outcomes_updated.append(outcomes[i])
            if i + 1 < len(outcomes):
                while outcomes[i + 1][0] == outcomes[i][0]:
                    outcomes_updated[len(outcomes_updated) - 1][3] += float(outcomes[i + 1][3])
                    i += 1
                    if i + 1 == len(outcomes):
                        break
            i += 1
        return (outcomes_updated)

    def incomes_update(incomes):  # This function is needed for calculation, again united the information from one day
        incomes_updated = []
        i = 0
        while i < len(incomes):
            incomes_updated.append(incomes[i])
            if i + 1 < len(incomes):
                while incomes[i + 1][0] == incomes_updated[len(incomes_updated) - 1][0]:
                    incomes_updated[len(incomes_updated) - 1][5] += float(incomes[i + 1][5])
                    i += 1
                    if i + 1 == len(incomes):
                        break
            i += 1
        return (incomes_updated)

    def makeReport(f):
        output_list = []
        begin = f[0][0]
        for i in range(len(f)):
            circle_body = i + 1 <= len(f) - 1
            if circle_body and f[i][1] != f[i + 1][1] or not circle_body:
                output_list.append((f'Количество дней - {f[i][0] - begin + 1} ' +
                (f'дней с {dayToStr(begin, firstYear)} по {dayToStr(f[i][0], firstYear)} '
                 if f[i][0] - begin > 0 else f'день {dayToStr(begin, firstYear)} числа ') +
                                    f'задолженность составила {(f[i][0] - begin + 1) * f[i][1]}' +
                                    f' штраф {(f[i][0] - begin + 1) * f[i][2]}, пени = {percent}%, формула растчета: сумма штрафа = {(f[i][0] - begin + 1) * f[i][1]}/100*{percent}\n'))
            if circle_body and f[i][1] != f[i + 1][1]:
                begin = f[i + 1][0]
        return output_list


    '''
    # Прототип функции по нахождению расстояния между датами в днях. Аргумент - ? , возвращаемое значение - ?

    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)

    '''

    ''' List for date convert
    '''
    days_in_months = [
    0,
    31,
    28,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31
    ]

    # Определяет високосный ли год для двухначного числа (int), 18 for 2018.
    def is_intercalary_year(year):
        year-=2000  # for yy only
        return (year % 4 == 0 and year % 100 != 0 or year % 400 == 0) # Високосный год для грегорианского календаря.
        
    ''' Преобразует day, month, year и firstYear (все int) в номер дня, считая с января firstYear (18 значит 2018).
    1 января года указанного в файле это цифра 1, второе января это 2 итд.
    '''
    def dayToInt(day, month, year, firstYear):
        # print("DEBUG dayToInt("+str(day)+', '+str(month)+', '+str(year)+', '+str(firstYear)+') ', end='')
        # Дни за все прошедшие годы и месяцы отчетного период прибавляем к current_day.  
        for _year in range(firstYear, year): # за годы: с firstYear до current_year исключая последний.
            day += 366 if is_intercalary_year(_year) else 365
        for _month in range(1, month):
            day += days_in_months[_month]
        if month>2 and is_intercalary_year(year):
            day += 1 # Febr intercalary current year.
        # print('returns '+str(day))
        return day

    '''
    Функция преобразует в массиве data дату (data[i][0]) из строки в целое число, возвращает кортеж (data, номер_первого_года).
    This function is need for calculation. It transfer the dates to a numbers, which are used for calculation.
    data - list[][][] from data.csv; return - tuple( modified data[][][], firstYear - год как int, 18 для 2018)
    Берём первый элемент из data (это data[i][0]), это дата формата дд.мм.гг, д.м.гг, или дд.м.гг. 
    (firstYear = int(data[0][0][6] + data[0][0][7]) - это номер года, 18 для 2018).
    Надо запомнить какой год был указан в этой дате и пронумеровать дальше все даты следующим образом:
    1 января года указанного в файле это цифра 1, второе января это 2 итд.
    '''
    def dataDatesConvertToInt(data):
        firstYear = int(data[0][0][6:8]) # 18 for 2018
        for i in range(0, len(data)):
            lst=data[i][0].split(',')[0].split('.') # Отделим по ',' дату, затем разделим дату по '.' на список строк. 
            data[i][0] = dayToInt( int(lst[0]), int(lst[1]), int(lst[2]), firstYear)
        return (data, firstYear) # Tuple - (Total number of days, include current_day; год как int, 18 для 2018).

    
    ''' Converts date (int) and firstYear (int) to return str: dd.mm.yy.
    Первым днем (1) считается 1 января указанного года firstYear (18 из 2018).
    '''
    def dayToStr(date, firstYear):
        # print("DEBUG dayToStr(date="+str(date), end='')
        day, month, year = date, 1, firstYear
        yearLength = 365+int(is_intercalary_year(year)) # продолжительность года year с учетом его високосности (365 или 366)
        while date >= yearLength: # цикл исчерпывания полных годов из day
            date -= yearLength
            if date==0: # Если все дни исчерпаны текущим годом, то..
                day, month = 31, 12 # ... то это 31.12 - последний день года.
            else:    
                year += 1
                yearLength = int(is_intercalary_year(year)) # продолжительность года year с учетом его високосности (365 или 366)
        while date >= days_in_months[month]: # цикл исчерпывания полных месяцев из day
            date -= days_in_months[month]
            if date==0:                     # Если все дни исчерпаны текущим месяцем, то...
                day = days_in_months[month] # ... то это последний день месяца.
            else:                           # Если нет...
                month += 1                  # ... то переходим на следующий месяц.
                day = date        
        # print(", firstYear="+str(firstYear)+") returns " + str(day//10) + str(day%10) + '.' + str(month//10) + str(month%10) + '.' + str(year) )        
        return str(day//10) + str(day%10) + '.' + str(month//10) + str(month%10) + '.' + str(year)


    data = read_info(file_name) # This is the first input of data 
    data = first_data_check(data)
    u_d = dataDatesConvertToInt(data) # Special variable not to call the function two times
    data = u_d[0] # Return tuple, NEW data[][][] with dates converted to int, AND firstYear, 18 for 2018.
    firstYear = u_d[1]
    calend = calendar(firstYear)

    incomes = []
    outcomes = []

    for i in range(0, len(
            data)):  # This part shoul be rewrited, in fact tehre are 4 main and one additional type of words and we should separete them
        if data[i][1][0] == 'П' and data[i][1][3] == 'х':
            data[i][5] = float(data[i][5])
            incomes.append(data[i])
        elif data[i][1][0] == 'О' and data[i][1][2] == 'л':
            data[i][3] = float(data[i][3])
            outcomes.append(data[i])

    outcomes_updated = update_outcomes(outcomes)
    incomes_updated = incomes_update(incomes)

    start_date = data[0][0]  # This is the first date for calculation
    last_date = data[len(data) - 1][0]
    fee_to_pay = 0
    current_incomes_number = 0  # The number of incomes with which we are workig
    current_outcomes_number = 0
    not_used_outcomes = 0  # This variable is needed to remember all money which was not paied
    check_to_enter_outcomes = True  # Not to go in unnessesary part of the program in the last steps

    fee_fedbak_final = []
    fee_fedbak = 0

    i = start_date
    while i <= last_date:
        check_to_enter = True
        if not_used_outcomes != 0:  # Check for the elder outcomes for which user still need to pay
            if incomes_updated[current_incomes_number][5] - not_used_outcomes >= 0:
                incomes_updated[current_incomes_number][5] -= not_used_outcomes
                not_used_outcomes = 0
            else:
                not_used_outcomes -= incomes_updated[current_incomes_number][5]
                incomes_updated[current_incomes_number][5] = 0
                current_incomes_number += 1

        if outcomes_updated[current_outcomes_number][
            0] == i and check_to_enter_outcomes:  # Check if next outcome is going to be today
            if incomes_updated[current_incomes_number][5] - outcomes_updated[current_outcomes_number][3] >= 0:
                incomes_updated[current_incomes_number][5] -= outcomes_updated[current_outcomes_number][3]
                outcomes_updated[current_outcomes_number][3] = 0
                current_outcomes_number += 1  # Switch to next outcomes_updated date
                if incomes_updated[current_incomes_number][5] == 0:
                    current_incomes_number += 1
            else:
                not_used_outcomes = outcomes_updated[current_outcomes_number][3] - \
                                    incomes_updated[current_incomes_number][5]
                incomes_updated[current_incomes_number][5] = 0
                current_incomes_number += 1
                outcomes_updated[current_outcomes_number][3] = 0
                if current_outcomes_number + 1 < len(outcomes_updated):
                    current_outcomes_number += 1
                else:
                    check_to_enter_outcomes = False
                i -= 1
                check_to_enter = False

        if Working_Days:
            if i - incomes_updated[current_incomes_number][0] > late_time and check_to_enter:
                quantity_working = 0
                for k in range(incomes_updated[current_incomes_number][0] - 1, i):
                    if calend[k] == 0:
                        quantity_working += 1
                if quantity_working > late_time:
                    fee_fedbak = 0
                    current_sum_to_pay = incomes_updated[current_incomes_number][5]
                    if calend[current_incomes_number - 1] == 0:
                        fee_to_pay += (percent) * (incomes_updated[current_incomes_number][5])
                        fee_fedbak = (percent) * (incomes_updated[current_incomes_number][5])
                        j = 1
                        if incomes_updated[current_incomes_number][0] != last_date and current_incomes_number + j <= (
                            len(incomes_updated) - current_incomes_number):
                            while i - incomes_updated[current_incomes_number + j][0] > late_time:
                                if calend[current_incomes_number - 1] == 0:
                                    fee_to_pay += (percent) * (incomes_updated[current_incomes_number + j][5])
                                    current_sum_to_pay += incomes_updated[current_incomes_number + j][5]
                                    fee_fedbak += (percent) * (incomes_updated[current_incomes_number + j][5])
                                    j += 1
                                if incomes_updated[current_incomes_number][0] == last_date or j == (
                                        len(incomes_updated) - current_incomes_number):
                                    break



        elif i - incomes_updated[current_incomes_number][0] > late_time and check_to_enter:  # Start checkingfor fees
            fee_fedbak = 0
            current_sum_to_pay = incomes_updated[current_incomes_number][5]  # Used for output in final
            fee_to_pay += (percent) * (incomes_updated[current_incomes_number][5])
            fee_fedbak = (percent) * (incomes_updated[current_incomes_number][5])
            j = 1
            if incomes_updated[current_incomes_number][0] != last_date and current_incomes_number + j <= (
                    len(incomes_updated) - current_incomes_number):
                while i - incomes_updated[current_incomes_number + j][0] > late_time:
                    fee_to_pay += (percent) * (incomes_updated[current_incomes_number + j][5])
                    current_sum_to_pay += incomes_updated[current_incomes_number + j][5]
                    fee_fedbak += (percent) * (incomes_updated[current_incomes_number + j][5])
                    j += 1
                    if incomes_updated[current_incomes_number][0] == last_date or j == (
                            len(incomes_updated) - current_incomes_number):
                        break

        if fee_to_pay != 0:
            #   print(f'Задолженность за {i} день составляет {current_sum_to_pay} рублей, штраф составляет {fee_fedbak} рублей')
            fee_fedbak_final.append([i, current_sum_to_pay, fee_fedbak])
        else:
            #   print(f'Задолженность за {i} день составляет 0 рублей, штраф составляет {fee_fedbak} рублей')
            fee_fedbak_final.append([i, 0, fee_fedbak])
        i += 1

    output_list = makeReport(fee_fedbak_final)

    with io.open(output_file_name, 'w',
                 encoding=("utf-16")) as fo:  # In this function all the information is outputed to the doc format
        for i in range(0, len(output_list)):
            fo.write(output_list[i] + '\n')
    fo.close()


# Center the window with given width and height.
def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def clean():
    entry_Percent.delete(0, len(entry_Percent.get()))
    label_Error.config(text='', bg='lightgrey', fg='lightgrey')
    label_Error.place_forget()
    lable_place_output.config(bg='grey', fg='white')
    bnt_question_1.place(x=650, y=132)
    bnt_question_2.place(x=650, y=202)
    bnt_question_3.place(x=650, y=270)
    bnt_question_4.place(x=650, y=335)
    button_Output_File.place(x=400, y=335)
    entry_Percent.config(bg='white', fg='black')
    entry_Time.config(bg='white', fg='black')
    label_Percent.place(x=30, y=130)
    label_Time.place(x=30, y=200)
    entry_Time.delete(0, len(entry_Time.get()))


def button_colour_change_gc(event=None):
    # print('button_colour_change')
    bnt_calendar_days['fg'] = "green"
    bnt_calendar_days['activeforeground'] = "green"
    # bnt_calendar_days['selectbackground'] = "red"
    bnt_working_days['fg'] = "red"
    bnt_working_days['activeforeground'] = "red"
    Working_Days = True


def button_colour_change_gw(event=None):
    bnt_working_days['fg'] = "green"
    bnt_working_days['activeforeground'] = "green"
    bnt_calendar_days['fg'] = "red"
    bnt_calendar_days['activeforeground'] = "red"
    Working_Days = False


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
button_Main.place(x=270, y=420)

button_File = Button(root, text='Выбор файла: ', font='Times 11', command=insert_file)
button_File.bind('<Button-2>')
button_File.place(x=400, y=75)

button_Output_File = Button(root, text='Выберите файл:', font='Times 11', command=output_file_fun)
button_Output_File.bind('<Button-3>')
button_Output_File.place(x=400, y=335)

btn_clean = Button(root, text='Отменить', bg='white', fg='black', font='15', command=clean)
btn_clean.bind('<Button-4>')
btn_clean.place(x=530, y=420)

bnt_calendar_days = Button(text='Календарные дни', command=button_colour_change_gc)
bnt_calendar_days.place(x=400, y=280)
# bnt_calendar_days.bind('<Button-5>', button_colour_change) # bind event: Press this button
# bnt_calendar_days.bind('<Return>', button_colour_change)   # bind event: press Enter (when focus)
# bnt_calendar_days.pack() # pack() нельзя вызывать, если выполняется позиционирование place(x, y)

bnt_working_days = Button(root, text='Рабочие дни', bg='grey', fg='black', command=button_colour_change_gw)
# bnt_working_days.bind('<Button-6>', button_colour_change)
# bnt_working_days.bind('<Return>', button_colour_change)
bnt_working_days.place(x=200, y=280)

# Image for Button(?)
or_bnt_photo = PhotoImage(file='question.png')
re_bnt_photo = or_bnt_photo.subsample(20, 20)

# Button(?)
bnt_question_1 = Button(root)
bnt_question_1.config(image=re_bnt_photo, height=25, width=25)
bnt_question_1.place(x=660, y=152)
h1 = HoverInfo(bnt_question_1, text='Введите целое число/\nчисло с разделительной точкой')

bnt_question_2 = Button(root)
bnt_question_2.config(image=re_bnt_photo, height=25, width=25)
bnt_question_2.place(x=660, y=222)
h2 = HoverInfo(bnt_question_2, text='Введите целое число')

bnt_question_3 = Button(root)
bnt_question_3.config(image=re_bnt_photo, height=25, width=25)
bnt_question_3.place(x=660, y=290)
h3 = HoverInfo(bnt_question_3, text='Выберите по каким дням\nбудет считаться отстрочка')

bnt_question_4 = Button(root)
bnt_question_4.config(image=re_bnt_photo, height=25, width=25)
bnt_question_4.place(x=660, y=355)
h4 = HoverInfo(bnt_question_4, text='Выберите файл\nдля вывода данных')

root.mainloop()
