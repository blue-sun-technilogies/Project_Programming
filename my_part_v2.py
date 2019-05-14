'''
py_part.py, 8/05/2019
Создать отдельный файл, создать массив (fee_fedbak_final).
output -  выводить в отдельный тексовый файл подряд идущие эоементы массива,
у которых совпадает второй элемент - задолжность (период дней, задолжность и штраф). работать должна во всех случиях
v1 - шаблон для любой задачи фильтрации данных.
v2 - выводит в файл подряд идущие эоементы массива, у которых совпадает NUMF элемент
'''

# принимает: имя файла , возвращает: список с содержимым файла.
def inputf(file_name):
    with open(file_name, 'r') as f:
        return [line.split(',')[:-1] for line in f]

# Из списка списков lst копирует в возвращаемый список подряд идущие эоементы массива, у которых совпадает второй элемент.
def processing(lst):
    ln = len(lst)
    NUMF=3
    prev_added=False # Был ли добавлен второй элемент пары  на предыдущем шаге цикла?
    retval = []
    for i in range(ln-1):
        if lst[i][NUMF]==lst[i+1][NUMF]:
            if not prev_added:        # Если второй элемент пары не был добавлен на предыдуще шаге цикла, то...
                retval.append(lst[i]) # ...то добавляем его (на этом шаге он стал первым).
            retval.append(lst[i+1])
            prev_added = True  # Если второй элемент добавлен - отметим это во флаге.
        else:
            prev_added = False # Если второй элемент НЕ добавлен - отметим это во флаге.
    return retval

# принимает список, печатает список в csv файл fname через запятую.
def output(lst, file_name):
    with open(file_name, 'w') as fname:
        for line in lst:
            print(*line,sep=',')
            print(*line, sep=',', file=fname)

lst=inputf('1.csv')
# print('DEBUG:\n', *lst, end='\nDEBUG END\n')
lst=processing(lst)
output(lst, 'output.csv')