from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from calculation import *


def app(args):
    try:
        D = float(d_input.get())
        N = int(n_input.get())
        DT = float(dt_input.get())
        NT = int(nt_input.get())
        S = int(s_input.get())
    except:
        sys.exit("Входные данные ошибочны.")

    Z = calculate(D, N, DT, NT, S, f_input, u_input)

    if checked.get() == 1:
        fig, ax = plt.subplots()
        plt.ylim(Z.min(), Z.max())
        x = range(0, N)

        line, = ax.plot(x, Z[0])

        def init():
            line.set_ydata(np.ma.array(x, mask=True))
            return line,

        def frame(i):
            line.set_ydata(Z[i])
            return line,

        def output():
            anmt=animation.FuncAnimation(fig, frame, np.arange(0, NT), init_func=init, interval=300 * DT, blit=True)
            canvas.draw()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(column=0, row=7, columnspan=6)

        output()
    elif checked.get() == 2:
        fig = plt.figure()
        plt.imshow(Z.T)

        myCanvas = FigureCanvasTkAgg(fig, master=root)
        myCanvas.draw()
        myCanvas.get_tk_widget().grid(column=0, row=7, columnspan=6)
    else:
        sys.exit("Что-то пошло не так.")


root = Tk()
root.geometry('1000x650')
root.title("Численное решение уравнения диффузии")

d_label = Label(root, font=("Times New Roman", 12), text="D:")
d_label.grid(row=1, column=1, sticky=E)
d_input = Entry(root)
d_input.grid(row=1, column=2, sticky=W)
d_input.insert(0, "0.01")

n_label = Label(root, font=("Times New Roman", 12), text="N:")
n_label.grid(row=2, column=1, sticky=E)
n_input = Entry(root)
n_input.grid(row=2, column=2, sticky=W)
n_input.insert(0, "500")

dt_label = Label(root, font=("Times New Roman", 12), text="DT:")
dt_label.grid(row=3, column=1, sticky=E)
dt_input = Entry(root)
dt_input.grid(row=3, column=2, sticky=W)
dt_input.insert(0, "0.1")

nt_label = Label(root, font=("Times New Roman", 12), text="NT:")
nt_label.grid(row=4, column=1, sticky=E)
nt_input = Entry(root)
nt_input.grid(row=4, column=2, sticky=W)
nt_input.insert(0, "500")

u_label = Label(root, font=("Times New Roman", 12), text="u(x,0):")
u_label.grid(row=1, column=3, sticky=E)
u_input = Entry(root)
u_input.grid(row=1, column=4, sticky=W)
u_input.insert(0, "np.sin(5*x)")

f_label = Label(root, font=("Times New Roman", 12), text="F(u(x,t),t):")
f_label.grid(row=2, column=3, sticky=E)
f_input = Entry(root)
f_input.grid(row=2, column=4, sticky=W)
f_input.insert(0, "0.5*np.sin(0.1*u+t)")

s_label = Label(root, font=("Times New Roman", 12), text="S:")
s_label.grid(row=3, column=3, sticky=E)
s_input = Entry(root)
s_input.grid(row=3, column=4, sticky=W)
s_input.insert(0, "3")

checked = IntVar()
Radiobutton(root, font=("Times New Roman", 10), text="Анимация профиля волны", variable=checked, value=1)\
    .grid(row=5, column=2, columnspan=3, sticky=W)
Radiobutton(root, font=("Times New Roman", 10), text="Тепловая карта", variable=checked, value=2)\
    .grid(row=5, column=4, columnspan=3, sticky=W)
checked.set(1)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0, row=7, columnspan=6)

RunBtn = Button(root, font=("Times New Roman", 10), text='Построить', width=145, height=2)
RunBtn.bind("<Button-1>", app)
RunBtn.grid(row=6, column=0, columnspan=5)
root.mainloop()
