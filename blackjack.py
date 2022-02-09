import random
import sys


class Game:
    def __init__(self, money):
        # Set up the constants:
        self.HEARTS = chr(9829)  # Character 9829 is '♥'.
        self.DIAMONDS = chr(9830)  # Character 9830 is '♦'.
        self.SPADES = chr(9824)  # Character 9824 is '♠'.
        self.CLUBS = chr(9827)  # Character 9827 is '♣'.
        # (A list of chr codes is at https://inventwithpython.com/charactermap)
        self.BACKSIDE = 'backside'
        self.money = money

    def main(self):
        print('''Blackjack,
     
          Rules:
           Try to get as close to 21 without going over.
           Kings, Queens, and Jacks are worth 10 points.
           Aces are worth 1 or 11 points.
           Cards 2 through 10 are worth their face value.
           (H)it to take another card.
           (S)tand to stop taking cards.
           On your first play, you can (D)ouble down to increase your bet
           but must hit exactly one more time before standing.
           In case of a tie, the bet is returned to the player.
           The dealer stops hitting at 16.''')

        while True:  # Main game loop.
            # Check if the player has run out of money:
            if self.money <= 0:
                print("You're broke!")
                print("Good thing you weren't playing with real money.")
                print('Thanks for playing!')
                sys.exit()

            # Let the player enter their bet for this round:
            print('Money:', self.money)
            bet = self.getBet(self.money)

            # Give the dealer and player two cards from the deck each:
            deck = self.getDeck()
            dealerHand = [deck.pop(), deck.pop()]
            playerHand = [deck.pop(), deck.pop()]

            # Handle player actions:
            print('Bet:', bet)
            while True:  # Keep looping until player stands or busts.
                self.displayHands(playerHand, dealerHand, False)
                print()

                # Check if the player has bust:
                if self.getHandValue(playerHand) > 21:
                    break

                # Get the player's move, either H, S, or D:
                move = self.getMove(playerHand)

                # Handle the player actions:
                if move == 'D':
                    # Player is doubling down, they can increase their bet:
                    additionalBet = self.getBet(min(bet, (self.money - bet)))
                    bet += additionalBet
                    print('Bet increased to {}.'.format(bet))
                    print('Bet:', bet)

                elif move in ('H', 'D'):
                    # Hit/doubling down takes another card.
                    newCard = deck.pop()
                    rank, suit = newCard
                    print('You drew a {} of {}.'.format(rank, suit))
                    playerHand.append(newCard)

                    if self.getHandValue(playerHand) > 21:
                        # The player has busted:
                        continue

                elif move in ('S', 'D'):
                    # Stand/doubling down stops the player's turn.
                    break

            # Handle the dealer's actions:
            if self.getHandValue(playerHand) <= 21:
                while self.getHandValue(dealerHand) < 16:
                    # The dealer hits:
                    print('Dealer hits...')
                    dealerHand.append(deck.pop())
                    self.displayHands(playerHand, dealerHand, False)

                    if self.getHandValue(dealerHand) > 21:
                        break  # The dealer has busted.
                    input('Press Enter to continue...')
                    print('\n\n')

            # Show the final hands:
            self.displayHands(playerHand, dealerHand, True)

            playerValue = self.getHandValue(playerHand)
            dealerValue = self.getHandValue(dealerHand)
            # Handle whether the player won, lost, or tied:
            if dealerValue > 21:
                print('Dealer busts! You win ${}!'.format(bet))
                self.money += bet
            elif (playerValue > 21) or (playerValue < dealerValue):
                print('You lost!')
                self.money -= bet
            elif playerValue > dealerValue:
                print('You won ${}!'.format(bet))
                self.money += bet
            elif playerValue == dealerValue:
                print('It\'s a tie, the bet is returned to you.')

            input('Press Enter to continue...')
            print('\n\n')

    @staticmethod
    def getBet(maxBet):
        """Ask the player how much they want to bet for this round."""
        while True:  # Keep asking until they enter a valid amount.
            print('How much do you bet? (1-{}, or QUIT)'.format(maxBet))
            bet = input('> ').upper().strip()
            if bet == 'QUIT':
                print('Thanks for playing!')
                sys.exit()

            if not bet.isdecimal():
                continue  # If the player didn't enter a number, ask again.

            bet = int(bet)
            if 1 <= bet <= maxBet:
                return bet  # Player entered a valid bet.

    def getDeck(self):
        """Return a list of (rank, suit) tuples for all 52 cards."""
        deck = []
        for suit in (self.HEARTS, self.DIAMONDS, self.SPADES, self.CLUBS):
            deck.extend((str(rank), suit) for rank in range(2, 11))
            deck.extend((rank, suit) for rank in ('J', 'Q', 'K', 'A'))
        random.shuffle(deck)
        return deck

    def displayHands(self, playerHand, dealerHand, showDealerHand):
        """Show the player's and dealer's cards. Hide the dealer's first card if showDealerHand is False."""
        print()
        if showDealerHand:
            print('DEALER:', self.getHandValue(dealerHand))
            self.displayCards(dealerHand)
        else:
            print('DEALER: ???')
            # Hide the dealer's first card:
            self.displayCards([self.BACKSIDE] + dealerHand[1:])

        # Show the player's cards:
        print('PLAYER:', self.getHandValue(playerHand))
        self.displayCards(playerHand)

    @staticmethod
    def getHandValue(cards):
        """Returns the value of the cards. Face cards are worth 10, aces are
        worth 11 or 1 (this function picks the most suitable ace value)."""
        value = 0
        numberOfAces = 0

        # Add the value for the non-ace cards:
        for card in cards:
            rank = card[0]  # card is a tuple like (rank, suit)
            if rank == 'A':
                numberOfAces += 1
            elif rank in ('K', 'Q', 'J'):  # Face ards are worth 10 points.
                value += 10
            else:
                value += int(rank)  # Numbered cards are worth their number.

        # Add the value for the aces:
        value += numberOfAces  # Add 1 per ace.
        for _ in range(numberOfAces):
            # If another 10 can be added with busting, do so:
            if value + 10 <= 21:
                value += 10

        return value

    def displayCards(self, cards):
        """Display all the cards in the cards list."""
        rows = ['', '', '', '', '']  # The text to display on each row.

        for card in cards:
            rows[0] += ' ___  '  # Print the top line of the card.
            if card == self.BACKSIDE:
                # Print a card's back:
                rows[1] += '|## | '
                rows[2] += '|###| '
                rows[3] += '|_##| '
            else:
                # Print the card's front:
                rank, suit = card  # The card is a tuple data structure.
                rows[1] += '|{} | '.format(rank.ljust(2))
                rows[2] += '| {} | '.format(suit)
                rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

        # Print each row on the screen:
        for row in rows:
            print(row)

    def getMove(self, playerHand):
        """Asks the player for their move, and returns 'H' for hit, 'S' for stand, and 'D' for double down."""
        while True:  # Keep looping until the player enters a correct move.
            # Determine what moves the player can make:
            moves = ['(H)it', '(S)tand']

            # The player can double down on their first move, which we can
            # tell because they'll have exactly two cards:
            if len(playerHand) == 2 and self.money > 0:
                moves.append('(D)ouble down')

            # Get the player's move:
            movePrompt = ', '.join(moves) + '> '
            move = input(movePrompt).upper()
            if move in ('H', 'S') or move == 'D' and '(D)ouble down' in moves:
                return move  # Player has entered a valid move.


Game(100).main()
