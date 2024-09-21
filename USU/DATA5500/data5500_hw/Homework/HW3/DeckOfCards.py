import random

# creating blueprint for each individual card
class Card():
    def __init__(self, suit, face, value):
        self.suit = suit
        self.face = face
        self.val = value


    # how cards will be read
    def __str__(self):
        return self.face + " of " + self.suit + ", value: " + str(self.val)
        # ex: 2 of Clubs, value: 2


# combining cards to make a deck
class DeckOfCards():
    def __init__(self):
        self.deck = []
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        self.faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.play_idx = 0
        
        for suit in self.suits:
            i = 0
            for i in range(len(self.faces)):
                self.deck.append(Card(suit, self.faces[i], self.values[i]))
                

    # creating card shuffling        
    def shuffle_deck(self):
        random.shuffle(self.deck)
        self.play_idx = 0
        
    def print_deck(self):
        for card in self.deck:
            print(card.face, "of", card.suit, end=", ")
        print("---")
        
    def get_card(self):
        self.play_idx += 1
        return self.deck[self.play_idx - 1]