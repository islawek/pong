# Implementation of Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


in_play = False
outcome = ""
wins, losses = 0, 0

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}



class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
        
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        return_list = ""
        for i in self.cards:
            return_list = return_list +" "+str(i.suit + i.rank)
        return str(return_list)

    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        has_ace = False
        for i in self.cards:
            value += VALUES[i.rank]
            if i.rank == "A":
                has_ace = True
        if has_ace and value + 10 <= 21:
            value += 10
        return value
   
    def draw(self, canvas, pos):
        for i in self.cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(i.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(i.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            pos[0] += CARD_SIZE[0]

        

class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        return_list = ""
        for i in self.cards:
            return_list = return_list +" "+str(i.suit + i.rank)
        return str(return_list)


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, losses
    if in_play:
        outcome = "You lose. Hit or stand?"
        losses += 1
    else: 
        outcome = "Hit or stand?"
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    in_play = True

def hit():
    global in_play, player, deck, outcome, losses
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            if player.get_value() > 21:
                outcome = "You have busted. New deal?"
                in_play = False
                losses += 1
                
def stand():
    global player, dealer, deck, in_play, outcome, losses, wins
    if in_play:
        if player.get_value() > 21:
            outcome = "You have busted, dealer wins. New deal?"
        else:
            while dealer.get_value() <= 17:
                dealer.add_card(deck.deal_card())
            if dealer.get_value() > 21:
                outcome = "Dealer has busted, you win. New deal?"
                wins += 1
            elif dealer.get_value() >= player.get_value():
                outcome = "You lose. New deal?"
                losses += 1
            else:
                outcome = "You win. New deal?"
                wins += 1
        in_play = False
        

# draw handler    
def draw(canvas):
    global dealer, player
    dealer.draw(canvas, [10, 100])
    player.draw(canvas, [10, 300])
    canvas.draw_text("Blackjack", [400, 40], 30, "Maroon", "monospace")
    canvas.draw_text("Dealer",[10, 90], 20, "Black")
    canvas.draw_text("Player", [10, 290], 20, "Black")
    canvas.draw_text(outcome, [200, 290], 30, "Maroon")
    canvas.draw_text("Wins: " + str(wins), [800, 60], 20, "Black")
    canvas.draw_text("Losses: " + str(losses),[800, 85], 20, "Black")
    if in_play:
        canvas.draw_image(card_back, [CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]], CARD_BACK_SIZE, [10 + CARD_BACK_CENTER[0], 100 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 900, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()