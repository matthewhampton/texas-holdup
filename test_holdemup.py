import unittest 
from holdemup import parse_hands, parse_hand, ParseError, Card, Face, Suit, find_straight, dump_hand, label_hand

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

    def test_find_straight(self):
        self.assertEqual(dump_hand(find_straight(parse_hand("Qs Jd Th 9s 8c"))), "Qs Jd Th 9s 8c")
        self.assertEqual(dump_hand(find_straight(parse_hand("Ks Jd Th 9s 8c"))), "") #Not a straight
        self.assertEqual(dump_hand(find_straight(parse_hand("Qs Jd Th 9s 8c As"))), "Qs Jd Th 9s 8c") #Extras don't matter
        self.assertEqual(dump_hand(find_straight(parse_hand("Qs Jd Th 9s 8c 7s"))), "Qs Jd Th 9s 8c") #Choose the higher valued one
        self.assertEqual(dump_hand(find_straight(parse_hand("8c Jd Th Qs 9s"))), "Qs Jd Th 9s 8c") #Order doesn't matter
        self.assertEqual(dump_hand(find_straight(parse_hand("Qs Jd Th 9s"))), "") #You need at least five cards for it to be a straight
        self.assertEqual(dump_hand(find_straight(parse_hand("As Kd Qd Js Th"))), "As Kd Qd Js Th") #Ace high
        self.assertEqual(dump_hand(find_straight(parse_hand("5h 4s 3s 2h Ad"))), "5h 4s 3s 2h Ad") #Ace low
        self.assertEqual(dump_hand(find_straight(parse_hand("2d As Kc Qc Jh"))), "") #But not in the middle

    def test_label_hand_royal_flush(self):
        self.assertEqual(label_hand(parse_hand("As Ks Qs Js Ts 9s 8c")).dump(), "As Ks Qs Js Ts 9s 8c Royal Flush")

    def test_label_hand_straight_flush(self):
        self.assertEqual(label_hand(parse_hand("Ad Ks Qs Js Ts 9s 8c")).dump(), "Ks Qs Js Ts 9s Ad 8c Straight Flush")


if __name__ == '__main__':
    unittest.main()