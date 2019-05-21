from tkinter import *
from tkinter import filedialog as fd
import os 
import codecs
import io


def insert_file():
    global file_name
    file_name = fd.askopenfilename()
    label_File.config(text = file_name)
    return(file_name)


def working_days():#This function check do we need to work with only working days or no
    global working_d
    working_d = True
    button_Workinf_days.config(bg = 'green')
    return(0)


def output_file_fun():
    global output_file_name
    output_file_name = fd.asksaveasfilename() + '.doc'
    #print(output_file_name)


def start(percent, time):
    label_Error.config(text = '')
    start = True
    point_in_percent = False #Checking for point in percent
    Percent = percent
    late_time = time
    if Percent == '' or late_time == '':
        label_Error.config(text = 'Поля ввода не заполнены')
        start = False
    for i in range(0, len(Percent)):
        if Percent[i].isdigit() == False and start:
            if Percent[i] != '.' or i == 0 or point_in_percent:
                start = False
                label_Error.config(text = f'{Percent} это не число с разделительной точкой')
            if Percent[i] == '.':
                point_in_percent = True

    
    if start:
        for i in range(0, len(late_time)):
            if late_time[i].isdigit() == False:
                start = False
                label_Error.config(text = f'{late_time} это не целое число')
                break
    if start:
        main(float(Percent) / 100, int(late_time), file_name)
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


    def update_outcomes(outcomes): #Special for calculation
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


    def incomes_update(incomes):
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



    def qurent_date(data):
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

    def back_date(date, first_year_date): #This function convert date in a noramal format 
        day = 0
        month = 0
        year = 0
        while date > 366: ####
            into = False #This technical variable for 
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


    data = read_info(file_name)
    data = first_data_check(data)
    u_d = qurent_date(data)#Special variable not to call the function two times
    data = u_d[0]
    first_year_date = u_d[1]

    incomes = []
    outcomes = []

    for i in range(0, len(data)):
        if data[i][1][0] == 'П' and data[i][1][3] == 'х':
            data[i][5] = float(data[i][5])
            incomes.append(data[i])
        elif data[i][1][0] == 'О' and data[i][1][2] == 'л':
            data[i][3] = float(data[i][3])
            outcomes.append(data[i])


    outcomes_updated = update_outcomes(outcomes)
    incomes_updated = incomes_update(incomes)



    start_date = data[0][0]
    last_date = data[len(data) - 1][0]
    fee_to_pay = 0
    #fee_to_pay_previous = fee_to_pay #For output
    #current_outcomes_date = outcomes_updated[0][0]
    #current_incomes_date = incomes_updated[0][0]
    current_incomes_number = 0 #The number of incomes with which we are workig
    current_outcomes_number = 0
    not_used_outcomes = 0
    check_to_enter_outcomes = True #Not to go in unnessesary part of the program in the last steps

    fee_fedbak_final = []
    fee_fedbak = 0



    i = start_date
    while i <= last_date:
        check_to_enter = True
        if not_used_outcomes != 0:
            if incomes_updated[current_incomes_number][5] - not_used_outcomes >= 0: 
                incomes_updated[current_incomes_number][5] -= not_used_outcomes
                not_used_outcomes = 0
            else:
                not_used_outcomes -= incomes_updated[current_incomes_number][5]
                incomes_updated[current_incomes_number][5] = 0
                current_incomes_number += 1


        
        if outcomes_updated[current_outcomes_number][0] == i and check_to_enter_outcomes:
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
        
        if i - incomes_updated[current_incomes_number][0] > late_time and check_to_enter:
            fee_fedbak = 0
            current_sum_to_pay = incomes_updated[current_incomes_number][5] #Used for output in final
            fee_to_pay += (percent) * (incomes_updated[current_incomes_number][5])
            fee_fedbak = (percent) * (incomes_updated[current_incomes_number][5])
            j = 1
            #print(fee_to_pay)
            if incomes_updated[current_incomes_number][0] != last_date and current_incomes_number + j <= (len(incomes_updated) - current_incomes_number):
                while i - incomes_updated[current_incomes_number + j][0] > late_time:
                    fee_to_pay += (percent) * (incomes_updated[current_incomes_number + j][5])
                    current_sum_to_pay += incomes_updated[current_incomes_number + j][5]
                    fee_fedbak += (percent) * (incomes_updated[current_incomes_number + j][5])
                    j += 1
                    #print(fee_to_pay)
                    if incomes_updated[current_incomes_number][0] == last_date or j == (len(incomes_updated) - current_incomes_number):
                        break
        
        if fee_to_pay != 0:
         #   print(f'Задолженность за {i} день составляет {current_sum_to_pay} рублей, штраф составляет {fee_fedbak} рублей')
            fee_fedbak_final.append([i, current_sum_to_pay, fee_fedbak])
        else:
         #   print(f'Задолженность за {i} день составляет 0 рублей, штраф составляет {fee_fedbak} рублей')
            fee_fedbak_final.append([i, 0, fee_fedbak])
        i += 1

    output_list = []
    fff_start = fee_fedbak_final[0][0] #This is the first day from which we start calculation 
    for i in range(0, len(fee_fedbak_final)):
        if i + 1 <= len(fee_fedbak_final) - 1:
            if fee_fedbak_final[i][1] != fee_fedbak_final[i + 1][1]:
                output_list.append(f'За {fee_fedbak_final[i][0] - fff_start + 1} дней с {back_date(fff_start, first_year_date)} по {back_date(fee_fedbak_final[i][0], first_year_date)} задолженность составила {(fee_fedbak_final[i][0] - fff_start + 1) * fee_fedbak_final[i][1]} штраф {(fee_fedbak_final[i][0] - fff_start + 1) * fee_fedbak_final[i][2]}')
                fff_start = fee_fedbak_final[i + 1][0]
        else:
            output_list.append(f'За {fee_fedbak_final[i][0] - fff_start + 1} дней с {back_date(fff_start, first_year_date)} по {back_date(fee_fedbak_final[i][0], first_year_date)} задолженность составила {(fee_fedbak_final[i][0] - fff_start + 1) * fee_fedbak_final[i][1]} штраф {(fee_fedbak_final[i][0] - fff_start + 1) * fee_fedbak_final[i][2]}')

    with io.open(output_file_name, 'w', encoding = ("utf-16")) as fo:
        for i in range(0, len(output_list)):
            fo.write(output_list[i] + '\n')
    fo.close()
    





root = Tk()
root.title('Расчет')
root.geometry('512x360')

canvas = Canvas(root, width = 500, height = 350, bg = '#002')

canvas.pack(side = 'right')


canvas.create_text(500, 350, text = 'Percent', fill = 'white')


label_Percent = Label(root, text = 'Штрафной процент (число с разделительной точкой)')
label_Percent.place(x = 50, y = 50)
label_Time = Label(root, text = 'Количество дней на оплату (целое число)')
label_Time.place(x = 50, y = 75)
label_Error = Label(root, text = '')
label_Error.place(x = 230, y = 250)
label_File = Label(root, text = '                        ')
label_File.place(x = 50, y = 100)


entry_Percent = Entry(root)
entry_Percent.place(x = 360, y = 51)
entry_Time = Entry(root)
entry_Time.place(x = 300, y = 76)


button_Main = Button(root, text = 'Press')
button_Main.bind('<Button-1>', lambda event: start(entry_Percent.get(), entry_Time.get()))
button_Main.place(x = 240, y = 300)

button_File = Button(root, text = 'Выбор файла', command = insert_file)
button_File.place(x = 240, y = 100)

button_Output_File = Button(root, text = 'Вывод ответа', command = output_file_fun)
button_Output_File.place(x = 240, y = 150)

button_Workinf_days = Button(root, text = 'Учитывать рабочие дни', command = working_days)
button_Workinf_days.place(x = 240, y = 200)

root.mainloop()
