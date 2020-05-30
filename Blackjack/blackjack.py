# took some ideas from this source ( https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b  )
import random
from enum import Enum
from time import  time

class Game_Status(Enum):
    WIN = 1
    LOSE = 2
    PUSH = 3


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return " of ".join((self.value, self.suit))


class Deck:
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts",
                                           "Diamonds"] for v in ["A", "2", "3", "4", "5", "6",
                                                                 "7", "8", "9", "10", "10", "10", "10"]] * 6
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)
        else:
            self.__init__()
            return self.cards.pop(0)


class Hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        number_of_aces = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    number_of_aces += 1
                    self.value += 11
                else:
                    self.value += 10

        while 12 > number_of_aces > 0 and self.value > 21:
            self.value -= 10
            number_of_aces -= 1

        return self.value

    def get_value(self):
        self.calculate_value()
        return self.value

    def display(self):
        if self.dealer:
            print("hidden")
            print(self.cards[1])
        else:
            for card in self.cards:
                print(card)
            print("Value:", self.get_value())

    def final_display(self):
        for card in self.cards:
            print(card)
        print("Value:", self.get_value())

    def is_busted(self):  # check if value is > 21
        return self.get_value() > 21

    def can_split(self):
        return self.cards[0].value == self.cards[1].value

    def can_not_split(self):
        return self.cards[0].value != self.cards[1].value

    def is_push(self, other):
        return self.get_value() == other.get_value()

    def player_win(self, other):
        return self.get_value() > other.get_value()

    def player_loss(self, other):
        return self.get_value() < other.get_value()

    def check_for_blackjack(self):
        return self.get_value() == 21 and len(self.cards) == 2


class Game:

    def print_status(self, status: Game_Status):
        if status == Game_Status.WIN:
            print(" you win ! ")
        elif status == Game_Status.LOSE:
            print(" you lose !")
        elif status == Game_Status.PUSH:
            print(" push !")

    def play(self):
        playing = True

        while playing:
            self.deck = Deck()
            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)
            self.first_hand = Hand()
            self.second_hand = Hand()

            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            print("Your hand is:")
            self.player_hand.display()
            print()
            print("Dealer's hand is:")
            self.dealer_hand.display()

            game_over = False
            can_play_double_down = True

            while not game_over:
                player_has_blackjack = self.player_hand.check_for_blackjack()
                dealer_has_blackjack = self.dealer_hand.check_for_blackjack()
                if player_has_blackjack or dealer_has_blackjack:
                    self.show_blackjack_results(player_has_blackjack, dealer_has_blackjack)
                    break

                choice = input("Please choose [Hit / Stand / DoubleDown/ Split] by typing the option").lower()
                while choice not in ["h", "s", "d", "p", "hit", "stand", "doubledown", "split"]:
                    choice = input("Please enter 'hit' or 'stand' or 'doubledown' or 'split' (or H/S/D/p) ").lower()

                if choice in ['hit', 'h']:
                    self.player_hand.add_card(self.deck.deal())
                    self.player_hand.display()
                    can_play_double_down = False
                    if self.player_hand.is_busted():
                        print("You have lost!")
                        game_over = True

                elif choice in ["stand", "s"]:

                    while self.dealer_hand.get_value() < 17:
                        self.dealer_hand.add_card(self.deck.deal())

                    print("Final Results")
                    print("Your hand:", self.player_hand.get_value())
                    print("Dealer's hand:", self.dealer_hand.get_value())

                    if self.player_hand.is_busted():
                        self.print_status(Game_Status.LOSE)
                    elif self.dealer_hand.is_busted():
                        self.print_status(Game_Status.WIN)
                    elif self.player_hand.player_win(self.dealer_hand):
                        self.print_status(Game_Status.WIN)
                    elif self.player_hand.is_push(self.dealer_hand):
                        self.print_status(Game_Status.PUSH)
                    elif self.player_hand.player_loss(self.dealer_hand):
                        self.print_status(Game_Status.LOSE)
                    self.display_result()
                    game_over = True

                elif choice in [" doubledown ", "d"] and can_play_double_down:
                    self.player_hand.add_card(self.deck.deal())

                    while self.dealer_hand.get_value() < 17:
                        self.dealer_hand.add_card(self.deck.deal())

                    if self.player_hand.is_busted():
                        self.print_status(Game_Status.LOSE)
                    elif self.dealer_hand.is_busted():
                        self.print_status(Game_Status.WIN)
                    elif self.player_hand.player_win(self.dealer_hand):
                        self.print_status(Game_Status.WIN)
                    elif self.player_hand.player_loss(self.dealer_hand):
                        self.print_status(Game_Status.LOSE)
                    elif self.player_hand.is_push(self.dealer_hand):
                        self.print_status(Game_Status.PUSH)
                    self.display_result()
                    game_over = True

                elif choice in [" doubledown ", "d"] and not can_play_double_down:
                    print("you can not play double down")

                elif choice in [" split ", "p"] and self.player_hand.can_split():
                    first_card = Card(self.player_hand.cards[0].suit, self.player_hand.cards[0].value)
                    second_card = Card(self.player_hand.cards[1].suit, self.player_hand.cards[1].value)
                    self.first_hand.add_card(first_card)
                    self.second_hand.add_card(second_card)
                    self.first_hand.add_card(self.deck.deal())
                    self.second_hand.add_card(self.deck.deal())
                    print("your first hand : ")
                    self.first_hand.final_display()
                    print("your second hand : ")
                    self.second_hand.final_display()

                    not_finish_first_loop = True
                    while not_finish_first_loop:
                        first_choice = input("Please choose [Hit / stand] for your first hand ").lower()
                        while first_choice not in ["h", "s", "hit", "stand"]:
                            first_choice = input("Please enter 'hit' or 'stand' (or H/S) for the first hand ").lower()
                        if first_choice in ['hit', 'h']:
                            self.first_hand.add_card(self.deck.deal())
                            self.first_hand.display()
                            if self.first_hand.is_busted():
                                print("You have lost in your first hand!")
                                not_finish_first_loop = False
                        else:
                            not_finish_first_loop = False

                    not_finish_second_loop = True
                    while not_finish_second_loop:
                        second_choice = input("Please choose [Hit / stand] for your second hand ").lower()
                        while second_choice not in ["h", "s", "hit", "stand"]:
                            second_choice = input("Please enter 'hit' or 'stand' (or H/S) for the second hand ").lower()
                        if second_choice in ['hit', 'h']:
                            self.second_hand.add_card(self.deck.deal())
                            self.second_hand.display()
                            if self.second_hand.is_busted():
                                print("You have lost in your second hand!")
                                not_finish_first_loop = False
                        else:
                            not_finish_second_loop = False

                    if not not_finish_first_loop and not not_finish_second_loop:

                        while self.dealer_hand.get_value() < 17:
                            self.dealer_hand.add_card(self.deck.deal())

                        if self.dealer_hand.is_busted():

                            print("Final Results")
                            self.first_hand.final_display()
                            self.second_hand.final_display()
                            self.dealer_hand.final_display()
                            print(" you win in both hands")
                            game_over = True

                        else:

                            print("Final Results")
                            print("Your first hand:", self.first_hand.get_value())
                            print("Your second hand:", self.second_hand.get_value())
                            print("Dealer's hand:", self.dealer_hand.get_value())

                            if self.first_hand.is_busted():
                                print("you lost your first hand , your hand is over 21")
                            elif self.first_hand.player_win(self.dealer_hand):
                                print("You Win in your first hand!")
                            elif self.first_hand.player_loss(self.dealer_hand):
                                print("you lost your first hand ")
                            elif self.first_hand.is_push(self.dealer_hand):
                                print("push in the first hand!")
                            if self.second_hand.is_busted():
                                print("you lost your first hand , your hand is over 21")
                            elif self.second_hand.player_loss(self.dealer_hand):
                                print("you lost your second hand ")
                            elif self.second_hand.player_win(self.dealer_hand):
                                print("You Win in your second hand!")
                            elif self.second_hand.is_push(self.dealer_hand):
                                print("push in the second hand!")
                            game_over = True

                elif choice in [" split ", "p"] and self.player_hand.can_not_split():
                    print(" no you can not splet")

            again = input("Play Again? [Y/N] ")
            while again.lower() not in ["y", "n"]:
                again = input("Please enter Y or N ")
            if again.lower() == "n":
                print("Thanks for playing!")
                playing = False
            else:
                playing = True

    def display_result(self):

        print("player hand")
        self.player_hand.final_display()
        print("dealer hand")
        self.dealer_hand.final_display()

    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack):

        if player_has_blackjack and dealer_has_blackjack:
            print("Both players have blackjack! Draw!")
        elif player_has_blackjack:
            print("You have blackjack! You win!")
        elif dealer_has_blackjack:
            print("Dealer has blackjack! Dealer wins!")


class Result:

    def __init__(self, dealer_card, player_hand_value):
        self.dealer_card = dealer_card
        self.player_hand_value = player_hand_value
        self.hit_win_count = 0
        self.hit_loss_count = 0
        self.hit_draw_count = 0
        self.stand_win_count = 0
        self.stand_loss_count = 0
        self.stand_draw_count = 0


class Simulation:

    def __init__(self):
        self.results = []
        self.deck = Deck()

    def simulation_rounds(self, num_of_rounds):
        self.start = time()
        for round in range(num_of_rounds):

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            player_hand_value = self.player_hand.get_value()

            while self.player_hand.get_value() < 11:
                self.player_hand.add_card(self.deck.deal())
                player_hand_value = self.player_hand.get_value()

            while self.dealer_hand.get_value() < 17:
                self.dealer_hand.add_card(self.deck.deal())

            dealer_up_card = self.dealer_hand.cards[0].value
            actions = ["h", "s"]
            random.shuffle(actions)
            choice = actions.pop(0)

            if choice in ['h'] and player_hand_value != 21:
                self.player_hand.add_card(self.deck.deal())
                self.calculateResult('h', dealer_up_card, player_hand_value)

            else:
                self.calculateResult('s', dealer_up_card, player_hand_value)

        self.display_result()

    def calculateResult(self, action, dealer_up_card, player_hand_value):

        result = self.if_there(dealer_up_card, player_hand_value)
        if result is None:
            result = Result(dealer_up_card, player_hand_value)
            self.results.append(result)

        if self.player_hand.is_busted():

            if action == 'h':
                result.hit_loss_count += 1
            else:
                result.stand_loss_count += 1

        elif self.dealer_hand.is_busted():

            if action == 'h':
                result.hit_win_count += 1
            else:
                result.stand_win_count += 1

        elif self.player_hand.check_for_blackjack():

            result.stand_win_count += 1

        elif self.player_hand.player_win(self.dealer_hand):

            if action == 'h':
                result.hit_win_count += 1
            else:
                result.stand_win_count += 1

        elif self.player_hand.is_push(self.dealer_hand):

            if action == 'h':
                result.hit_draw_count += 1
            else:
                result.stand_draw_count += 1

        elif self.player_hand.player_loss(self.dealer_hand):

            if action == 'h':
                result.hit_loss_count += 1
            else:
                result.stand_loss_count += 1

    def if_there(self, dealer_up_card, player_hand_value):
        if len(self.results) > 0:
            for result in self.results:
                if result.dealer_card == dealer_up_card and result.player_hand_value == player_hand_value:
                    return result
        return None

    def display_result(self):
        self.results.sort(key=lambda x: x.dealer_card)
        self.results.sort(key=lambda x: x.player_hand_value)

        total_wins = 0
        total_loss = 0
        total_push = 0
        total_hit_win = 0
        total_hit_loss = 0
        total_hit_push = 0
        total_stand_win = 0
        total_stand_loss = 0
        total_stand_push = 0
        counter = 1
        dash = '-' * 118
        print(dash)
        print('{:<12s}{:>12s}{:>19s}{:>12s}{:>12s}{:>9s}{:>13s}{:>14s}{:>8}'.format("Counter", "Player Card Value",
                                                                                    "Dealer Up Card", "Hit Win",
                                                                                    "Hit Lose",
                                                                                    "Push", "Stand win",
                                                                                    "Stand Loss", "Push"))
        print(dash)

        for result in self.results:
            print('{:>1}{:>20}{:>20}{:>15}{:>12}{:>12}{:>10}{:>13}{:>12}'.format(counter, result.player_hand_value,
                                                                                 result.dealer_card,
                                                                                 result.hit_win_count,
                                                                                 result.hit_loss_count,
                                                                                 result.hit_draw_count,
                                                                                 result.stand_win_count,
                                                                                 result.stand_loss_count,
                                                                                 result.stand_draw_count))
            counter += 1
            total_wins += result.hit_win_count + result.stand_win_count
            total_loss += result.hit_loss_count + result.stand_loss_count
            total_push += result.hit_draw_count + result.stand_draw_count
            total_hit_win += result.hit_win_count
            total_hit_loss += result.hit_loss_count
            total_hit_push += result.hit_draw_count
            total_stand_win += result.stand_win_count
            total_stand_loss += result.stand_loss_count
            total_stand_push += result.hit_draw_count

        total = total_wins + total_loss + total_push
        print("total wins  :", total_wins)
        print("total loss  :", total_loss)
        print("total push  :", total_push)
        print("total       :", total)
        print()
        print("----------- details ------------")
        print("total hit wis    :", total_hit_win)
        print("total hit loss   :", total_hit_loss)
        print("total hit push   :", total_hit_push)
        print("total stand  wis :", total_stand_win)
        print("total stand loss :", total_stand_loss)
        print("total stand push :", total_stand_push)
        self.end = time()
        print("time " + str(self.end - self.start) )


class OurStrategy(Simulation):

    def __init__(self):
        super().__init__()
        self.results = []
        self.deck = Deck()

    def simulation_rounds(self, num_of_rounds):
        self.start = time()
        for round in range(num_of_rounds):

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            player_hand_value = self.player_hand.get_value()

            while self.player_hand.get_value() < 11:
                self.player_hand.add_card(self.deck.deal())
                player_hand_value = self.player_hand.get_value()

            while self.dealer_hand.get_value() < 17:
                self.dealer_hand.add_card(self.deck.deal())

            dealer_up_card = self.dealer_hand.cards[0].value

            if (player_hand_value == 11 and dealer_up_card in ["2", "4", "5", "6", "7", "8", "9", "10"]) or \
                    (player_hand_value == 12 and dealer_up_card in ["2", "7", "8", "9", "10", "A"]) or \
                    (player_hand_value == 13 and dealer_up_card in ["5", "7", "8", "9"]) or \
                    (player_hand_value == 14 and dealer_up_card == "9") or \
                    (player_hand_value == 15 and dealer_up_card == "A"):

                self.player_hand.add_card(self.deck.deal())
                self.calculateResult('h', dealer_up_card, player_hand_value)

            else:
                self.calculateResult('s', dealer_up_card, player_hand_value)

        self.display_result()

if __name__ == "__main__":

    x = Simulation()
    x.simulation_rounds(1000000)

    s = OurStrategy()
    s.simulation_rounds(1000000)