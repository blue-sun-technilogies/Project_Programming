import smtplib
import requests  # Requre: pip3 install requests


some_error = False
type_of_error = ''
to_user_error = ''


def first_data_check(data):
    # This function check the position of the information in the file
    global some_error
    global type_of_error
    if data[0][0] == '':
        try:
            for i in range(len(data) + 1):
                data[i][0] = data[i][6]
                data[i][1] = data[i][7]
                data[i][3] = data[i][9]
                data[i][5] = data[i][11]
        except Exception:
            some_error = True
            type_of_error += (
                'The problem in file, the finding of the info position'
            )
    return data


def make_calendar_list(first_year=0, tries=7):
    global some_error
    global type_of_error
    for i in range(7):
        try:
            # Use API for calendar days to define work days and holidays
            url = 'https://isdayoff.ru/api/getdata?year='
            r = requests.get(url + str(first_year + 2000))
            return [1 if elem == 49 else 0 for elem in r.content]
        except ConnectionError:
            if i + 1 == tries:
                some_error = True
                type_of_error += (
                    'The problem in file, the finding of the info position'
                )


def read_info(file_name):
    # This function read information from input_file
    data = []
    with open(file_name, 'r', encoding='utf-8') as file_name:
        chec_to_sit_in_end = False  # Finding the place of data
        for line in file_name:
                if (((line[0] + line[1]).isdigit() and
                        line[2] == '.') or chec_to_sit_in_end):
                    part = line.split(',')
                    # This is a split of information into a matrix
                    row = part[:14]
                    data.append(row)
                elif (chec_to_sit_in_end is False):
                    part = line.split(',')
                    if part[0] == '' and len(part) > 6:
                        if len(part[6]) >= 3:
                            if (part[6][0].isdigit() and part[6][1].isdigit and
                                    part[6][2] == '.'):
                                # This is a split of on information in the way
                                # if info was situated in another part of file
                                row = part[:14]
                                data.append(row)
                                chec_to_sit_in_end = True
    return data


def write_info(report, output_file_name):
    # Function of writing penalty in output file
    with open(output_file_name, 'w', encoding='utf-16') as fo:
        # Information is outputed to the doc format
        for elem in report[0]:
            fo.write(elem)
        # This is the last line of the output file
        fo.write(f'Общая сумма штрафа составила {round(report[1], 2)} рублей')


def update_outcomes(outcomes):
    # Function that united all info from one day for outcomes
    outcomes_updated = []
    i = 0
    while i < len(outcomes):
        outcomes_updated.append(outcomes[i])
        if i + 1 < len(outcomes):
            while outcomes[i + 1][0] == outcomes[i][0]:
                outcomes_updated[len(outcomes_updated) - 1][3] += (
                    float(outcomes[i + 1][3]))
                i += 1
                if i + 1 == len(outcomes):
                    break
        i += 1
    return outcomes_updated


def incomes_update(incomes):
    # This function is needed for calculation,
    # again united the information from one day for incomes
    incomes_updated = []
    i = 0
    while i < len(incomes):
        incomes_updated.append(incomes[i])
        if i + 1 < len(incomes):
            while incomes[i + 1][0] == (
                    incomes_updated[len(incomes_updated) - 1][0]):
                incomes_updated[len(incomes_updated) - 1][5] += (
                    float(incomes[i + 1][5])
                )
                i += 1
                if i + 1 == len(incomes):
                    break
        # In that block we check for the information from the one day
        # and unite it to one line
        i += 1
    return incomes_updated


def make_report(file, percent, first_year):
    # This function unite the information for output
    # It makes report for period of debt times
    output_list = []
    final_to_pay = 0
    begin = file[0][0]
    for i in range(len(file)):
        circle_body = i + 1 <= len(file) - 1
        if circle_body and file[i][1] != file[i + 1][1] or not circle_body:
            output_list.append(
                f'Количество дней - {file[i][0] - begin + 1} ' +
                f'дней с {day_to_str(begin, first_year)} по ' +
                (
                    f'{day_to_str(file[i][0], first_year)} '
                    if file[i][0] - begin > 0 else
                    f'день {day_to_str(begin, first_year)} числа '
                ) +
                f'задолженность составила ' +
                f'{round((file[i][0] - begin + 1) * file[i][1], 2)} ' +
                f'штраф {round((file[i][0] - begin + 1) * file[i][2], 2)}, '
                f'пени = {percent}%, формула расчета: сумма штрафа = '
                f'{(file[i][0] - begin + 1) *file[i][1]}/100*{percent}\n'
            )
            final_to_pay += (file[i][0] - begin + 1) * file[i][2]
        if circle_body and file[i][1] != file[i + 1][1]:
            begin = file[i + 1][0]
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


def is_intercalary_year(year):
    # Function defying is year intercalary or not (int), 18 for 2018.
    year -= 2000  # for yy only
    # For gregorian calendar
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def day_to_int(day, month, year, first_year):
    # for years: from firstYear to current_year except last one.
    for _year in range(first_year, year):
        day += 366 if is_intercalary_year(_year) else 365
    for _month in range(1, month):
        day += days_in_months[_month]
    if month > 2 and is_intercalary_year(year):
        day += 1  # Febr intercalary current year.
    return day


def data_dates_convert_to_int(data):
    first_year = int(data[0][0][6:8])  # 18 for 2018
    try:
        for i in range(0, len(data)):
            # In this function we convert date
            # in appropriate form for processing
            lst = data[i][0].split(',')[0].split('.')
            data[i][0] = day_to_int(
                int(lst[0]), int(lst[1]), int(lst[2]), first_year
            )
    except IndexError:
        global some_error
        global type_of_error
        global to_user_error
        some_error = True
        type_of_error += 'Problem in the function data_dates_convert_to_int'
        to_user_error += (
            'Проверьте корректность дат в файле, убедитесь, '
            'что даты разделены точкой, а не запятой, '
            'в случае если все верно, свяжитесь с нами и опишите проблему'
        )
        # Tuple - (Total number of days, include current_day;
        #   year is int, 18 for 2018).
    return data, first_year


def day_to_str(date, first_year):
    # print("DEBUG day_to_str(date="+str(date), end='')
    day, month, year = date, 1, first_year
    # Duration of the year
    year_length = 365 + int(is_intercalary_year(year))
    while date >= year_length:
        date -= year_length
        if date == 0:  # If there is no more days in year
            day, month = 31, 12  # ... 31.12 - last day of the year.
        else:
            year += 1
            # Duration of the year
            year_length = int(is_intercalary_year(year))
    while date >= days_in_months[month]:
        date -= days_in_months[month]
        if date == 0:  # If there is no more days in month
            day = days_in_months[month]  # ... last day in month
        else:  # If no
            month += 1  # ... go next month
            day = date
            # print(
            #     f', first_year={first_year}' +
            #     f") returns {day // 10}{day % 10}" +
            #     f'.{month // 10}{month % 10}.{year}'
            # )
    return f'{day // 10}{day % 10}.{month // 10}{month % 10}.{year}'


def main_calc(percent, late_time, working_days, file_name, output_file_name):
    # The begining of calculation program.
    # No interface widgets. Started by startCalculation().
    data = read_info(file_name)  # This is the first input of data
    data = first_data_check(data)
    # Special variable not to call the function two times
    u_d = data_dates_convert_to_int(data)
    # Return tuple, NEW data[][][] with dates converted to int,
    # AND first_year, 18 for 2018.
    data = u_d[0]
    first_year = u_d[1]
    calend = make_calendar_list(first_year)

    # To lists in which data will be separated
    incomes = []
    outcomes = []

    for i in range(len(data)):
        # This part shoul be rewrited, in fact tehre are 4 main and
        # one additional type of words and we should separete them
        if (data[i][1][0] == 'П' and data[i][1][3] == 'х' or
                data[i][1][0] == 'О' and data[i][1][1] == 'Т'):
            data[i][5] = float(data[i][5])
            incomes.append(data[i])

        elif data[i][1][0] == 'О' and data[i][1][2] == 'л':
            data[i][3] = float(data[i][3])
            outcomes.append(data[i])

    # Updated versions of lists just to unite the info
    # from one day in one line
    outcomes_updated = update_outcomes(outcomes)
    incomes_updated = incomes_update(incomes)

    start_date = data[0][0]  # This is the first date for calculation
    last_date = data[len(data) - 1][0]
    fee_to_pay = 0
    # The number of incomes with which we are workig
    current_incomes_number = 0
    current_outcomes_number = 0
    # This variable is needed to remember all money which was not paied
    not_used_outcomes = 0
    # Not to go in unnessesary part of the program in the last steps
    check_to_enter_outcomes = True

    fee_fedbak_final = []
    fee_fedbak = 0
    i = start_date
    while i <= last_date:  # The main function
        check_to_enter = True
        if not_used_outcomes != 0:

            # Check for the elder outcomes for which user still need to pay
            if (incomes_updated[current_incomes_number][5] -
                    not_used_outcomes >= 0):
                # In this pice of code we are cheaking
                # the quantity of money from the previous step and
                # cut them from the nem outcomes
                incomes_updated[current_incomes_number][5] -= (
                    not_used_outcomes)
                not_used_outcomes = 0
            else:
                not_used_outcomes -= (
                    incomes_updated[current_incomes_number][5]
                )
                incomes_updated[current_incomes_number][5] = 0
                current_incomes_number += 1

        if (outcomes_updated[current_outcomes_number][0] == i and
                check_to_enter_outcomes):
            # Check if next outcome is going to be today
            if (incomes_updated[current_incomes_number][5] -
                    outcomes_updated[current_outcomes_number][3] >= 0):
                incomes_updated[current_incomes_number][5] -= (
                    outcomes_updated[current_outcomes_number][3]
                )
                outcomes_updated[current_outcomes_number][3] = 0
                # Switch to next outcomes_updated date
                current_outcomes_number += 1
                if incomes_updated[current_incomes_number][5] == 0:
                    current_incomes_number += 1
            else:
                not_used_outcomes = (
                    outcomes_updated[current_outcomes_number][3] -
                    incomes_updated[current_incomes_number][5]
                )
                incomes_updated[current_incomes_number][5] = 0
                current_incomes_number += 1
                # The outcomes become zero, previous incomes updates
                outcomes_updated[current_outcomes_number][3] = 0
                if current_outcomes_number + 1 < len(outcomes_updated):
                    # Check if is there another day
                    current_outcomes_number += 1
                else:
                    check_to_enter_outcomes = False
                i -= 1
                check_to_enter = False

        if working_days:  # This function calculate fee for working days
            if (i - incomes_updated[current_incomes_number][0] >
                    late_time and check_to_enter):
                # Checking if it neccessary to check
                # the quantity of days between these days
                quantity_working = 0
                for k in range(
                        incomes_updated[current_incomes_number][0] - 1, i):
                    if calend[k] == 0:
                        # Checking the quantity of
                        # working days between these days
                        quantity_working += 1
                if quantity_working > late_time:
                    fee_fedbak = 0
                    # The sum that we should pay in this day
                    current_sum_to_pay = (
                        incomes_updated[current_incomes_number][5]
                    )
                    if calend[current_incomes_number - 1] == 0:
                        # The total fee to pay
                        fee_to_pay += (
                            percent *
                            incomes_updated[current_incomes_number][5]
                        )
                        # The fee in the local day
                        fee_fedbak = (
                            percent *
                            incomes_updated[current_incomes_number][5]
                        )
                        j = 1
                        # This block will check the information while
                        # the sum which should be payed is more then zero
                        if (incomes_updated[current_incomes_number][0] !=
                                last_date and current_incomes_number + j <=
                                (
                                    len(incomes_updated) -
                                    current_incomes_number)):
                            while (i - incomes_updated[
                                    current_incomes_number + j][0] >
                                    late_time):
                                if calend[current_incomes_number - 1] == 0:
                                    fee_to_pay += (
                                        percent * incomes_updated[
                                            current_incomes_number + j][5]
                                    )
                                    current_sum_to_pay += (
                                        incomes_updated[
                                            current_incomes_number + j][5]
                                    )
                                    fee_fedbak += (
                                        percent *
                                        incomes_updated[
                                            current_incomes_number + j][5]
                                    )
                                    j += 1
                                if (incomes_updated[
                                        current_incomes_number][0] ==
                                        last_date or
                                        j == (
                                            len(incomes_updated) -
                                            current_incomes_number)):
                                    break

        # The same code, but do not pay attention to working days
        # Start checkingfor fees
        elif (i - incomes_updated[current_incomes_number][0] >
                late_time and check_to_enter):
            fee_fedbak = 0
            # Used for output in final
            current_sum_to_pay = incomes_updated[current_incomes_number][5]
            fee_to_pay += (
                percent * incomes_updated[current_incomes_number][5]
            )
            fee_fedbak = (
                percent * incomes_updated[current_incomes_number][5]
            )
            j = 1
            if (incomes_updated[current_incomes_number][0] != last_date and
                    current_incomes_number + j <=
                    (len(incomes_updated) - current_incomes_number)):
                while (i - incomes_updated[current_incomes_number + j][0] >
                        late_time):
                    fee_to_pay += (
                        percent *
                        incomes_updated[current_incomes_number + j][5]
                    )
                    current_sum_to_pay += incomes_updated[
                        current_incomes_number + j][5]
                    fee_fedbak += (
                        percent *
                        incomes_updated[current_incomes_number + j][5]
                    )
                    j += 1
                    if (incomes_updated[current_incomes_number][0] ==
                            last_date or
                            j == (
                                len(incomes_updated) -
                                current_incomes_number)):
                        break
        # Checking if it's neccessary to pay some fee
        if fee_to_pay != 0:
            fee_fedbak_final.append([i, current_sum_to_pay, fee_fedbak])

        else:
            fee_fedbak_final.append([i, 0, fee_fedbak])
        i += 1

    if some_error:
        # This part of code helps the creators tofind all the bugs of
        # the program, for this version all users will send reports,
        # after realise only who want to do this
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("cher6304830@gmail.com", "dzmhdmifphfvcqif")
        data_send = ''
        for i in range(len(data)):
            for k in range(14):
                data_send += str(data[i][k])
            data_send += '\n'
        server.sendmail(
            "cher6304830@gmail.com",
            "cher6304830@gmail.com",
            type_of_error
        )
        server.sendmail(
            "cher6304830@gmail.com",
            "cher6304830@gmail.com",
            data_send
        )
        server.quit()

    write_info(
        make_report(
            fee_fedbak_final,
            percent,
            first_year
        ),
        output_file_name
    )
