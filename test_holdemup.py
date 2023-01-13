import unittest 
from holdemup import parse_hands, parse_hand, ParseError, Card, Face, Suit, find_straight, dump_hand, label_hand, find_of_a_kinds

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

    def test_find_of_a_kinds(self):
        of_a_kinds = find_of_a_kinds(parse_hand("Qs 8c Jd Jh 9s 8h"))
        self.assertEqual(len(of_a_kinds[2]), 2)
        self.assertEqual(len(of_a_kinds[3]), 0)
        self.assertEqual(len(of_a_kinds[4]), 0)

        of_a_kinds = find_of_a_kinds(parse_hand("Qs 8c Jd 8d Jh 9s 8h"))
        self.assertEqual(len(of_a_kinds[2]), 1)
        self.assertEqual(len(of_a_kinds[3]), 1)
        self.assertEqual(len(of_a_kinds[4]), 0)

        of_a_kinds = find_of_a_kinds(parse_hand("8s Qs 8c Jd 8d Jh 9s 8h"))
        self.assertEqual(len(of_a_kinds[2]), 1)
        self.assertEqual(len(of_a_kinds[3]), 0)
        self.assertEqual(len(of_a_kinds[4]), 1)


    def test_label_hand_royal_flush(self):
        self.assertEqual(label_hand(parse_hand("As Ks Qs Js Ts 9s 8c")).dump(), "As Ks Qs Js Ts 9s 8c Royal Flush")

    def test_label_hand_straight_flush(self):
        self.assertEqual(label_hand(parse_hand("Ad Ks Qs Js Ts 9s 8c")).dump(), "Ks Qs Js Ts 9s Ad 8c Straight Flush")

    def test_label_hand_four_of_a_kind(self):
        self.assertEqual(label_hand(parse_hand("3s 3c 3h 3d As")).dump(), "3s 3c 3h 3d As Four of a Kind")
        self.assertEqual(label_hand(parse_hand("4s 4c 4h 4d 2s")).dump(), "4s 4c 4h 4d 2s Four of a Kind")

    def test_label_hand_full_house(self):
        self.assertEqual(label_hand(parse_hand("9s 9c 9h 4s 4c")).dump(), "9s 9c 9h 4s 4c Full House")
        self.assertEqual(label_hand(parse_hand("8s 8c 8h As Ac")).dump(), "8s 8c 8h As Ac Full House")
        self.assertEqual(label_hand(parse_hand("8s 8c 8h As Ac Ad")).dump(), "As Ac Ad 8s 8c 8h Full House")

    def test_label_hand_flush(self):
        self.assertEqual(label_hand(parse_hand("As Ks 2s Js Ts 9d 8c")).dump(), "As Ks Js Ts 2s 9d 8c Flush")

    def test_label_hand_straight(self):
        self.assertEqual(label_hand(parse_hand("Qs Jd Th 9s 8c")).dump(), "Qs Jd Th 9s 8c Straight")
        self.assertEqual(label_hand(parse_hand("As Kd Qd Js Th")).dump(), "As Kd Qd Js Th Straight")
        self.assertEqual(label_hand(parse_hand("5h 4s 3s 2h Ad")).dump(), "5h 4s 3s 2h Ad Straight")
        self.assertEqual(label_hand(parse_hand("Ad Ks Qs Jd Ts 9s 8c")).dump(), "Ad Ks Qs Jd Ts 9s 8c Straight")

    def test_label_hand_three_of_a_kind(self):
        self.assertEqual(label_hand(parse_hand("5s 5c 5h 3s 2c")).dump(), "5s 5c 5h 3s 2c Three of a Kind")
        self.assertEqual(label_hand(parse_hand("4s 4c 4h Ks Qc")).dump(), "4s 4c 4h Ks Qc Three of a Kind")

    def test_label_hand_two_pair(self):
        self.assertEqual(label_hand(parse_hand("Js Jc 2s 2c 4s")).dump(), "Js Jc 2s 2c 4s Two Pair")
        self.assertEqual(label_hand(parse_hand("Ts Tc 9s 9c 8s")).dump(), "Ts Tc 9s 9c 8s Two Pair")
        self.assertEqual(label_hand(parse_hand("8s 8c 6s 6c 3s")).dump(), "8s 8c 6s 6c 3s Two Pair")
        self.assertEqual(label_hand(parse_hand("8s 8c 5s 5c Ks")).dump(), "8s 8c 5s 5c Ks Two Pair")
        self.assertEqual(label_hand(parse_hand("Qs Qc 5s 5c 8s")).dump(), "Qs Qc 5s 5c 8s Two Pair")
        self.assertEqual(label_hand(parse_hand("Qs Qc 5s 5c 4s")).dump(), "Qs Qc 5s 5c 4s Two Pair")

    def test_label_hand_pair(self):
        self.assertEqual(label_hand(parse_hand("6s 6c 4h 3d 2s")).dump(), "6s 6c 4h 3d 2s Pair")
        self.assertEqual(label_hand(parse_hand("5s 5c Ah Kd Qs")).dump(), "5s 5c Ah Kd Qs Pair")
        self.assertEqual(label_hand(parse_hand("Js Jc Ah 9d 3s")).dump(), "Js Jc Ah 9d 3s Pair")
        self.assertEqual(label_hand(parse_hand("Js Jc Ah 8d 7s")).dump(), "Js Jc Ah 8d 7s Pair")

    def test_label_hand_high_card(self):
        self.assertEqual(label_hand(parse_hand("As Jc 9h 5d 3s")).dump(), "As Jc 9h 5d 3s High Card")
        self.assertEqual(label_hand(parse_hand("As Td 9h 6c 4s")).dump(), "As Td 9h 6c 4s High Card")

if __name__ == '__main__':
    unittest.main()