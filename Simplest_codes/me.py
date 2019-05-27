# [0] = дата, [1] = задолжность
fee_feedback_final = [[9, 0, 0],
                     [10, 0, 0],
                     [11, 0, 0],
                     [12, 408.0, 8.16],
                     [13, 3476.0, 69.52],
                     [14, 3476.0, 69.52],
                     [14, 3476.0, 69.52],
                     [15, 2911.0, 58.22]]

#нужно посчитать количество дней, когда задолжность была одинакова.
def makeReport(f):
    output_list = []
    begin = f[0][0]
    for i in range(len(f)):
        circle_body = i + 1 <= len(f) - 1
        if circle_body and f[i][1] != f[i + 1][1] or not circle_body:
            output_list.append((f'За {f[i][0] - begin + 1} ' +
                (f'дней с {begin} по {f[i][0]} ' if f[i][0] - begin > 0 else f'день {begin} числа ') +
                f'задолженность составила {(f[i][0] - begin + 1) * f[i][1]}' +
                f' штраф {(f[i][0] - begin + 1) * f[i][2]}'))
        if circle_body and f[i][1] != f[i + 1][1]:
            begin = f[i + 1][0]
    return output_list
            
print(*makeReport(fee_feedback_final), sep='\n')
#print(makeReport(fee_feedback_final))
