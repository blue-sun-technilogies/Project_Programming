import requests
from chardet.universaldetector import UniversalDetector

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
calend = calendar(2019)
print(calend)


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