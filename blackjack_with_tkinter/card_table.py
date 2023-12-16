import tkinter as tk
from PIL import ImageTk
import cards
import random


def draw_card():
    global cards_dict
    global card_names

    # drawing a random card
    some_card_name = card_names[random.randint(0, len(card_names)-1)]
    some_card = cards_dict[some_card_name]
    some_card_tk = ImageTk.PhotoImage(some_card)

    lbl.config(image=some_card_tk)
    lbl.image = some_card_tk


root = tk.Tk()

mfrm = tk.Frame(root, bg='green', width=180, height=80, pady=30, padx=30)
mfrm.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

# calling the cards object
obj = cards.pngCards()
cards_dict = obj.cards_dict
card_names = obj.card_names

# drawing a random card
some_card_name = card_names[random.randint(0, len(card_names)-1)]
some_card = cards_dict[some_card_name]
some_card_tk = ImageTk.PhotoImage(some_card)

lbl = tk.Label(master=mfrm, image=some_card_tk, bg="green")
lbl.pack()

stop_frm = tk.Frame(master=mfrm, bg="green")

draw_card_btn = tk.Button(master=stop_frm, text='Draw!', border=1, relief=tk.GROOVE, command=draw_card, bg='green')
stop_btn = tk.Button(master=stop_frm, text='Quit!', border=1, relief=tk.GROOVE, command=root.destroy, bg='green')

stop_btn.grid(row=0, column=0)
draw_card_btn.grid(row=1, column=0)

stop_frm.pack(side=tk.BOTTOM, fill=tk.Y)

tk.mainloop()
