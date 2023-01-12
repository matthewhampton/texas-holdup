import unittest 
from holdemup import parse_hands, parse_hand, ParseError, Card, Face, Suit

class TestHoldemUp(unittest.TestCase):

    def test_parse_hands_documented_example(self):
        hands = parse_hands("""
            Kc 9s Ks Kd 9d 3c 6d
            9c Ah Ks Kd 9d 3c 6d
            Ac Qc Ks Kd 9d 3c
            9h 5s
            4d 2d Ks Kd 9d 3c 6d
            7s Ts Ks Kd 9d        
        """)
        self.assertEqual(len(hands), 6)
        self.assertEqual(len(hands[0]), 7)
        self.assertEqual(len(hands[1]), 7)
        self.assertEqual(len(hands[2]), 6)
        self.assertEqual(len(hands[3]), 2)
        self.assertEqual(len(hands[4]), 7)
        self.assertEqual(len(hands[5]), 5)

    def test_parse_hand_valid(self):
        hand = parse_hand("Kc 9s Ks Kd 9d 3c 6d")
        self.assertEqual(len(hand), 7)
        self.assertEqual(hand[0], Card(Face.K, Suit.c, 13))
        self.assertEqual(hand[1], Card(Face['9'], Suit.s, 9))

    def test_parse_hand_invalid_card_len(self):
        self.assertRaises(ParseError, parse_hand, "Kc 9ss Ks Kd 9d 3c 6d")

    def test_parse_hand_invalid_card_face(self):
        self.assertRaises(ParseError, parse_hand, "Kc Hs Ks Kd 9d 3c 6d")

    def test_parse_hand_invalid_card_suit(self):
        self.assertRaises(ParseError, parse_hand, "Kc 9k Ks Kd 9d 3c 6d")



if __name__ == '__main__':
    unittest.main()