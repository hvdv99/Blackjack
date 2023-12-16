from blackjack_from_command_line.classes import *
from blackjack_with_tkinter.helpers import draw_possible, blackjack, winner

def show_hands():
  print(the_dealer, the_player, end='\n', sep='\n')

"""
The deck, dealer and player are initiated.
The dealer is dealt one card.
The player is dealt 2 cards,
While the game is still on: the player gets the following options: Hit, Stand, Double Down, Split, Surrender
"""

request = input("Do you want to play a game of blackjack? (Y, N)\n").strip().lower()
if request[0] == 'y':
  name = input('What is your name?\n')

  while True:
    # init deck
    the_deck = Deck(ndecks=2)
    the_deck.shuffle()

    #init dealer
    the_dealer = Player('Dealer')
    the_dealer.hand.cards.append(the_deck.draw()) # deals dealer one card

    # init player
    name.strip().capitalize()
    the_player = Player(name)
    print('\n')
    for _ in range(2):
       the_player.hand.cards.append(the_deck.draw()) # deals player 2 cards

    while draw_possible(the_player):
        bet = int(input("What is your bet?\n"))
        checker = True
        while checker:
          if bet <= the_player.money:
            the_player.money -= bet
            checker = False
          else:
            print("Not enough money to bet, please bet lower\n")
            bet = int(input("What is your bet?\n"))

        show_hands()

        question = input(f'What is your choice {the_player.name}? (Hit, Stand, Double Down, Split or Surrender)\n').strip().lower()

        if question == 'hit':
            the_player.hand.cards.append(the_deck.draw())
            show_hands()
            if blackjack(the_player):
                break

        if question == 'stand':
            while the_dealer.hand.value() < 17:
                the_dealer.hand.cards.append(the_deck.draw())
                if blackjack(the_dealer):
                  break
            break

    show_hands()

    if the_dealer.hand.value() == the_player.hand.value():
       the_player.money += bet
       print("It's a draw!")
       print(f'Current money: {the_player.money}\n\n')

    else:
      winner2 = winner(the_player, the_dealer)
      winner2.money += (2*bet)
      print(f'{print(winner2.name)} is the winner!\n')
      print(f'Current money: {the_player.money}\n\n')

    again = input("Do you want to play another game?\n (y, n)")
    again = again.strip().lower()
    if again[0] != 'y':
        print('GAME OVER')
        break

else:
    print('GAME OVER')
