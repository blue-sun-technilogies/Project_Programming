'''
Эта функция подтягивает информацию с сайта о праздничных и рабочих днях в РФ в след формате: [49,49,49,48...] 
Далее преобразуют в след. формат [1, 1, 1, 0...], где (1 - выходные дни и 0 - будние дни на output).
Возвращает список, где индекс, начинающийся от 0 - номер дня в году, а значение 1 для вых. и 0 для буднего (int).
'''
def makeCalendarList(firstYear=0):
    import requests
    url = 'https://isdayoff.ru/api/getdata?year='  # Используем API для выходных дней
    path = url + str(firstYear + 2000)
    r = requests.get(path)
    # print(*r.content, type(r.content)) # ... 48 49 49 <class 'bytes'>
    return [1 if elem==49 else 0 for elem in r.content]


# Техническая функция модульного тестирования функций обьявленных в main()     
def test():
    print(*makeCalendarList(18))

# Техническая функция: Запуск модульного тестирования функций обьявленных в main()     
test()
