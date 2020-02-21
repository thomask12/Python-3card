import random
import operator
import sys
import os

class Player(object):
    #Add strategy with optimal, suboptimal and all that which players can access to find "best" card
    def __init__(self, id):
        # Unique id for each player
        self.id = id
        # Cards that are faced down at the beginning of the game
        self.bottom = []
        # Cards selected to be the best later in the game. Placed face up on the bottom cards
        self.top = []
        # The players hand. Must always be at least 3 cards in length unless the deck is == 0
        self.hand = []

#Determines value of actual card
def card_value(card):
    #This is how you find the correct value of cards accounting for suit changes: card_value(players[0].hand[0] % 13)
    new_card = card % 13
    # 14 = Ace
    if new_card == 1:
        return 14
    # 2 = 2 *reset*
    elif new_card == 2:
        return 15
    # 10 = 10 *blows up*
    elif new_card == 10:
        return 16
    # 13 = King
    elif new_card == 0:
        return 13
    else:
        return new_card

def card_value_deck():
    d = list(range(1,53))
    random.shuffle(d)
    pack = d
    d[:] = [card_value(card) for card in d]
    return pack

def draw(id):
    #Checks to see if a player can draw a new card
    while len(players[id].hand) < 3:
        #Draws from deck if the deck has cards remaining
        if len(deck) > 0:
            players[id].hand.append(deck.pop())
        elif len(players[id].hand) == 0:
            #Player takes their top hand
            if len(players[id].top) > 0:
                for x in  players[id].top:
                    players[id].hand.append(x)
                players[id].top.clear()
                flips.append(tuple((turns, id + 1, "Top", players[id].hand)))
                print(flips[len(flips)-1])
            #Player flips one card at a time from their face down cards
            elif len(players[id].bottom) != 0:
                players[id].hand.append(players[id].bottom.pop())
                flips.append(tuple((turns, id + 1, "Flip", players[id].hand[0])))
                print(flips[len(flips)-1])
            #Exits when a player wins the game
            else:
                print("Player ", id + 1, " won the game.")
                output_string = "Player " + str(id) + " won the game."
                exit(0)
            break
        else:
            break

#Determines how many cards of the same value a player has in their hand currently
def multiple_card(id, card):
    number_of_cards = 0
    for x in players[id].hand:
        if x == card:
            number_of_cards += 1
    return number_of_cards

#Determines how many cards of the same value have already been played
def in_row(card):
    in_row = 0
    for x in range(to_pick):
        if card == 6 and in_row == 3:
            print("The Number of the BEAST")
        if out_play[len(out_play)-x-1][3] == card:
            in_row += 1
        else:
            break
    return in_row

#Determines if 4 cards are in a row to blow up
def remove_row(id, index):
    if multiple_card(id, index) == 4 or in_row(index) + multiple_card(id, index) == 4:
        return True
    return False

#Finds the lowest possible card that can be played
def lowest_playable(id):
    #highest card in player's hand
    highest = max(players[id].hand)
    #lowest card in player's hand
    player_min = min(players[id].hand)
    last_index = out_play[len(out_play)-1]
    #Value of the last card played
    last = last_index[3]
    #If the pile was picked up by the last player
    if last == -1:
        put(id, player_min)
        return True
    if highest >= last:
        for card in players[id].hand:
            if card >= last and card < highest:
                highest = card
        put(id, highest)
        return True
    else:
        pick(id)
        return False

def pick(id):
    global to_pick
    global turns
    turns += 1
    out_play.append(tuple((turns, id + 1, "Pick", -1)))
    x = 0
    while x < to_pick:
        new_tuple = out_play[len(out_play)-2-x]
        players[id].hand.append(new_tuple[3])
        x += 1
    print(out_play[len(out_play)-1])
    to_pick = 0

def _two_(id):
    global turns
    global to_pick
    out_play.append(tuple((turns, id + 1, "Put", 15)))
    to_pick += 1
    print(out_play[len(out_play)-1])
    players[id].hand.remove(15)
    draw(id)
    newmin = min(players[id].hand)
    put(id, newmin)

def _ten_(id):
    global turns
    global to_pick
    out_play.append(tuple((turns, id + 1, "Boom bebe", 16)))
    to_pick = 0
    print(out_play[len(out_play)-1])
    players[id].hand.remove(16)
    draw(id)
    newmin = min(players[id].hand)
    put(id, newmin)

def _four_ofa_kind_(id, card, multi):
    global turns
    global to_pick
    for x in range(multi):
        out_play.append(tuple((turns, id + 1, "Put", card)))
        print(out_play[len(out_play)-1])
        players[id].hand.remove(card)
    out_play.append(tuple((turns, id + 1, "Boom bebe", card)))
    to_pick = 0
    print(out_play[len(out_play)-1])
    draw(id)
    newmin = min(players[id].hand)
    put(id, newmin)

def put(id, card):
    global turns
    global to_pick
    draw(id)
    turns += 1
    to_remove = multiple_card(id, card)
    if card == 15:
        _two_(id)
    elif card == 16:
        _ten_(id)
    elif to_remove == 4 or remove_row(id, card):
        _four_ofa_kind_(id, card, to_remove)
    else:
        for x in range(to_remove):
            out_play.append(tuple((turns, id + 1, "Put", card)))
            to_pick += 1
            print(out_play[len(out_play)-1])
            players[id].hand.remove(card)
    draw(id)

def begin_game():
    min_ray = []
    for player in players:
        tmp = min(player.hand)
        min_ray.append(card_value(tmp))
    put(min_ray.index(min(min_ray)), min(min_ray))
    draw(min_ray.index(min(min_ray)))
    return min_ray.index(min(min_ray))

def setup_game(num_players):
    for play in range(num_players):
        players.append(Player(play))

    for card in range(num_players * 3):
        #Add 3 cards to each bottom
        players[card % num_players].bottom.append(deck.pop())

    for card in range(num_players * 6):
        #Add 6 cards to each hand
        players[card % num_players].hand.append(deck.pop())
    for card in range(num_players * 3):
        highest = max(players[card % num_players].hand)
        players[card % num_players].top.append(highest)
        players[card % num_players].hand.remove(highest)
    play_game(begin_game(), num_players)

def play_game(playing, num):
    next_player = playing
    while True:
        next_player = (next_player + 1) % num
        lowest_playable(next_player)

deck = card_value_deck()
#The "best" way to play (subject to debate)
optimal = [3,4,5,6,7,8,9,11,12,13,1,2,10]
turns = 0
to_pick = 0
players = list()
#Tuple with (turn number, player number, action[pick_up, put, blow up], card played)
out_play = list()
flips = list()

if int(sys.argv[1]) < 5:
    i = int(sys.argv[1])
else:
    i = 2
setup_game(i)
