global some_error
some_error = False
global type_of_error 
type_of_error = ''
global to_user_error
to_user_error = ''

def first_data_check(data):  # This function check the position of the information in the file
    if data[0][0] == '':
        try:
            for i in range(0, len(data) + 1):
                data[i][0] = data[i][6]
                data[i][1] = data[i][7]
                data[i][3] = data[i][9]
                data[i][5] = data[i][11]
        except:
            global some_error
            some_error = True
            global type_of_error
            type_of_error += 'The problem in file, the finding of the info position'
    return (data)


def makeCalendarList(firstYear=0):
    import requests                                # Requre: pip3 install requests
    url = 'https://isdayoff.ru/api/getdata?year='  # Используем API для выходных дней
    r = requests.get(url + str(firstYear + 2000))
    # print(*r.content, type(r.content)) # ... 48 49 49 <class 'bytes'>
    return [1 if elem == 49 else 0 for elem in r.content]


# Функция ввода данных (file IO, try - except).
def read_info(file_name):  # Add check of all lines
    data = []
    file_name = open(file_name, 'r', encoding='utf-8')  # Python3 need not codecs modul for encoding.
    chec_to_sit_in_end = False  # Finding the place of data
    for line in file_name:
        try:
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
        except:
            global some_error
            global type_of_error
            some_error = True
            type_of_error += ' The problem with the accuracy of data in some line (read_info function)'
    file_name.close()  #######
    return data


# Функция вывода данных (IO, try - except).
def write_info(report, output_file_name):
    fo=open(output_file_name, 'w', encoding='utf-16') # Information is outputed to the doc format
    for elem in report[0]:
        fo.write(elem + '\n')
    fo.write(f'Общая сумма штрафа составила {report[1]} рублей')
    fo.close()


def update_outcomes(outcomes):  # Special for calculation, this function united information from one day
    outcomes_updated = []
    i = 0
    try:
        while i < len(outcomes): 
            outcomes_updated.append(outcomes[i])
            if i + 1 < len(outcomes):
                while outcomes[i + 1][0] == outcomes[i][0]:
                    outcomes_updated[len(outcomes_updated) - 1][3] += float(outcomes[i + 1][3])
                    i += 1
                    if i + 1 == len(outcomes):
                        break
            i += 1
    except:
        global some_error
        global type_of_error
        some_error = True
        type_of_error += ' Some error in update outcomes function'
    return (outcomes_updated)

def incomes_update(incomes):  # This function is needed for calculation, again united the information from one day
    incomes_updated = []
    i = 0
    try:
        while i < len(incomes):
            incomes_updated.append(incomes[i])
            if i + 1 < len(incomes):
                while incomes[i + 1][0] == incomes_updated[len(incomes_updated) - 1][0]:
                    incomes_updated[len(incomes_updated) - 1][5] += float(incomes[i + 1][5])
                    i += 1
                    if i + 1 == len(incomes):
                        break
            i += 1
    except:
        global some_error
        global type_of_error
        some_error = True
        type_of_error += ' Some problem in incomes updated function'
    return (incomes_updated)

def makeReport(f, percent, firstYear):
    output_list = []
    final_to_pay = 0
    begin = f[0][0]
    for i in range(len(f)):
        circle_body = i + 1 <= len(f) - 1
        if circle_body and f[i][1] != f[i + 1][1] or not circle_body:
            output_list.append((f'Количество дней - {f[i][0] - begin + 1} ' +
                                (f'дней с {dayToStr(begin, firstYear)} по {dayToStr(f[i][0], firstYear)} '
                                 if f[i][0] - begin > 0 else f'день {dayToStr(begin, firstYear)} числа ') +
                                f'задолженность составила {round((f[i][0] - begin + 1) * f[i][1], 2)}' +
                    f' штраф {round((f[i][0] - begin + 1) * f[i][2], 2)}, пени = {percent}%, формула расчета: сумма штрафа = {(f[i][0] - begin + 1) *f[i][1]}/100*{percent}\n'))
            final_to_pay += (f[i][0] - begin + 1) * f[i][2]         
        if circle_body and f[i][1] != f[i + 1][1]:
            begin = f[i + 1][0]
    return [output_list, final_to_pay]


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
    year -= 2000  # for yy only
    return (year % 4 == 0 and year % 100 != 0 or year % 400 == 0)  # Високосный год для грегорианского календаря.



def dayToInt(day, month, year, firstYear):
    # print("DEBUG dayToInt("+str(day)+', '+str(month)+', '+str(year)+', '+str(firstYear)+') ', end='')
    # Дни за все прошедшие годы и месяцы отчетного период прибавляем к current_day.
    for _year in range(firstYear, year):  # за годы: с firstYear до current_year исключая последний.
        day += 366 if is_intercalary_year(_year) else 365
    for _month in range(1, month):
        day += days_in_months[_month]
    if month > 2 and is_intercalary_year(year):
        day += 1  # Febr intercalary current year.
    # print('returns '+str(day))
    return day


def dataDatesConvertToInt(data):
    firstYear = int(data[0][0][6:8])  # 18 for 2018
    try:
        for i in range(0, len(data)):
            lst = data[i][0].split(',')[0].split(
                '.')  # Отделим по ',' дату, затем разделим дату по '.' на список строк.
            data[i][0] = dayToInt(int(lst[0]), int(lst[1]), int(lst[2]), firstYear)
    except:
        global some_error
        global type_of_error
        global to_user_error
        some_error = True
        type_of_error += 'Problem in the function dataDatesConvertToInt'
        to_user_error += 'Проверьте корректность дат в файле, убедитесь, что даты разделены точкой, а не запятой, в случае если все верно, свяжитесь с нами и опишите проблему'
    return (data, firstYear)  # Tuple - (Total number of days, include current_day; год как int, 18 для 2018).


def dayToStr(date, firstYear):
    # print("DEBUG dayToStr(date="+str(date), end='')
    day, month, year = date, 1, firstYear
    yearLength = 365 + int(
        is_intercalary_year(year))  # продолжительность года year с учетом его високосности (365 или 366)
    while date >= yearLength:  # цикл исчерпывания полных годов из day
        date -= yearLength
        if date == 0:  # Если все дни исчерпаны текущим годом, то..
            day, month = 31, 12  # ... то это 31.12 - последний день года.
        else:
            year += 1
            yearLength = int(
                is_intercalary_year(year))  # продолжительность года year с учетом его високосности (365 или 366)
    while date >= days_in_months[month]:  # цикл исчерпывания полных месяцев из day
        date -= days_in_months[month]
        if date == 0:  # Если все дни исчерпаны текущим месяцем, то...
            day = days_in_months[month]  # ... то это последний день месяца.
        else:  # Если нет...
            month += 1  # ... то переходим на следующий месяц.
            day = date
            # print(", firstYear="+str(firstYear)+") returns " + str(day//10) + str(day%10) + '.' + str(month//10) + str(month%10) + '.' + str(year) )
    return str(day // 10) + str(day % 10) + '.' + str(month // 10) + str(month % 10) + '.' + str(year)


# The begining of calculation program. No interface widgets. Started by startCalculation().
def mainCalc(percent, late_time, Working_Days, file_name, output_file_name):
    data = read_info(file_name)  # This is the first input of data
    data = first_data_check(data)
    u_d = dataDatesConvertToInt(data)  # Special variable not to call the function two times
    data = u_d[0]  # Return tuple, NEW data[][][] with dates converted to int, AND firstYear, 18 for 2018.
    firstYear = u_d[1]
    calend = makeCalendarList(firstYear)

    incomes = []
    outcomes = []

    for i in range(0, len(
            data)):  # This part shoul be rewrited, in fact tehre are 4 main and one additional type of words and we should separete them
        if data[i][1][0] == 'П' and data[i][1][3] == 'х' or data[i][1][0] == 'О' and data[i][1][1] == 'Т':
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
    try:
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
    except:
        global some_error
        global type_of_error
        some_error = True
        type_of_error += ' Some errors in main calculations'
    write_info(makeReport(fee_fedbak_final, percent, firstYear), output_file_name)
