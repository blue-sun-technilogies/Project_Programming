from tkinter import *
from tkinter import filedialog as fd
import os 
import codecs
import io
from platform import system
import re
from tkinter.filedialog import askopenfilename

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
        #self.configure(activebackground='SystemMenu', activeborderwidth=10, activeforeground='SystemMenuText')
        toktext=re.split('\n', text)
        for t in toktext:
            self.add_command(label=t)
            self._displayed=False
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
       self._displayed=False
       self.unpost()
     if self._com != None:
       self.unbind_all("<Return>")

    def Click(self, event):
       self._com()


def insert_file():#This fuction need to find the name of the file
    global file_name #This variable is the name of the inputed file
    global button_File
    file_name = fd.askopenfilename()
    button_File.config(file_name)


def working_days():#This function check do we need to work with only working days or no
    global working_d
    working_d = True
    bnt_working_days.config()
    return(0)

def calendar_days():
    global calendar_d
    calendar_d = True
    bnt_calendar_days.config()
    return(0)

def output_file_fun():#This function is need to find the name of output file
    global output_file_name #This variable is the name of the output file
    output_file_name = fd.asksaveasfilename() + '.doc'
    return(0)


def start(percent, time): #The main function from which all other functions are started
    label_Error.config(text='') #The label for errors to the user
    label_Percent.place(x = 30, y = 130)
    label_Error.place_forget()
    label_Time.place(x = 30, y = 200)
    entry_Percent.config(bg = 'white', fg = 'black')
    entry_Time.config(bg = 'white', fg = 'black')
    #label_Error.place(x = 30, y = 320)
    #bnt_question_4.place_forget()
    #button_Output_File.place_forget()
    start = True #The variable to check if the progrma can start or not
    point_in_percent = False #Checking for point in percent
    Percent = percent#From the user entered percent to the main progrem
    late_time = time#From the user entered how many days shoul be waited before the fees started
    if Percent == '' or late_time == '':
        entry_Percent.config(bg = 'red', fg = 'white')
        entry_Time.config(bg = 'red', fg = 'white')
        label_Time.place_forget()
        label_Percent.place_forget()
        label_Error.config(text='   Поля ввода не    \nзаполнены!', bg = 'grey', fg = 'white')
        label_Error.place(x = 30, y = 170)
        start = False
    for i in range(0, len(Percent)):
        if Percent[i].isdigit() == False and start:
            if Percent[i] != '.' or i == 0 or point_in_percent:
                start = False
                label_Error.config(text = f'{Percent} это не число с    \nразделительной точкой', bg = 'grey', fg = 'white')
                label_Error.place(x = 30, y = 130)
                label_Percent.place_forget()
                entry_Percent.config(bg = 'red', fg = 'white')
            if Percent[i] == '.':
                point_in_percent = True

    
    if start:
        for i in range(0, len(late_time)):
            if late_time[i].isdigit() == False:
                start = False
                label_Error.config(text = f'{late_time} это не целое число ', bg = 'grey', fg = 'white')
                label_Error.place(x = 30, y = 200)
                label_Time.place_forget()
                entry_Time.config(bg = 'red', fg = 'white')
                break
    if start:
        bnt_question_1.place_forget()
        bnt_question_2.place_forget()
        bnt_question_3.place_forget()
        bnt_question_4.place_forget()
        main(float(Percent) / 100, int(late_time), file_name)#The beggining ot the program
    return(0)


def main(percent, late_time, file_name):
    def first_data_check(data): #This function check the position of th einformation in the fike
        if data[0][0] == '':
            for i in range(0, len(data) + 1):
                data[i][0] = data[i][6]
                data[i][1] = data[i][7]
                data[i][3] = data[i][9]
                data[i][5] = data[i][11]
        return(data)


    def read_info(file_name): #Add check of all lines
        data = []
        file_name = codecs.open(file_name, 'r', 'utf-8') #We should check the coding sistem
        chec_to_sit_in_end = False #Finding the place of data
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
                            chec_to_sit_in_end =True
        file_name.close()#######
        return data


    def days_work(data):
        return(0)


    def update_outcomes(outcomes): #Special for calculation, this function united information from one day
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
        return(outcomes_updated)

    def incomes_update(incomes):#This function is needed for calculation, again united the information from one day
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
        return(incomes_updated)

    def makeReport(f):
        output_list = []
        begin = f[0][0]
        for i in range(len(f)):
            circle_body = i + 1 <= len(f) - 1
            if circle_body and f[i][1] != f[i + 1][1] or not circle_body:
                output_list.append((f'За {f[i][0] - begin + 1} ' +
                                    (f'дней с {back_date(begin, first_year_date)} по {back_date(f[i][0], first_year_date)} ' if f[i][
                                                                            0] - begin > 0 else f'день {back_date(begin, first_year_date)} числа ') +
                                    f'задолженность составила {(f[i][0] - begin + 1) * f[i][1]}' +
                                    f' штраф {(f[i][0] - begin + 1) * f[i][2]}, пени = {percent}%'))
            if circle_body and f[i][1] != f[i + 1][1]:
                begin = f[i + 1][0]
        return output_list


    def qurent_date(data):#This function is need for calculation it transfer the dates to a numbers, which are used for calculation
        first_year_date = int(data[0][0][6] + data[0][0][7])
        for i in range(0, len(data)):
            current_year = int(data[i][0][6] + data[i][0][7])
            querent_day = int(data[i][0][0]) * 10 + int(data[i][0][1])
            querent_month = int(data[i][0][3]) * 10 + int(data[i][0][4])
            if querent_month == 1:
                querent_month = 0
            elif querent_month == 2:
                querent_month = 31
            elif querent_month == 3 and current_year % 4 != 0:
                querent_month = 59
            elif querent_month == 3 and current_year % 4 == 0:
                querent_month = 60
            elif querent_month == 4 and current_year % 4 != 0:
                querent_month = 90
            elif querent_month == 4 and current_year % 4 == 0:
                querent_month = 91
            elif querent_month == 5 and current_year % 4 != 0:
                querent_month = 120
            elif querent_month == 5 and current_year % 4 == 0:
                querent_month = 121
            elif querent_month == 6 and current_year % 4 != 0:
                querent_month = 151
            elif querent_month == 6 and current_year % 4 == 0:
                querent_month = 152
            elif querent_month == 7 and current_year % 4 != 0:
                querent_month = 181
            elif querent_month == 7 and current_year % 4 == 0:
                querent_month = 182
            elif querent_month == 8 and current_year % 4 != 0:
                querent_month = 212
            elif querent_month == 8 and current_year % 4 == 0:
                querent_month = 213
            elif querent_month == 9 and current_year % 4 != 0:
                querent_month = 243
            elif querent_month == 9 and current_year % 4 == 0:
                querent_month = 244
            elif querent_month == 10 and current_year % 4 != 0:
                querent_month = 273
            elif querent_month == 10 and current_year % 4 == 0:
                querent_month = 274
            elif querent_month == 11 and current_year % 4 != 0:
                querent_month = 304
            elif querent_month == 11 and current_year % 4 == 0:
                querent_month = 305
            elif querent_month == 12 and current_year % 4 != 0:
                querent_month = 334  #This work with no years divided by 4
            elif querent_month == 12 and current_year % 4 == 0:
                querent_month = 335

            date = querent_day + querent_month + ((current_year - first_year_date) * 365)
            data[i][0] = date
        return ([data, first_year_date])

    def back_date(date, first_year_date): # This function convert date in a noramal format.
        day = 0
        month = 0
        year = 0
        while date > 366: ####
            into = False  # This technical variable for.
            if date % 4 == 0:
                year += 1
                date -= 365
                into = True
            elif (into == False):
                year += 1
                date -= 366
        if date == 366 and (year + first_year_date) % 4 != 0:
            date -= 365
            year += 1
        year += first_year_date
        if date <= 31: #January
            month = 1
            day = date
        elif date <= 59 and year % 4 != 0:#February
            month = 2
            day = date - 31
        elif date <= 60 and year % 4 == 0:
            month = 2
            day = date - 31
        elif date <= 90 and year % 4 != 0: #March
            month = 3
            day = date - 59
        elif date <= 91 and year % 4 == 0:
            month = 3
            day = date - 60
        elif date <= 120 and year % 4 != 0: #April
            month = 4
            day = date - 90
        elif date <= 121 and year % 4 == 0:
            month = 4
            day = date - 91
        elif date <= 151 and year % 4 != 0: #May
            month = 5
            day = date - 120
        elif date <= 152 and year % 4 == 0:
            month = 5
            day = date - 121
        elif date <= 181 and year % 4 != 0: #June 
            month = 6
            day = date - 151
        elif date <= 182 and year % 4 == 0:
            month = 6
            day = date - 152
        elif date <= 212 and year % 4 != 0: #Jule 
            month = 7
            day = date - 181
        elif date <= 213 and  year % 4 == 0:
            month = 7
            day = date - 182
        elif date <= 243 and year % 4 != 0: #August
            month = 8
            day = date - 212
        elif date <= 244 and year % 4 == 0:
            month = 8
            day = date - 213
        elif date <= 273 and year % 4 != 0: #September
            month = 9
            day = date - 243
        elif date <= 274 and year % 4 == 0:
            month = 9 
            day = date - 244
        elif date <= 304 and year % 4 != 0: #October:
            month = 10
            day = date - 273
        elif date <= 305 and year % 4 == 0:
            month = 10
            day = date - 274
        elif date <= 334 and year % 4 != 0: #November
            month = 11
            day = date - 304
        elif date <= 335 and year % 4 == 0:
            month = 11
            day = date - 305
        elif date <= 365 and year % 4 != 0: #January
            month = 12
            day = date - 334
        elif date <= 366 and year % 4 == 0:
            month = 12
            day = date - 335
        day = str(day)
        month = str(month)
        year = str(year)
        return(day + '.' + month + '.' + year)


    data = read_info(file_name)#This is the first input of data 
    data = first_data_check(data)
    u_d = qurent_date(data)#Special variable not to call the function two times
    data = u_d[0]
    first_year_date = u_d[1]

    incomes = []
    outcomes = []

    for i in range(0, len(data)):#This part shoul be rewrited, in fact tehre are 4 main and one additional type of words and we should separete them
        if data[i][1][0] == 'П' and data[i][1][3] == 'х':
            data[i][5] = float(data[i][5])
            incomes.append(data[i])
        elif data[i][1][0] == 'О' and data[i][1][2] == 'л':
            data[i][3] = float(data[i][3])
            outcomes.append(data[i])


    outcomes_updated = update_outcomes(outcomes)
    incomes_updated = incomes_update(incomes)



    start_date = data[0][0]#This is the first date for calculation
    last_date = data[len(data) - 1][0]
    fee_to_pay = 0
    current_incomes_number = 0 #The number of incomes with which we are workig
    current_outcomes_number = 0
    not_used_outcomes = 0#This variable is needed to remember all money which was not paied 
    check_to_enter_outcomes = True #Not to go in unnessesary part of the program in the last steps

    fee_fedbak_final = []
    fee_fedbak = 0



    i = start_date
    while i <= last_date:
        check_to_enter = True
        if not_used_outcomes != 0:#Check for the elder outcomes for which user still need to pay
            if incomes_updated[current_incomes_number][5] - not_used_outcomes >= 0: 
                incomes_updated[current_incomes_number][5] -= not_used_outcomes
                not_used_outcomes = 0
            else:
                not_used_outcomes -= incomes_updated[current_incomes_number][5]
                incomes_updated[current_incomes_number][5] = 0
                current_incomes_number += 1


        
        if outcomes_updated[current_outcomes_number][0] == i and check_to_enter_outcomes:#Check if next outcome is going to be today
            if incomes_updated[current_incomes_number][5] - outcomes_updated[current_outcomes_number][3] >= 0:
                incomes_updated[current_incomes_number][5] -= outcomes_updated[current_outcomes_number][3]
                outcomes_updated[current_outcomes_number][3] = 0
                current_outcomes_number += 1 #Switch to next outcomes_updated date
                if incomes_updated[current_incomes_number][5] == 0:
                    current_incomes_number += 1
            else:
                not_used_outcomes = outcomes_updated[current_outcomes_number][3] - incomes_updated[current_incomes_number][5]
                incomes_updated[current_incomes_number][5] = 0
                current_incomes_number += 1
                outcomes_updated[current_outcomes_number][3] = 0
                if current_outcomes_number + 1 < len(outcomes_updated):
                    current_outcomes_number += 1
                else:
                    check_to_enter_outcomes = False
                i -= 1
                check_to_enter = False
        
        if i - incomes_updated[current_incomes_number][0] > late_time and check_to_enter: #Start checkingfor fees
            fee_fedbak = 0
            current_sum_to_pay = incomes_updated[current_incomes_number][5] #Used for output in final
            fee_to_pay += (percent) * (incomes_updated[current_incomes_number][5])
            fee_fedbak = (percent) * (incomes_updated[current_incomes_number][5])
            j = 1
            if incomes_updated[current_incomes_number][0] != last_date and current_incomes_number + j <= (len(incomes_updated) - current_incomes_number):
                while i - incomes_updated[current_incomes_number + j][0] > late_time:
                    fee_to_pay += (percent) * (incomes_updated[current_incomes_number + j][5])
                    current_sum_to_pay += incomes_updated[current_incomes_number + j][5]
                    fee_fedbak += (percent) * (incomes_updated[current_incomes_number + j][5])
                    j += 1
                    if incomes_updated[current_incomes_number][0] == last_date or j == (len(incomes_updated) - current_incomes_number):
                        break
        
        if fee_to_pay != 0:
         #   print(f'Задолженность за {i} день составляет {current_sum_to_pay} рублей, штраф составляет {fee_fedbak} рублей')
            fee_fedbak_final.append([i, current_sum_to_pay, fee_fedbak])
        else:
         #   print(f'Задолженность за {i} день составляет 0 рублей, штраф составляет {fee_fedbak} рублей')
            fee_fedbak_final.append([i, 0, fee_fedbak])
        i += 1

    output_list = makeReport(fee_fedbak_final)

    with io.open(output_file_name, 'w', encoding = ("utf-16")) as fo:#In this function all the information is outputed to the doc format
        for i in range(0, len(output_list)):
            fo.write(output_list[i] + '\n')
    fo.close()


# Center the window with given width and height.
def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def clean():
    entry_Percent.delete(0, len(entry_Percent.get()))
    label_Error.config(text = '', bg = 'lightgrey', fg = 'lightgrey')
    label_Error.place_forget()
    lable_place_output.config(bg = 'grey', fg = 'white')
    bnt_question_1.place(x=650, y=132)
    bnt_question_2.place(x=650, y=202)
    bnt_question_3.place(x=650, y=270)
    bnt_question_4.place(x=650, y=335)
    button_Output_File.place(x=400, y=335)
    entry_Percent.config(bg = 'white', fg = 'black')
    entry_Time.config(bg = 'white', fg = 'black')
    label_Percent.place(x = 30, y = 130)
    label_Time.place(x = 30, y = 200)
    entry_Time.delete(0, len(entry_Time.get()))


def button_colour_change_gc(event=None):
    # print('button_colour_change')
    bnt_calendar_days['fg'] = "green"
    bnt_calendar_days['activeforeground'] = "green"
    # bnt_calendar_days['selectbackground'] = "red"
    bnt_working_days['fg'] = "red"
    bnt_working_days['activeforeground'] = "red"

def button_colour_change_gw(event=None):
    bnt_working_days['fg'] = "green"
    bnt_working_days['activeforeground'] = "green"
    bnt_calendar_days['fg'] = "red"
    bnt_calendar_days['activeforeground'] = "red"
root = Tk()

root.title('Калькулятор задолжности') # name of the window application.
#root.iconbitmap(r'final.png') # НЕ ОТОБРАЖАЕТСЯ
root.resizable(False, False)

center_window(root, 700, 500) # window size.

canvas = Canvas(root, width=700, height=500, bg='lightgrey')
canvas.pack()

#Icons for different platforms
platformD = system()
if platformD == 'Darwin':
    img = Image("photo", file="icon.gif") #GIF
    root.call('wm', 'iconphoto', root._w, img)
elif platformD == 'Windows':
    logo_image = 'icon.ico'
    root.iconbitmap(logo_image)
else:
    logo_image = '@icon.xbm'
    root.iconbitmap(logo_image)

#Image for window
original_photo = PhotoImage(file='final.png')
display_photo = original_photo.subsample(9, 9)
canvas.create_image(330, 10, anchor=NW, image=display_photo)

# Lables of the window application
lable_choose_file = Label(root, text='Выберите файл:      ', bg='grey', fg='white', font='Courier 20')#20 symbols in a line
lable_choose_file.place(x=30, y=70)
label_Percent = Label(root, text = 'Введите размер пени:\n ', bg='grey', fg='white', font='Courier 20')
label_Percent.place(x=30, y=130)
label_Time = Label(root, text='Введите количество  \n'
                                'дней на оплату: ', bg='grey', fg='white', font='Courier 20')
label_Time.place(x=30, y=200)
lable_place_output = Label(root, text='Выберите место для  \nсохранения файла:', bg='grey', fg='white', font='Courier 20')
lable_place_output.place(x=30, y=320)

label_Error = Label(root, text='', bg='lightgrey', fg='lightgrey', font='Courier 20')
label_Error.place()
#label_File = Label(root, text='', bg='lightgrey', fg='lightgrey')
#label_File.place(x=50, y=100)


# Text boxes of the window application
entry_Percent = Entry(root, width = 11, font=('Ubuntu', 30))
entry_Percent.place(x=400, y=140)
entry_Time = Entry(root, width = 11, font = ('Ubuntu', 30))
entry_Time.place(x=400, y=210)


# Buttons of the window application
button_Main = Button(root, text='Рассчитать', bg='white', fg='black', font='15')
button_Main.bind('<Button-1>', lambda event: start(entry_Percent.get(), entry_Time.get()))
button_Main.place(x=270, y=420)


button_File = Button(root, text='Выбор файла: ', font = 'Times 11', command=insert_file)
button_File.bind('<Button-2>')
button_File.place(x=400, y=75)

button_Output_File = Button(root, text='Выберите файл:', font = 'Times 11', command=output_file_fun)
button_Output_File.bind('<Button-3>')
button_Output_File.place(x=400, y=335)

btn_clean = Button(root, text='Отменить', bg='white', fg='black', font='15', command=clean)
btn_clean.bind('<Button-4>')
btn_clean.place(x=530, y=420)


bnt_calendar_days = Button(text='Календарные дни', command=button_colour_change_gc)
bnt_calendar_days.place(x=400, y=280)
# bnt_calendar_days.bind('<Button-5>', button_colour_change) # bind event: Press this button
# bnt_calendar_days.bind('<Return>', button_colour_change)   # bind event: press Enter (when focus)
#bnt_calendar_days.pack() # pack() нельзя вызывать, если выполняется позиционирование place(x, y)

bnt_working_days = Button(root, text='Рабочие дни', bg='grey', fg='black', command=button_colour_change_gw)
#bnt_working_days.bind('<Button-6>', button_colour_change)
#bnt_working_days.bind('<Return>', button_colour_change)
bnt_working_days.place(x=200, y=280)

#Image for Button(?)
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
