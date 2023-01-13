from enum import Enum
from dataclasses import dataclass

HandName = Enum('HandName', ['Royal Flush', 'Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card'])
Face = Enum('Face', ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
Suit = Enum('Suit', ['c', 'd', 'h', 's' ])

FACE_VALUES = dict((f, i+2) for i, f in enumerate(Face))
HAND_VALUES = dict((f, i+1) for i, f in enumerate(reversed(HandName)))

@dataclass
class Card:
    face: Face
    suit: Suit
    face_value: int

@dataclass
class Hand:
    hand: list
    kickers: list
    unused: list
    name: HandName
    hand_rank: int

    def dump(self) -> str:
        return " ".join(filter(None, (dump_hand(self.hand), dump_hand(self.kickers), dump_hand(self.unused), self.name.name)))

class ParseError(Exception):
    pass

def raise_parse_error(line_nr, line, message):
    if line_nr is None:
        raise ParseError("Parsing error in line [%s]: %s" % (line, message))
    else:
        raise ParseError("Parsing error at line %d [%s]: %s" % (line_nr, line, message))

def parse_hand(hand_text, line_nr=None):
    hand = []
    for c in filter(None, hand_text.split()):
        if len(c) != 2:
            raise_parse_error(line_nr, hand_text, "'%s' is not a valid card" % c)
        try:
            face = Face[c[0].upper()]
        except KeyError:
            raise_parse_error(line_nr, hand_text, "'%s' is not a valid face value" % c[0])

        try:
            suit = Suit[c[1].lower()]
        except KeyError:
            raise_parse_error(line_nr, hand_text, "'%s' is not a valid suit value" % c[1])

        hand.append(Card(face, suit, FACE_VALUES[face]))

    return hand

def dump_hand(hand):
    return " ".join("%s%s" % (c.face.name, c.suit.name) for c in hand) if hand else ""

def parse_hands(hands_text):
    hands = []
    for line_nr, line in enumerate(hands_text.split('\n')):
        if not line.strip():
            continue
        hands.append(parse_hand(line, line_nr=line_nr))
    return hands

def winner(hand1, hand2):
    if hand1.hand_rank > hand2.hand_rank:
        return hand1
    if hand1.hand_rank < hand2.hand_rank:
        return hand2
    if hand1.hand[0].face_value > hand2.hand[0].face_value:
        return hand1
    if hand1.hand[0].face_value < hand2.hand[0].face_value:
        return hand2
    return hand1 #TODO: kicker

def new_hand(hand, full_sorted_hand, handname_text):
    handname = HandName[handname_text]
    rest = list(filter(lambda c: c not in hand, full_sorted_hand))
    return Hand(hand, rest[:5-len(hand)], rest[5-len(hand):], handname, HAND_VALUES[handname])

def label_hand(hand):
    
    sorted_hand = sorted(hand, key=lambda c: -c.face_value)

    best_hand = new_hand([sorted_hand[0]], sorted_hand, 'High Card')

    cards_in_suit = {}
    for suit in Suit:
        cards_in_suit[suit] = list(filter(lambda c: c.suit == suit, sorted_hand))
    
        straight_flush = find_straight(cards_in_suit[suit])
        if straight_flush:
            best_hand = winner(best_hand, new_hand(straight_flush, sorted_hand, "Royal Flush" if straight_flush[0].face == Face.A else "Straight Flush"))

    return best_hand
        

def find_straight(hand):
    if not hand:
        return

    deduped_hand = []
    for c in sorted(hand, key=lambda c: -c.face_value):
        if deduped_hand and deduped_hand[-1].face_value == c.face_value:
            continue
        deduped_hand.append(c)

    straight = _find_straight_in_deduped_hand(deduped_hand)
    if straight:
        return straight

    if deduped_hand[0].face == Face.A:
        #Now try with the Ace low
        deduped_hand.append(deduped_hand.pop(0))
        straight = _find_straight_in_deduped_hand(deduped_hand)
        if straight:
            return straight
       
def _find_straight_in_deduped_hand(deduped_hand):
    for i in range(len(deduped_hand)-4):
        potential_straight = deduped_hand[i:i+5]
        if _is_straight(potential_straight):
            return potential_straight
    return None

def _is_straight(potential_straight):
    last_c = None
    for c in potential_straight:
        if last_c and last_c.face_value-1 != c.face_value:
            if not (last_c.face == Face['2'] and c.face == Face.A):
                return False
        last_c = c
    return True


def main():
    pass

if __name__ == "__main__":
    main()