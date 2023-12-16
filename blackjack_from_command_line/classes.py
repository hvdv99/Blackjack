import random

symbols = ['A', 'C', 'H', 'D']
grades = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

# initiate the values for each grade
values = {}
for i in range(len(grades)):
    if grades[i] not in values:
      values[grades[i]] = None
    if grades[i] not in ['J','Q','K','A']:
      values[grades[i]] = i+2
    else:
      values[grades[i]] = 10


class Card:
  def  __init__(self, grade, symbol):
    self.symbol = symbol
    self.grade = grade
    self.display = grade+symbol
    self.value = values[self.grade]

  def __str__(self):
    return self.symbol+self.grade


class Deck:
  def __init__(self, ndecks=1):
    self.cards = list()
    for _ in range(ndecks):
      for i in [s+symbols for symbols in symbols for s in grades]: # this means each card has first the grade than the symbol!
        if len(i) == 2:
          grade  = i[0]
        else:
          grade = i[:2]
        temp_card = Card(grade, i[-1])
        self.cards.append(temp_card)

  def __len__(self):
    return len(self.cards)

  def shuffle(self):
    random.shuffle(self.cards)

  def draw(self):
    return self.cards.pop(random.randint(0,len(self.cards)-1))


class Hand:
  def __init__(self):
    self.cards = []

  def value(self):
    return sum([c.value for c in self.cards])

  def display(self):
    stringOfCards = ' - '.join([c.display for c in self.cards])
    return stringOfCards


class Player:
  def __init__(self, name):
    self.name = name
    self.hand = Hand()
    self.money = 10

  def __str__(self):
    return f"Player: {self.name}\nHand: {self.hand.display()}\nValue: {self.hand.value()}\n"