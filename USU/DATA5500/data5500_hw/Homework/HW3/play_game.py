
from DeckOfCards import *

# welcome message
print("\033[1mWelcome to Blackjack! Let's deal you some cards.\n\033[0m")

#setting up the deck of cards
deck = DeckOfCards()
print("\033[1mUnshuffled Deck:\033[0m")
deck.print_deck()
print()

#condition for unlimited rounds
play_game = True

while play_game == True:

    # shuffling the deck of cards
    deck.shuffle_deck()
    print("\033[1mShuffled Deck:\033[0m")
    deck.print_deck()
    print()

    # setting up user score and conditions
    user_score = 0
    user_busted = 0 # user has not busted
    user_hitting = 0 # user can still hit
    user_blackjack = 0 # user does not have blackjack
    user_aces = 0 # user has no aces

    # setting up dealer score and conditions
    dealer_score = 0
    dealer_busted = 0 # dealer has not busted
    dealer_hitting = 0 # dealer can still hit
    dealer_blackjack = 0 # dealer does not have blackjack
    dealer_in = 0 # dealer gets a turn
    dealer_aces = 0 # dealer has no aces

    # deal two cards to the user
    user_card = deck.get_card()
    user_card2 = deck.get_card()

    # check for aces in user's hand
    if user_card.face == 'Ace':
        user_aces += 1
    if user_card2.face == 'Ace':
        user_aces += 1

    # deal two cards to the dealer
    dealer_card = deck.get_card()
    dealer_card2 = deck.get_card()

    # check for aces in dealer's hand
    if dealer_card.face == 'Ace':
        dealer_aces += 1
    if dealer_card2.face == 'Ace':
        dealer_aces += 1

    # show the user's cards
    print("\033[1mYour Cards\033[0m")
    print(user_card)
    print(user_card2)
    print()

    # calculate the user's hand score
    user_score += user_card.val
    user_score += user_card2.val
    print("Your score: ", user_score, "\n")

    # testing user score
    while user_hitting == 0:

        # black jack when first draw is equal to 21
        if user_score == 21:
            user_hitting = 1
            user_blackjack = 1
            dealer_in = 1 #dealer does not get a turn
        
        else:

            # asking user if they would like another card
            hit = input("Hit? (y/n): ")

            if hit == 'y':

                # giving user another card
                user_card3 = deck.get_card()
                user_score += user_card3.val

                print(user_card3)
                print("Your new score: ", user_score, "\n")

                # tracking ace count
                if user_card3.face == 'Ace':
                    user_aces += 1

                # adjusting ace from 11 to 1
                if user_score > 10 and user_aces > 0:
                    user_score -= 10
                    user_aces -= 1  
                    print("Your adjusted score: ", user_score, "\n")

                # user stops at 21
                if user_score == 21:
                    print("21!")
                    user_hitting = 1

                # checking for bust
                elif user_score > 21:
                    user_hitting = 1
                    user_busted = 1
                    dealer_in = 1 # skips the dealers turn

            # stop users turn
            elif hit == 'n':
                user_hitting = 1

            else:
                print()

    # dealers turn (when given)
    while dealer_in == 0:

        print()

        # show the dealer's cards
        print("\033[1mDealer's Cards\033[0m")
        print(dealer_card)
        print(dealer_card2)
        print()

        # calculate the user's hand score
        dealer_score += dealer_card.val
        dealer_score += dealer_card2.val
        print("Dealer's score: ", dealer_score, "\n")
        
        # checking for blackjack
        if dealer_score == 21:
            dealer_blackjack = 1
            dealer_hitting = 1
            dealer_in = 1

        # checking dealer score
        while dealer_hitting == 0:

            # adjusting ace from 11 to 1
            if dealer_score > 10 and dealer_aces > 0:
                dealer_score -= 10
                dealer_aces -= 1  
                print("Dealer's adjusted score: ", dealer_score, "\n")

            # cheking for bust
            if dealer_score > 21:
                dealer_busted = 1
                dealer_hitting = 1
                dealer_in = 1

            # checking for hitting stop
            elif dealer_score < 17:

                # giving dealer another card
                dealer_card3 = deck.get_card()
                dealer_score += dealer_card3.val

                print(dealer_card3)
                print("Dealer's new score: ", dealer_score, "\n")

                # tracking ace count
                if dealer_card3.face == 'Ace':
                    dealer_aces += 1
            
            # dealer turn ends between 17 and 21
            else:
                dealer_hitting = 1
                dealer_in = 1

    # determining is user or dealer won

    # checking busts
    if user_busted == 1:
        print("You busted")
        print("\033[1mYou lose\033[0m") 
    
    elif dealer_busted == 1:
        print("Dealer busts")
        print("\033[1mYou win\033[0m")
    
    else:

        # checking blackjacks
        if user_blackjack == 1:
            print("Blackjack!")
            print("\033[1mYou win\033[0m")
        
        elif dealer_blackjack == 1:
            print("Dealer has Blackjack")
            print("\033[1mYou lose\033[0m") 

        else:

            # checking scores
            if user_score == dealer_score:
                print("You got the same score")
                print("\033[1mYou draw\033[0m")

            elif user_score > dealer_score:
                print("Your score is higher")
                print("\033[1mYou win\033[0m")

            else:
                print("Dealer's score is higher")
                print("\033[1mYou lose\033[0m") 

    # checking for more games
    more = input("\nAnother game? (y/n): ")
    print()

    # ending game loop
    if more == 'n':
        print("Thanks for playing! \n")
        play_game = False
    
    # keep game looped
    if more == "y":
        print("Here we go again! \n")
        play_game = True

# I learned how to bold text to make it stand out :)



