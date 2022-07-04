from tkinter import *
from math import *
from functools import partial

root = Tk()
w = 650 #разрешение
h = 750
root.geometry(str(w) + "x" + str(h)) #создаем окно width x height
root.title("Аффинные преобразования")

#приблизительная фигура
points = [[-3.5,-1.5],[-3.5,3],[-1,3],[3.3,-2.8],[3.1,-0.8],[-3.5,-1.45]]

save = [[x,y] for x,y in points] #для сброса
c = Canvas(root, width=w, height=h/2 + w/4, bg='white')
c.grid(row = 0,column = 0,columnspan = 4 + 3)

face = 110; #сколько примерно занимает интерфейс
m = 45 #масштаб фигуры
c.create_line(0, h/2 - face, w, h/2 - face) #учитываем выравнивание
c.create_line(w/2, 0, w/2, h)
c.create_line(w/2 + 50, h/2-8-face, w/2+50, h/2+8-face)
c.create_line(w, h/2 - face, w - 30, h/2 - face + 8)
c.create_line(w, h/2 - face, w - 30, h/2 - face - 8)
c.create_line(w/2, 0, w/2 + 8, 30)
c.create_line(w/2, 0, w/2 - 8, 30)
c.create_text(w/2+58,h/2-10-face,fill="black",font="Times 13 italic bold",text="1")
c.create_text(w/2+7,h/2-10-face,fill="black",font="Times 13 italic bold",text="0")
c.create_text(w-40,h/2+30-face,fill="black",font="Times 15 italic bold",text="X")
c.create_text(w/2+15,50,fill="black",font="Times 15 italic bold",text="Y")

#побочная функция для расчета поворота
def rotate(angle, x0, y0 , x, y):
    rad = angle * pi / 180.0
    return x0 + cos(rad)*(x-x0)-sin(rad)*(y-y0),y0 + sin(rad)*(x-x0)+cos(rad)*(y-y0)

#поворот
def rot2D(angle,x0,y0):
    for i in range(len(points)):
        points[i][0],points[i][1] = rotate(angle,x0,y0,points[i][0],points[i][1])

#масштабирование
def resize(a,b):
    for i in range(len(points)):
        points[i][0] = points[i][0]*a
        points[i][1] = points[i][1]*b

#перемещение
def moving(u,q):
    for i in range(len(points)):
        points[i][0] = points[i][0] + u
        points[i][1] = points[i][1] + q

#отражение
def mirror():
    for i in range(len(points)):
        points[i][0] = -points[i][0] + w
        points[i][1] = points[i][1]

#перерисовка и выбор преобразования
def display(i,a,b):
    global rect,points #чтобы можно было изменять
    c.delete(rect)
    if(i == 1):
       moving(-w/2,-h/2+face)
       resize(float(a.get()),float(b.get()))
       moving(w/2,h/2-face)
    elif(i == 2):
        rot2D(float(a.get()),w/2,h/2-face);
    elif(i == 3):
        moving(float(a.get()),float(b.get()));
    elif(i == 4):
        mirror();
    elif(i == 5):
        points = [[x,y] for x,y in save]
        resize(m,m)  #изначальный масштаб фигуры
        moving(w/2,h/2-face)
        rot2D(180,w/2,h/2-face)
        mirror()
    rect = c.create_line(points,width=3)

#меню на основе grid таблицы
def menu():
    lb = Label(text = "ширина =")
    lb.grid(row = 1,column = 0)
    lb = Label(text = "высота =")
    lb.grid(row = 2,column = 0)
    ent = Entry(textvariable = rza,width = 10)
    ent.insert(0,'0.9')
    ent.grid(row = 1,column = 1,pady = 5) #a - масштаб по x
    ent = Entry(textvariable = rzb,width = 10)
    ent.insert(0,'1.1')
    ent.grid(row = 2,column = 1) #b - масштаб по y
    
    lb = Label(text = "угол =")
    lb.grid(row = 1,column = 2, rowspan = 2)
    ent = Entry(textvariable = fi,width = 10)
    ent.insert(0,'30')
    ent.grid(row = 1,column = 3,rowspan = 2) #угол
    
    lb = Label(text = "шаг по x =")
    lb.grid(row = 1,column = 4)
    lb = Label(text = "шаг по y =")
    lb.grid(row = 2,column = 4)
    ent = Entry(textvariable = mva,width = 10)
    ent.insert(0,'40')
    ent.grid(row = 1,column = 5) #u - сдвиг по x
    ent = Entry(textvariable = mvb,width = 10)
    ent.insert(0,'-30')
    ent.grid(row = 2,column = 5) #q - сдвиг по y
    
    #создаем кнопки и присваиваем им функцию
    func = partial(display,1,rza,rzb)
    btn = Button(text = 'Масштаб',command = func,width = 18)
    btn.grid(row = 3,column = 1,ipadx = 2,ipady = 5,pady = 30)
    
    func = partial(display,2,fi,0)
    btn = Button(text = 'Поворот', command = func,width = 18)
    btn.grid(row = 3,column = 3,ipadx = 2,ipady = 5)
    
    func = partial(display,3,mva,mvb)
    btn = Button(text = 'Сдвиг', command = func,width = 18)
    btn.grid(row = 3,column = 5,ipadx = 2, ipady = 5)
    
    func = partial(display,4,0,0)
    btn = Button(text = 'Отразить', command = func,width = 18)
    btn.grid(row = 4,column = 1,ipadx = 2, ipady = 5)
  
    func = partial(display,5,0,0)
    btn = Button(text = 'Сбросить', command = func,width = 18)
    btn.grid(row = 4,column = 3,ipadx = 2, ipady = 5)

resize(m,m)  #изначальный масштаб фигуры
moving(w/2,h/2-face)
rot2D(180,w/2,h/2-face)
mirror()
rect = c.create_line(points,width=3)

#угол поворота
fi = StringVar()

#масштабирование
rza = StringVar()
rzb = StringVar()

#перенос
mva = StringVar()
mvb = StringVar()

menu()
c.mainloop()