from PIL import Image, ImageTk
import os
import random

class pngCards:
    def __init__(self, ndecks=1):
      PATH = './cards'
      card_names = [f for f in list(os.listdir(PATH)) if f.endswith('.png')]
      card_values = {}
      for cn in card_names.copy():
         temp = os.path.splitext(cn)[0]
         temp = temp[:-1]
         if temp.isnumeric():
            card_values[cn] = int(temp)
         elif temp[0] == 'A':
            card_values[cn] = 11
         else:
            card_values[cn] = 10

      cards_dict = {}
      for cn in card_names:
          im = Image.open(os.path.join(PATH, cn))
          im_resized = im.resize((int(75*1.5), int(120*1.5)))
          cards_dict[cn] = im_resized

      card_names*=ndecks

      self.cards_dict = cards_dict
      self.card_names = card_names
      self.card_values = card_values