from enum import Enum
from dataclasses import dataclass

Face = Enum('Face', ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])
Suit = Enum('Suit', ['c', 'd', 'h', 's' ])

FACE_VALUES = dict((f, i+2) for i, f in enumerate(Face))

@dataclass
class Card:
    face: Face
    suit: Suit
    face_value: int

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

def parse_hands(hands_text):
    hands = []
    for line_nr, line in enumerate(hands_text.split('\n')):
        if not line.strip():
            continue
        hands.append(parse_hand(line, line_nr=line_nr))
    return hands


def main():
    pass

if __name__ == "__main__":
    main()