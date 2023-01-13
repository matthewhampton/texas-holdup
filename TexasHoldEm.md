## Problem description

You work for a cable network; specifically, you are the resident hacker
for a Texas Hold'Em Championship show.

The show's producer has come to you for a favor. It seems the
play-by-play announcers just can't think very fast. All beauty, no
brains. The announcers could certainly flap their jaws well enough, if
they just knew what hands the players were holding and which hand won
the round. Since this is live TV, they need those answers quick. Time to
step up to the plate. Bob, the producer, explains what you need to do.

BOB: Each player's cards for the round will be on a separate line of the
input. Each card is a pair of characters, the first character represents
the face, the second is the suit. Cards are separated by exactly one
space. Here's a sample hand.

      Kc 9s Ks Kd 9d 3c 6d
      9c Ah Ks Kd 9d 3c 6d
      Ac Qc Ks Kd 9d 3c
      9h 5s
      4d 2d Ks Kd 9d 3c 6d
      7s Ts Ks Kd 9d

YOU: Okay, I was going ask what character to use for 10, but I guess 'T'
is it. And 'c', 'd', 'h' and 's' for the suits, makes sense. Why aren't
seven cards listed for every player?

BOB: Well, if a player folds, only his hole cards and the community
cards he's seen so far are shown.

YOU: Right. And why did the fifth player play with a 4 and 2? They're
suited, but geez, talk about risk...

BOB: Stay on topic. Now, the end result of your code should generate
output that looks like this:

      Kc 9s Ks Kd 9d 3c 6d Full House (winner)
      9c Ah Ks Kd 9d 3c 6d Two Pair
      Ac Qc Ks Kd 9d 3c 
      9h 5s 
      4d 2d Ks Kd 9d 3c 6d Flush
      7s Ts Ks Kd 9d 

YOU: Okay, so I repeat the cards, list the rank or nothing if the player
folded, and the word "winner" in parenthesis next to the winning hand.
Do you want the cards rearranged at all?

BOB: Hmmm... we can get by without it, but if you have the time, do it.
Don't bother for folded hands, but for ranked hands, move the cards used
to the front of the line, sorted by face. Kickers follow that, and the
two unused cards go at the end, just before the rank is listed.

YOU: Sounds good. One other thing, I need to brush up on the hand ranks.
You have any good references for Texas Hold'Em?

BOB: Yeah, do an internet search on Poker Hand Rankings. And if you need
it, the Rules of Texas Hold'Em. While ranking, don't forget the kicker,
the next highest card in their hand if player's are tied. And of course,
if -- even after the kicker -- player's are still tied, put "(winner)"
on each appropriate line of output.

YOU: Ok. I still don't understand one thing...

BOB: What's that?

YOU: Why he stayed in with only the 4 and 2 of diamonds? That's just...

BOB: Hey! Show's on in ten minutes! Get to work!

# Hands

These are shown lowest to highest:

1. High card: Simple value of the card. Lowest: 2 – Highest: Ace 
2. Pair: Two cards with the same value	
3. Two pairs: Two times two cards with the same value	
4. Three of a kind: Three cards with the same value	
5. Straight: Sequence of 5 cards in increasing value (Ace can precede 2 and follow up King)
6. Flush: 5 cards of the same suit
7. Full house: Combination of three of a kind and a pair	
8. Four of a kind: Four cards of the same value	
9. Straight flush: Straight of the same suit

# Hand Rankings

Standard Poker Hand Ranking
There are 52 cards in the pack, and the ranking of the individual cards, from high to low, is ace, king, queen, jack, 10, 9, 8, 7, 6, 5, 4, 3, 2. There is no ranking between the suits – so for example the king of hearts and the king of spades are equal.

A poker hand consists of five cards. The categories of hand, from highest to lowest, are listed below. Any hand in a higher category beats any hand in a lower category (so for example any three of a kind beats any two pairs). Between hands in the same category the rank of the individual cards decides which is better, as described in more detail below.

In games where a player has more than five cards and selects five to form a poker hand, the remaining cards do not play any part in the ranking. Poker ranks are always based on five cards only.

S=Spades C= Clubs H= Hearts D=Diamonds

1. Royal Flush
This is the highest poker hand. It consists of ace, king, queen, jack, ten, all in the same suit. If there are 2 royal flushes in the running for High hand, then it's a draw.

2. Straight Flush
Five cards of the same suit in sequence – such as CJ-C10-C9-C8-C7. Between two straight flushes, the one containing the higher top card is higher. An ace can be counted as low, so H5-H4-H3-H2-HA is a straight flush, but its top card is the five, not the ace, so it is the lowest type of straight flush. The cards cannot “turn the corner”:D4-D3-D2-DA-DK is not valid.

3. Four of a kind  
Four cards of the same rank – such as four queens. The fifth card can be anything. This combination is sometimes known as “quads”, and in some parts of Europe it is called a “poker”, though this term for it is unknown in English. Between two fours of a kind, the one with the higher set of four cards is higher – so 3-3-3-3-A is beaten by 4-4-4-4-2. In Texas Hold’em, if the board shows “quads”, then the player with the higher fifth card is the winner.

4. Full House
This consists of three cards of one rank and two cards of another rank – for example three sevens and two tens (colloquially known as “sevens full” or more specifically “sevens on tens”). When comparing full houses, the rank of the three cards determines which is higher. For example 9-9-9-4-4 beats 8-8-8-A-A. If the threes of a kind were equal, the rank of the pairs would decide.

5. Flush
Five cards of the same suit. When comparing two flushes, the highest card determines which is higher. If the highest cards are equal then the second highest card is compared; if those are equal too, then the third highest card, and so on. For example SK-SJ-S9-S3-S2 beats DK-DJ-D7-D6-D5 because the nine beats the seven.

6. Straight
Five cards of mixed suits in sequence – for example Qs Jd Th 9s 8c. When comparing two sequences, the one with the higher ranking top card is better. Ace can count high or low in a straight, but not both at once, so As Kd Qd Js Th and 5h 4s 3s 2h Ad are valid straights, but 2d As Kc Qc Jh is not. 5-4-3-2-A is the lowest kind of straight, the top card being the five.

7. Three of a Kind
Three cards of the same rank plus two other cards. This combination is also known as Triplets or Trips. When comparing two threes of a kind the hand in which the three equal cards are of higher rank is better. So for example 5-5-5-3-2 beats 4-4-4-K-Q. If you have to compare two threes of a kind where the sets of three are of equal rank, then the higher of the two remaining cards in each hand are compared, and if those are equal, the lower odd card is compared.

8. Two Pair
A pair is two cards of equal rank. In a hand with two pairs, the two pairs are of different ranks (otherwise you would have four of a kind), and there is an odd card to make the hand up to five cards. When comparing hands with two pairs, the hand with the highest pair wins, irrespective of the rank of the other cards – so J-J-2-2-4 beats 10-10-9-9-8 because the jacks beat the tens. If the higher pairs are equal, the lower pairs are compared, so that for example 8-8-6-6-3 beats 8-8-5-5-K. Finally, if both pairs are the same, the odd cards are compared, so Q-Q-5-5-8 beats Q-Q-5-5-4.

9. Pair
A hand with two cards of equal rank and three other cards which do not match these or each other. When comparing two such hands, the hand with the higher pair is better – so for example 6-6-4-3-2 beats 5-5-A-K-Q. If the pairs are equal, compare the highest ranking odd cards from each hand; if these are equal compare the second highest odd card, and if these are equal too compare the lowest odd cards. So J-J-A-9-3 beats J-J-A-8-7 because the 9 beats the 8.

10. High Card
Five cards which do not form any of the combinations listed above. When comparing two such hands, the one with the better highest card wins. If the highest cards are equal the second cards are compared; if they are equal too the third cards are compared, and so on. So A-J-9-5-3 beats A-10-9-6-4 because the jack beats the ten.

See <https://www.southeastholdem.com/about/rules/hand-rankings/> 

# Links

See <https://codingdojo.org/kata/TexasHoldEm/> or <https://gitlab.com/codingdojo-org/codingdojo.org/-/blob/master/content/kata/TexasHoldEm.md>

See <https://www.pokernews.com/poker-hands.htm> for a list of poker hands with an explanation of how to figure out who wins when comparing the same hand but different values (e.g. when it comes to full houses, the higher three of a kind determines which hand wins, so in this case "kings full" would beat "fives full" )

See <https://www.google.com/search?q=what+is+the+high+card+for+a+straight+that+starts+with+an+ace>: Ace-to-five makes the lowest possible straight, while ten-to-ace is the highest possible straight. All other straights in between the low and high ends use the highest-ranking card to determine the hand's strength.

See <https://www.southeastholdem.com/about/rules/hand-rankings/> for more with text-based examples. Nice to unit tests.

See <https://www.google.com/search?q=how+do+you+compare+two+flushes+in+poker>: When comparing two flushes, the highest card determines which is higher. If the highest cards are equal then the second highest card is compared; if those are equal too, then the third highest card, and so on. For example SK-SJ-S9-S3-S2 beats DK-DJ-D7-D6-D5 because the nine beats the seven.