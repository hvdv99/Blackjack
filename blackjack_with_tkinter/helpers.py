
def draw_possible(a_player):
    if a_player.hand.value() < 21:
        return True
    return False

def blackjack(a_player):
    if a_player.hand.value() == 21:
        return True
    return False

def winner(a_player, the_dealer):
    if (a_player.hand.value() <= 21) and (the_dealer.hand.value() <= 21):
        if a_player.hand.value() > the_dealer.hand.value():
            return a_player
        return the_dealer
    else:
        if a_player.hand.value() > 21:
            return the_dealer
        return a_player