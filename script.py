import random as rm
from collections import deque
from tkinter import *

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
colors = ('black', 'red')
cardNames = ("Ace", "Deuce", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King")
cardLetters = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
cardValues = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)


CARD_IN_SUIT = 13
SUITS = 4


class Card:
    def __init__(self, suit : str, name:str, value : int):
        super().__init__()
        self.suit = suit
        self.setColor()
        self.name = name
        self.value = value
        self.letter = cardLetters[value - 1]
        self.setSymbol()
        self.face_shown = True
        self.x = self.y = 0


    def __str__(self):
        return "{0} of {1}".format(self.name, self.suit)
    
    def setSymbol(self):
        if self.suit == suits[0]:
            self.symbolNumber = 2665
        if self.suit == suits[1]:
            self.symbolNumber = 2666
        if self.suit == suits[2]:
            self.symbolNumber = 2660
        if self.suit == suits[3]:
            self.symbolNumber = 2663
        self.symbol = chr(int(str(self.symbolNumber), 16))

    def setColor(self):
        self.color = colors[1] if self.suit == suits[0] or self.suit == suits[1] else colors[0]

    def isAce(self):
        return self.value == 1

    def isKing(self):
        return self.value == 13


class CardDeck:
    def __init__(self):
        super().__init__()
        self.deck = []
        self.constructDeck()
        self.shuffleDeck()
    
    def constructDeck(self):
        for i in range(SUITS):
            for j in range(CARD_IN_SUIT):
                card = Card(suits[i], cardNames[j], cardValues[j])
                self.deck.append(card)

    def shuffleDeck(self):
        self.shuffled = False
        rm.shuffle(self.deck)
        self.shuffled = True

class BigDeck():
    def __init__(self):
        super().__init__()
        decks = [CardDeck() for i in range(2)]
        self.deck = decks[0].deck + decks[1].deck
        rm.shuffle(self.deck)
    
    def getTopCard(self):
        return self.deck[-1] if len(self.deck) > 0 else None

class BasePlaces:
    def __init__(self):
        super().__init__()
        self.places = [[]] * 8
        self.countOfFull = 0

    
    def getTopCard(self, index):
        return self.places[index][-1]

    def isSameSuit(self, card, index):
        return self.places[index][-1].suit == card.suit if len(self.places[index]) > 0 else True

    def isGreaterCard(self, index, card):
        return self.places[index][-1].value + 1 == card.value if len(self.places[index]) > 0 else card.isAce()
    
    def placeCard(self, index, card, smalldecks):
        print(card['id'])
        print(self.places[index])
        if len(self.places[index]) in range(13) and self.isSameSuit(card['card'], index) and self.isGreaterCard(index, card['card']):
            self.places[index].append(smalldecks.decks[card['id']].pop())
        # else: raise IndexError('Error: do not place more than 13 cards or do not place card with another suit')


class SmallDecks:
    def __init__(self, bigdeck):
        super().__init__()
        self.decks = [[bigdeck.deck.pop() for j in range(3)] for i in range(12)]

    def getTopCard(self, index):
        return self.decks[index][-1]

    def fillEmpty(self, index, bigdeck):
        self.decks[index]+=[bigdeck.deck.pop() for i in range(3)]

    def isPlace(self, index):
        size = len(self.decks[index])
        return size < 3 and size > 0

    def popTopCard(self, index):
        return self.decks[index].pop()

    def isSameSuit(self, index, card):
        return self.getTopCard(index).suit == card.suit

    def isLowerValue(self, index, card):
        return self.getTopCard(index).value - 1 == card.value

    def placeCard(self, index, card):
        if self.isPlace(index) and self.isSameSuit(index, card['card']) and isLowerValue(index, card['card']):
            self.decks[index].append(self.popTopCard(card['id']))


    


class Game:
    def __init__(self, master : Tk):
        self.game_frame = LabelFrame(master,  text = 'Solomon\'s Cave Solitaire', bg = 'White', font = 14, height = 720, width = 1280)
        self.game_frame.pack()
        self.left_bottom_frame = LabelFrame(self.game_frame, text = 'Game stacks', width=500, height=500, bg = 'Green')
        self.right_bottom_frame = LabelFrame(self.game_frame, text = 'Bace places', width=500, height=500, bg = 'Yellow')
        self.bigdeck_frame = LabelFrame(self.game_frame, text = "Deck - Left ", width = 200, height = 200, bg = 'Cyan')
        self.left_bottom_frame.pack(side=LEFT)
        self.right_bottom_frame.pack(side=RIGHT)
        self.bigdeck_frame.pack(side = TOP)
        self.bigdeck = BigDeck()
        self.smalldecks = SmallDecks(self.bigdeck)
        self.currentCard = {}

        self.bigdeck_frame['text'] += str(len(self.bigdeck.deck))
        self.bd_fr_label = Label(self.bigdeck_frame, text = '{0} {1}'.format(self.bigdeck.getTopCard().symbol, self.bigdeck.getTopCard().letter), fg = self.bigdeck.getTopCard().color)
        self.bd_fr_label.pack()
        self.baseplaces = BasePlaces()
        self.baceplaces_buttons = [Button(self.right_bottom_frame, text = str(i + 1), height = 2, width = 5) for i in range(8)]
        self.baceplaces_frames = [Frame(self.right_bottom_frame, bg='White', height=40, width=30, borderwidth=5) for i in range(8)]
        self.smalldecks_buttons = [Button(self.left_bottom_frame, text = str(i + 1) + ' Select', height = 2, width = 5) for i in range(12)]
        self.smalldecks_frames = [Frame(self.left_bottom_frame, bg='White', height=40, width=30, borderwidth=5) for i in range(12)]

        self.bf_text = [Label(self.baceplaces_frames[i], text = 'None') for i in range(8)]
        
        self.sf_text = [Label(self.smalldecks_frames[i], text = '{0} {1}'.format(self.smalldecks.getTopCard(i).symbol, self.smalldecks.getTopCard(i).letter), fg = self.smalldecks.getTopCard(i).color) for i in range(12)]
        
        self.selected = False

        for i in range(8):
            self.baceplaces_buttons[i].grid(row = i, column = 1)
            self.baceplaces_buttons[i].bind('<Button-1>', lambda event, idx = i: self.updateRightButtonsWhenClickedLeftRight(id = idx))
            self.baceplaces_frames[i].grid(row = i, column = 0)
            self.bf_text[i].grid(row = 0, column = 0)

        for i in range(12):
            self.sf_text[i].grid(row = 0, column = 0)
            self.smalldecks_buttons[i].grid(row = i, column = 1)
            self.smalldecks_buttons[i].bind('<Button-1>', lambda event, idx = i: self.updateLeftButtonsWhenClicked(id = idx))
            self.smalldecks_frames[i].grid(row = i, column = 0)


        for i in range(12):
            
            def on_leave(e):
                self.smalldecks_frames[i]['bg'] = 'White'
            def on_enter(e):
                self.smalldecks_frames[i]['bg'] = 'Blue'

            self.smalldecks_frames[i].bind('<Enter>', on_enter)
            self.smalldecks_frames[i].bind('<Leave>', on_leave)
        
        
        print(str(self.smalldecks.decks[0][-1]))
        # self.baseplaces.placeCard(0, self.smalldecks.decks[0].pop())

    def displayTopCardSmallDecksWhenMoved(self, index):
        self.sf_text[index]['text'] = '{0} {1}'.format(self.smalldecks.getTopCard(index).symbol, self.smalldecks.getTopCard(index).letter)
        self.sf_text[index]['fg'] = self.smalldecks.getTopCard(index).color

    def displayTopCardBacePlacesWhenMoved(self, index):
        print(self.baseplaces.places)
        print('{0} {1}'.format(self.baseplaces.getTopCard(index).symbol, self.baseplaces.getTopCard(index).letter))
        self.bf_text[index]['text'] = '{0} {1}'.format(self.baseplaces.getTopCard(index).symbol, self.baseplaces.getTopCard(index).letter)
        self.bf_text[index]['fg'] = self.baseplaces.getTopCard(index).color

    def returnCardLabel(self, card, frame):
        return Label(frame, text=u"{0}{1} ".format(card.letter, card.symbol), fg=card.color, bg="White")
        
    def returnGoalLabel(self, card, suit, frame):
        if card is not None:
            return Label(frame, text=u"{0}{1} ".format(card.letter, card.symbol), fg=card.color, bg="White")
        else:
            suitCard = Card(suit, "Blank", 0)
            return Label(frame, text=u"{0} ".format(suitCard.symbol), fg=suitCard.color, bg="White")


    def fillSmallDecks(self):
        for i in range(len(self.smalldecks.decks)):
            if len(self.smalldecks.decks[i]) == 0:
                self.smalldecks.fillEmpty(i, self.bigdeck)

    def updateLeftButtonsWhenClicked(self, id):
        print(id)
        if self.smalldecks_buttons[id]['text'] == str(id + 1) + ' Select' :
            for i in range(len(self.smalldecks_buttons)):
                if i == id:
                    self.smalldecks_buttons[id]['text'] = str(id + 1)
                else:
                    self.smalldecks_buttons[i]['text'] = str(i + 1) + ' Place'
            self.currentCard['card'] = self.smalldecks.getTopCard(id)
            self.currentCard['id'] = id
            # print(str(self.currentCard['card'])) # for debug
            self.selected = True
        elif self.smalldecks_buttons[id]['text'] == str(id + 1) or str(id + 1) + ' Place':
            for i in range(len(self.smalldecks_buttons)):
                self.smalldecks_buttons[i]['text'] = str(i + 1) + ' Select'
            if id != self.currentCard['id']:
                self.smalldecks.placeCard(id, self.currentCard)
                self.displayTopCardSmallDecksWhenMoved(self.currentCard['id'])
            self.selected = False
        self.updateRightButtonsWhenClickedLeft()

    def updateRightButtonsWhenClickedLeft(self):
        for i in range(len(self.baceplaces_buttons)):
            if self.selected:
                self.baceplaces_buttons[i]['text'] += ' Place'
            else:
                self.baceplaces_buttons[i]['text'] = str(i + 1)

    def updateRightButtonsWhenClickedLeftRight(self, id):
        print(id)
        if self.selected:
            
            for i in range(len(self.baceplaces_buttons)):
                self.baceplaces_buttons[i]['text'] = str(i+1)
            
            self.baseplaces.placeCard(id, self.currentCard, self.smalldecks)
            print(str(self.currentCard['card']))
            self.displayTopCardBacePlacesWhenMoved(id)
            self.displayTopCardSmallDecksWhenMoved(self.currentCard['id'])

            self.updateLeftButtonsWhenClickedLeftRight()
            self.selected = False

    def updateLeftButtonsWhenClickedLeftRight(self):
        for i in range(len(self.smalldecks_buttons)):
            self.smalldecks_buttons[i]['text'] = str(i + 1) + ' Select'




if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    root.mainloop()