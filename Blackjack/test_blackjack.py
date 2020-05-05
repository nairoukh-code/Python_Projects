from unittest import TestCase

from Blackjack.blackjack import Hand, Card, Deck


class TestDeck(TestCase):
    def test_deal(self):
        player_hand = []
        deck = Deck()
        player_hand.append(deck.deal())
        player_hand.append(deck.deal())
        actual = len(player_hand)
        self.assertEqual(actual, 2)


class TestHand(TestCase):
    def test_add_card(self):
        player_hand = Hand()
        card1 = Card("Spades", "9")
        player_hand.add_card(card1)
        actual = len(player_hand.cards)
        self.assertEqual(actual, 1)

    def test_calculate_value(self):
        player_hand = Hand()
        card1 = Card("Spades", "9")
        card2 = Card("Clubs", "8")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        actual = player_hand.calculate_value()
        self.assertEqual(actual, 17)

    def test_get_value(self):
        player_hand = Hand()
        card1 = Card("Spades", "4")
        card2 = Card("Clubs", "8")
        card3 = Card("Hearts", "9")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        player_hand.add_card(card3)
        actual = player_hand.get_value()
        self.assertEqual(actual, 21)



    def test_is_busted(self):
        player_hand = Hand()
        card1 = Card("Spades", "9")
        card2 = Card("Clubs", "8")
        card3 = Card("Hearts", "10")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        player_hand.add_card(card3)
        actual = player_hand.is_busted()
        self.assertEqual(actual, True)

    def test_can_split(self):
        player_hand = Hand()
        card1 = Card("Spades", "8")
        card2 = Card("Clubs", "8")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        actual = player_hand.can_split()
        self.assertEqual(actual, True)

    def test_can_not_split(self):
        player_hand = Hand()
        card1 = Card("Spades", "8")
        card2 = Card("Clubs", "7")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        actual = player_hand.can_not_split()
        self.assertEqual(actual, True)

    def test_is_push(self):
        player_hand = Hand()
        dealer_hand = Hand(dealer=True)
        card1 = Card("Spades", "9")
        card2 = Card("Clubs", "8")
        card3 = Card("Hearts", "8")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        dealer_hand.add_card(card1)
        dealer_hand.add_card(card3)
        Actual = player_hand.is_push(dealer_hand)
        self.assertEqual(Actual, True)

    def test_player_win(self):
        player_hand = Hand()
        dealer_hand = Hand(dealer=True)
        card1 = Card("Spades", "9")
        card2 = Card("Clubs", "9")
        card3 = Card("Hearts", "8")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        dealer_hand.add_card(card1)
        dealer_hand.add_card(card3)
        Actual = player_hand.player_win(dealer_hand)
        self.assertEqual(Actual, True)

    def test_player_loss(self):
        player_hand = Hand()
        dealer_hand = Hand(dealer=True)
        card1 = Card("Spades", "9")
        card2 = Card("Clubs", "8")
        card3 = Card("Hearts", "9")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        dealer_hand.add_card(card1)
        dealer_hand.add_card(card3)
        Actual = player_hand.player_loss(dealer_hand)
        self.assertEqual(Actual, True)

    def test_check_for_blackjack(self):
        player_hand = Hand()
        card1 = Card("Spades", "10")
        card2 = Card("Clubs", "A")
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        actual = player_hand.can_not_split()
        self.assertEqual(actual, True)