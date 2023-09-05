import tkinter as tk
from cards import pngCards
from PIL import ImageTk
import random

def renew_deck():
  cards_obj = pngCards(ndecks=2)
  card_names = cards_obj.card_names
  cards_imgs = cards_obj.cards_dict
  card_values = cards_obj.card_values
  return card_names, cards_imgs, card_values

card_names, cards_imgs, card_values = renew_deck()

def draw_card():
    some_card_name = str(random.sample(card_names, 1)[0])
    some_card = cards_imgs[some_card_name]
    card_names.remove(some_card_name)
    del cards_imgs[some_card_name]
    return ImageTk.PhotoImage(some_card), some_card_name

def start_game():
    dealer_cards = dealer_frm.grid_slaves(row=0, column=1)[0].grid_slaves(row=0)
    player_cards = player_frm.grid_slaves(row=0, column=1)[0].grid_slaves(row=0)

    # reset hands and scores if there are cards in them
    for hand in [dealer_cards, player_cards]:
      for card in hand:
          if card.cget("image"):
            card.configure(image="")
            card.image = ""

    # set the hand values to 0
    for i in range(2):
        hand_values['ace1'][i] = 0
        hand_values['ace11'][i] = 0

    # renew deck
    global card_names, cards_imgs, card_values
    card_names, cards_imgs, card_values = renew_deck()

    # dealer gets one card
    dealer_hit()

    dealer_frm.grid_slaves(row=0, column=0)[0].configure(text=f"Dealer: {str(hand_values['ace11'][0])}")

    # player gets two cards
    for _ in range(2):
        player_hit()

    player_frm.grid_slaves(row=0, column=0)[0].configure(text=f"Player: {str(hand_values['ace11'][1])}")

    # now we just need the hit, stand and quit buttons
    buttons = button_area.pack_slaves()
    for btn in buttons:
        btn.pack_forget()

    hit_btn = tk.Button(button_area, text="Hit!", command=player_hit)
    hit_btn.pack(fill=tk.BOTH)
    stand_btn = tk.Button(button_area, text="Stand!", command=stand)
    stand_btn.pack(fill=tk.BOTH)
    quit_btn = tk.Button(button_area, text="Quit!", command=quit)
    quit_btn.pack(fill=tk.BOTH)

def player_hit():
    new_card, card_name = draw_card()
    player_cards = player_frm.grid_slaves(row=0, column=1)[0].grid_slaves(row=0)

    # update the image of the first empty card slot
    for slot in player_cards:
        if not slot.cget("image"):
            slot.configure(image=new_card)
            slot.image = new_card
            break

    # update value of player's hand
    hand_values['ace11'][1] += card_values[card_name]
    if card_name[0] == 'A':
        hand_values['ace1'][1] += 1
    else:
        hand_values['ace1'][1] += card_values[card_name]

    # when the player goes bust because his hand value > 21 and there is an ace in his hand,
    # we switch the value of his hand to that when the ace is counted as 1.
    if hand_values['ace11'][1] > 21 and hand_values['ace1'][1] <= 21:
        hand_values['ace11'][1] = hand_values['ace1'][1]
    player_frm.grid_slaves(row=0, column=0)[0].configure(text=f"Player: {str(hand_values['ace11'][1])}")

    # check if player busted
    if hand_values['ace11'][1] > 21:
        player_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Player: {str(hand_values["ace11"][1])} BUSTED!')
        dealer_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Dealer: {str(hand_values["ace11"][0])} WINNER!')
        reset_btn_frame()

def dealer_hit():
    new_card, card_name = draw_card()
    dealer_cards = dealer_frm.grid_slaves(row=0, column=1)[0].grid_slaves(row=0)

    # update the image of the first empty card slot
    for slot in dealer_cards:
        if not slot.cget("image"):
            slot.configure(image=new_card)
            slot.image = new_card
            break

    #update value of dealer's hand
    hand_values['ace11'][0] += card_values[card_name]
    if card_name[0] == 'A':
        hand_values['ace1'][0] += 1
    else:
        hand_values['ace1'][0] += card_values[card_name]

    # when the dealer goes bust because he has an ace in his hand, we set the value of his hand to that when the ace is
    # counted as 1.
    if hand_values['ace11'][0] > 21 and hand_values['ace1'][0] <= 21:
        hand_values['ace11'][0] = hand_values['ace1'][0]
    dealer_frm.grid_slaves(row=0, column=0)[0].configure(text=f"Dealer: {str(hand_values['ace11'][0])}")

def stand():
    while hand_values['ace11'][0] < 17:
        dealer_hit()
        # check if dealer busted
        if hand_values["ace11"][0] > 21:
            dealer_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Dealer: {str(hand_values["ace11"][0])} BUSTED!')
            player_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Player: {str(hand_values["ace11"][1])} WINNER!')
            reset_btn_frame()
            return # return statement because we want the function to end when dealer busted.

    # check who won
    # check if it is a tie
    if hand_values["ace11"][0] == hand_values["ace11"][1]:
        dealer_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Dealer: {str(hand_values["ace11"][0])} TIE!')
        player_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Player: {str(hand_values["ace11"][1])} TIE!')
    # check if dealer won
    elif hand_values["ace11"][0] > hand_values["ace11"][1]:
        dealer_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Dealer: {str(hand_values["ace11"][0])} WINNER!')
        player_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Player: {str(hand_values["ace11"][1])} LOSER!')
    else:
        dealer_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Dealer: {str(hand_values["ace11"][0])} LOSER!')
        player_frm.grid_slaves(row=0, column=0)[0].configure(text=f'Player: {str(hand_values["ace11"][1])} WINNER!')
    reset_btn_frame()

def reset_btn_frame():
    btn_widgets = button_area.pack_slaves()
    for btn in btn_widgets: # remove all buttons
            btn.pack_forget()

    # now we just need the start button and the quit button
    start_btn = tk.Button(master=button_area, bg='green', text='Start Game!', relief=tk.SUNKEN, border=1, command=start_game)
    quit_btn = tk.Button(master=button_area, bg='green', text='Quit!', relief=tk.SUNKEN, border=1, command=root.destroy)
    start_btn.pack(fill=tk.BOTH)
    quit_btn.pack(fill=tk.BOTH)

root = tk.Tk()
root.title('Blackjack')

# Left side of window
left_frm = tk.Frame(master=root, bg='green')
left_frm.columnconfigure(weight=1, minsize=200, index=0)
left_frm.rowconfigure(weight=1, minsize=100, index=[0,1,2,3,4])

# Left side buttons
button_area = tk.Frame(master=left_frm)
start_btn = tk.Button(master=button_area, bg='green', text='Start Game!', relief=tk.SUNKEN, border=1, command=start_game)
quit_btn = tk.Button(master=button_area, bg='green', text='Quit!', relief=tk.SUNKEN, border=1, command=root.destroy)
start_btn.pack(fill=tk.BOTH)
quit_btn.pack(fill=tk.BOTH)

empty_frm1 = tk.Frame(master=left_frm, bg='green').grid(row=0, column=0)
empty_frm2 = tk.Frame(master=left_frm, bg='green').grid(row=1, column=0)
button_area.grid(row=2, column=0)
left_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Right side
right_frm = tk.Frame(master=root, bg='green')
right_frm.columnconfigure(weight=1, minsize=10, index=0)
right_frm.rowconfigure(weight=1, minsize=10, index=[0,1])

# Right side frames
dealer_frm = tk.Frame(master=right_frm, bg='green', width=1000)
player_frm = tk.Frame(master=right_frm, bg='green', width=1000)

dealer_frm.columnconfigure(weight=1, minsize=90, index=[0,1])
dealer_frm.rowconfigure(weight=1, minsize=20, index=0)
player_frm.columnconfigure(weight=1, minsize=90, index=[0,1])
player_frm.rowconfigure(weight=1, minsize=20, index=0)

# Interactive value and card spaces
hand_values = {'ace1':{0: 0, 1: 0},'ace11':{0: 0, 1: 0}}
for i, frm in enumerate([dealer_frm, player_frm]):
    value_frm = tk.Label(master=frm, text=f"Value: {hand_values['ace11'][i]}", fg='white', bg='green', padx=10, pady=10)
    cards_frm = tk.Frame(master=frm, bg='green', width=800, height=200, padx=10, pady=10)
    cards_frm.rowconfigure(weight=1, minsize=100, index=0)
    for i in range(6):
        cards_frm.columnconfigure(weight=1, minsize=100, index=i)
        lbl = tk.Label(master=cards_frm, image=None, bg="green", padx=3, pady=3)
        lbl.grid(row=0, column=i)
    value_frm.grid(row=0, column=0)
    cards_frm.grid(row=0, column=1)

dealer_frm.grid(row=0, column=0, sticky='nesw')
player_frm.grid(row=1, column=0, sticky='nesw')
right_frm.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.mainloop()