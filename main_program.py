from tkinter import *
import os 
import codecs
import Tr_6




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
        Tr_6.main(float(Percent) / 100, int(late_time))
    return(0)







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


entry_Percent = Entry(root)
entry_Percent.place(x = 360, y = 51)
entry_Time = Entry(root)
entry_Time.place(x = 300, y = 76)


button_Main = Button(root, text = 'Press')
button_Main.bind('<Button-1>', lambda event: start(entry_Percent.get(), entry_Time.get()))
button_Main.place(x = 240, y = 300)

root.mainloop()