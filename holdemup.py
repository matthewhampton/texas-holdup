from enum import Enum
from dataclasses import dataclass
import sys

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

def winner(hand1, hand2, none_for_draw=False):
    if hand1.hand_rank > hand2.hand_rank:
        return hand1
    if hand1.hand_rank < hand2.hand_rank:
        return hand2

    if hand1.hand[0].face_value > hand2.hand[0].face_value:
        return hand1
    if hand1.hand[0].face_value < hand2.hand[0].face_value:
        return hand2

    if hand1.name == HandName['Full House']:
        if hand1.hand[3].face_value > hand2.hand[3].face_value:
            return hand1
        if hand1.hand[3].face_value < hand2.hand[3].face_value:
            return hand2
    elif hand1.name == HandName['Two Pair']:
        if hand1.hand[2].face_value > hand2.hand[2].face_value:
            return hand1
        if hand1.hand[2].face_value < hand2.hand[2].face_value:
            return hand2

    for c1, c2 in zip(hand1.kickers, hand2.kickers):
        if c1.face_value > c2.face_value:
            return hand1
        if c1.face_value < c2.face_value:
            return hand2

    if none_for_draw:
        return None
    else:
        return hand1 

def new_hand(hand, full_sorted_hand, handname_text):
    handname = HandName[handname_text]
    rest = list(filter(lambda c: c not in hand, full_sorted_hand))
    return Hand(hand, rest[:5-len(hand)], rest[5-len(hand):], handname, HAND_VALUES[handname])

def label_hand(hand):
    
    sorted_hand = sorted(hand, key=lambda c: -c.face_value)

    best_hand = new_hand([sorted_hand[0]], sorted_hand, 'High Card')

    for suit in Suit:
        cards_in_suit = list(filter(lambda c: c.suit == suit, sorted_hand))
    
        straight_flush = find_straight(cards_in_suit)
        if straight_flush:
            best_hand = winner(best_hand, new_hand(straight_flush, sorted_hand, "Royal Flush" if straight_flush[0].face == Face.A else "Straight Flush"))
        elif len(cards_in_suit)>=5:
            best_hand = winner(best_hand, new_hand(cards_in_suit[:5], sorted_hand, "Flush"))

    of_a_kinds = _find_of_a_kinds(sorted_hand)

    if of_a_kinds[4]:
        best_hand = winner(best_hand, new_hand(of_a_kinds[4][0], sorted_hand, "Four of a Kind"))
    elif of_a_kinds[3]:
        if len(of_a_kinds[3])>1:
            best_hand = winner(best_hand, new_hand(of_a_kinds[3][0]+of_a_kinds[3][1][:2], sorted_hand, "Full House"))
        if of_a_kinds[2]:
            best_hand = winner(best_hand, new_hand(of_a_kinds[3][0]+of_a_kinds[2][0], sorted_hand, "Full House"))

        best_hand = winner(best_hand, new_hand(of_a_kinds[3][0], sorted_hand, "Three of a Kind"))
    elif len(of_a_kinds[2])>1:
        best_hand = winner(best_hand, new_hand(of_a_kinds[2][0]+of_a_kinds[2][1], sorted_hand, "Two Pair"))
    elif of_a_kinds[2]:
        best_hand = winner(best_hand, new_hand(of_a_kinds[2][0], sorted_hand, "Pair"))

    straight = find_straight(sorted_hand)
    if straight:
        best_hand = winner(best_hand, new_hand(straight, sorted_hand, "Straight"))

    return best_hand

def find_of_a_kinds(hand):
    sorted_hand = sorted(hand, key=lambda c: -c.face_value)
    return _find_of_a_kinds(sorted_hand)

def _find_of_a_kinds(sorted_hand):

    of_a_kinds = {
        2: [],
        3: [],
        4: [],
    }
    current_of_a_kind = []
    for card in sorted_hand:
        if current_of_a_kind and current_of_a_kind[0].face == card.face:
            current_of_a_kind.append(card)
        else:
            if len(current_of_a_kind)>1:
                of_a_kinds[len(current_of_a_kind)].append(current_of_a_kind)
            current_of_a_kind = [card]
    if len(current_of_a_kind)>1:
        of_a_kinds[len(current_of_a_kind)].append(current_of_a_kind)
        
    return of_a_kinds
        

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

def process_hands_text(hands_text):
    hands = parse_hands(hands_text)
    output_text = ""
    for i, hand in enumerate(hands):
        
        if len(hand) == 7:
            hand = label_hand(hand)
            is_winner = True
            for j, other_hand in enumerate(hands):
                if i == j:
                    continue
                if len(other_hand) < 7:
                    continue
                other_hand = label_hand(other_hand)
                w = winner(other_hand, hand, none_for_draw=True)
                if w is other_hand:
                    is_winner = False
                    break
            output_text += hand.dump() + (" (winner)" if is_winner else "") + "\n"
        else:
            output_text += dump_hand(hand) + "\n"

    return output_text

def process_hands_text_and_print(hands_text):
    print("-------------")
    print(process_hands_text(hands_text))

def main():

    hands_text = ""
    for line in sys.stdin:
        if not line.strip():
            if hands_text:
                process_hands_text_and_print(hands_text)
                hands_text = ""
        else:
            hands_text += line

    if hands_text:
        process_hands_text_and_print(hands_text)

if __name__ == "__main__":
    main()