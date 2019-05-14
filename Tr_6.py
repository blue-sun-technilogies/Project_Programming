
import os
import codecs

def main(percent, late_time):
    def first_data_check(data):
        if data[0][0] == '':
            for i in range(0, len(data) + 1):
                data[i][0] = data[i][6]
                data[i][1] = data[i][7]
                data[i][3] = data[i][9]
                data[i][5] = data[i][11]
        return(data)

    def read_info(file_name):
        data = []
        file_name = codecs.open(r'C:\Users\Denis\Documents\HSE\Progs\Final_project\1.csv', 'r', 'utf-8')
        for line in file_name:
            chec_to_sit_in_end = False #Finding the place of data
            if (line[0].isdigit() and line[1].isdigit() and line[2] == '.') or chec_to_sit_in_end:
                print(line)
                part = line.split(',')
                row = [
                        part[0], part[1], part[2], part[3],
                        part[4], part[5], part[6], part[7],
                        part[8], part[9], part[10],
                        part[11], part[12], part[12],
                        part[13]
                    ]
                data.append(row)

        return data


    def update_outcomes(outcomes):
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
        return data












    data = read_info(r'C:\Users\Denis\Documents\HSE\Progs\Final_project\Data2.csv')
    data = first_data_check(data)
    data = qurent_date(data)


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
    fee_to_pay_previous = fee_to_pay #For output
    current_outcomes_date = outcomes_updated[0][0]
    current_incomes_date = incomes_updated[0][0]
    current_incomes_number = 0 #The number of incomes with which we are workig
    current_outcomes_number = 0
    not_used_outcomes = 0
    #late_time = 1
    #percent = 0.01
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
            print(f'Задолженность за {i} день составляет {current_sum_to_pay} рублей, штраф составляет {fee_fedbak} рублей')
            fee_fedbak_final.append([i, current_sum_to_pay, fee_fedbak])
        else:
            print(f'Задолженность за {i} день составляет 0 рублей, штраф составляет {fee_fedbak} рублей')
            fee_fedbak_final.append([i, 0, fee_fedbak])







        i += 1

    print(fee_fedbak_final)


    print(fee_to_pay)
