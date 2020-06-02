# took some ideas from this source ( https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b  )
import random
from enum import Enum
import tkinter

class Game_Status(Enum):
    WIN = 1
    LOSE = 2
    PUSH = 3


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        if tkinter.TkVersion >= 8.6:
            self.extension = 'png'
        else:
            self.extension = 'ppm'

    def __repr__(self):
        return 'cards/{}_{}.{}'.format(self.value, self.suit, self.extension)


class Deck:

    def __init__(self):
        self.cards = [Card(s, v) for s in ["spade", "club", "heart",
                                           "diamond"] for v in ["A", "2", "3", "4", "5", "6",
                                                                 "7", "8", "9", "10", "jack", "queen", "king"]] * 6
        random.shuffle(self.cards)

        self.card_images = []
        for card in self.cards:
            image = tkinter.PhotoImage(file=card)
            #card_images[(card.value, card.suit)] = [card.value, card.suit,  image]
            self.card_images.append([card.value, card.suit, image])

        print(self.cards)


    def deal(self):
        if len(self.card_images) > 1:
            return self.card_images.pop(0)
        else:
            self.__init__()
            return self.card_images.pop(0)


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

            mainWindow = tkinter.Tk()
            mainWindow.title("Black Jack")
            mainWindow.geometry("6400x4800")
            mainWindow.configure(bg="blue")
            mainWindow.columnconfigure(0, weight=2)
            mainWindow.columnconfigure(1, weight=2)
            mainWindow.columnconfigure(2, weight=2)
            mainWindow.columnconfigure(3, weight=0)
            mainWindow.columnconfigure(4, weight=5)
            mainWindow.columnconfigure(5, weight=0)
            result_text = tkinter.StringVar()
            result = tkinter.Label(mainWindow, textvariable=result_text)
            result.grid(row=0, column=0, columnspan=3)

            card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, bg="white")
            card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

            dealer_score_label = tkinter.IntVar()
            tkinter.Label(card_frame, text="Dealer", bg="black", fg="white").grid(row=0, column=0)
            tkinter.Label(card_frame, textvariable=dealer_score_label, bg="black", fg="white").grid(row=1, column=0)
            # embedded frame to hold the card images
            dealer_card_frame = tkinter.Frame(card_frame, bg="black")
            dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

            player_score_label = tkinter.IntVar()

            tkinter.Label(card_frame, text="Player", bg="black", fg="white").grid(row=2, column=0)
            tkinter.Label(card_frame, textvariable=player_score_label, bg="black", fg="white").grid(row=3, column=0)
            # embedded frame to hold the card images
            player_card_frame = tkinter.Frame(card_frame, bg="black")
            player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

            button_frame = tkinter.Frame(mainWindow)
            button_frame.grid(row=3, column=1, columnspan=3, sticky='w')

            player_button = tkinter.Button(button_frame, text="Hit", padx=8)
            player_button.grid(row=0, column=0)

            dealer_button = tkinter.Button(button_frame, text="Stay",  padx=5)
            dealer_button.grid(row=0, column=1)

            reset_button = tkinter.Button(button_frame, text="New Game")
            reset_button.grid(row=0, column=2)

            shuffle_button = tkinter.Button(button_frame, text="Shuffle", padx=2)
            shuffle_button.grid(row=0, column=3)




            mainWindow.mainloop()


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




if __name__ == "__main__":

    game = Deck()
    Deck()