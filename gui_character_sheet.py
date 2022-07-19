from tkinter import *
from random import randint
from sys import exit

# make initial stats
def stats():
    global l1, l2, str, dex, intel
    str = randint(5,10)
    dex = randint(5,10)
    intel = randint(5, 10)
    ttt = (f"{name.get()}\nSTR - {str}\nDEX - {dex}\nINT - {intel}")
    l1 = Label(f2, text=ttt)
    l1.pack()
    hp_value = str * 3
    att_value = dex * 3
    def_value = dex * 3
    armor_value = 0
    dmg_value = 0 + (str * 0.20)
    focus = int(intel * 1.20)
    stt = (f"HP - {hp_value}\nAtt - {att_value}\nDef - {def_value}\nArmor - {armor_value}"
           f"\nDMG - {dmg_value:.0f}\nFocus - {focus}")
    l2 = Label(f3, text=stt) # update labels
    l2.pack()
    # enable/disable buttons
    b1.configure(state="disabled")
    b2.configure(state="normal")

# reroll stats
def roll():
    global str, dex, intel
    str = randint(5, 10)
    dex = randint(5, 10)
    intel = randint(5, 10)
    ttt = (f"{name.get()}\nSTR - {str}\nDEX - {dex}\nINT - {intel}")
    l1.configure(text=ttt)
    hp_value = str * 3
    att_value = dex * 3
    def_value = dex * 3
    armor_value = 0
    dmg_value = 0 + (str * 0.20)
    focus = int(intel * 1.20)
    stt = (f"HP - {hp_value}\nAtt - {att_value}\nDef - {def_value}\nArmor - {armor_value}"
           f"\nDMG - {dmg_value:.0f}\nFocus - {focus}")
    l2.configure(text=stt) # update labels


# initiate tkinter
p = Tk()
p.title("Character Creation")
p.iconbitmap(r"C:/Users/Ivo/PycharmProjects/python_basics/side_project/helmlogo.ico")
p.geometry("400x400")

f1 = LabelFrame(p, text="Enter character name")
f1.pack(padx=10, pady=10)
name = Entry(f1, width=30)
name.pack()

# tkinter variables
str = IntVar()
dex = IntVar()
intel = IntVar()

f2 = LabelFrame(p, text="Stats")
f2.pack(padx=10, pady=10)

f3 = LabelFrame(p, text="Combat Stats")
f3.pack(padx=10, pady=10)

# make buttons
b1 = Button(f1, text="Show stats", state=NORMAL, command=stats)
b1.pack()
b2 = Button(f1, text="Reroll", state=DISABLED, command=roll)
b2.pack()
be = Button(p, text="Close", command=exit)
be.pack(side=BOTTOM)

mainloop()
