#------------------------------------------------------------------------------
# Name:        mskh.py
# Purpose:     Project 3: Hearts AI
# Author:      Mubashwer Salman Khurshid (ID: 601738)
# Created:     16/05/2013
#------------------------------------------------------------------------------

from operator import itemgetter


# Supporting Functions #########################


def evals(card):
    """This function returns the numerical
    strength of a card."""

    # X is an arbitrary character given the highest value
    # to be used later.
    J, Q, K, A, X = 11, 12, 13, 14, 15
    value = float(eval(card[0]))
    if not value:
        value = 10.0
    return value


def suits_count(hand):
    """It returns a dictionary of number of cards for
    all four suits of a given list of cards."""

    suits = {'C': 0, 'D': 0, 'H': 0, 'S': 0}
    for card in hand:
        if card[-1] == 'C':
            suits['C'] += 1
        elif card[-1] == 'D':
            suits['D'] += 1
        elif card[-1] == 'S':
            suits['S'] += 1
        elif card[-1] == 'H':
            suits['H'] += 1
    return suits


# Answer 1 #####################################


def pass_cards(hand):
    """It passes three cards from hand."""

    retain_list = []  # cards to be potentially retained
    pass_list = []  # cards to be potentially removed

    # The two lists are lists of tuples of card and a
    # score of its value/abundance ratio. (Some of the scores
    # are manipulated to fix their position in list).
    # Cards with higer scores are more likely to be
    # passed.
    suits = suits_count(hand)
    for card in hand:
        # King and Ace of spades has to be removed
        if card == "AS" or card == 'KS':
            pass_list += [(card, evals(card) / suits[card[1]] + 15)]
        # Queen of spades is only retained if there are
        # more than 5 spades remaining in hand. If both king of spades
        # and queen of spades are in hand, and there are atleast
        # 8 spades in hand, queen of spades must be retained
        elif card == 'QS' and suits['S'] > 7 and 'AS' in hand and 'KS' in hand:
            retain_list += [(card, evals(card) / suits[card[1]] - 19)]
        elif card == 'QS' and suits['S'] > 5:
            retain_list += [(card, evals(card) / suits[card[1]] - 16)]
        elif card == 'QS':
            pass_list += [(card, evals(card) / suits[card[1]] + 15)]
        # High diamonds are to be retained in order to win reward.
        elif (card == "AD" or card == "KD" or card == "QD" or card == "JD"):
            retain_list += [(card, evals(card) / suits[card[1]] - 15)]
        # Aces, Kings and Queens are to be removed.
        elif card[0] == 'A' or card[0] == 'K' or card[0] == 'Q':
            pass_list += [(card, evals(card) / suits[card[1]])]
        # All spades lower than Queen are to be retained, so given low score.
        elif card[1] == 'S':
            retain_list += [(card, evals(card) / suits[card[1]] - 15)]
        # 10 of diamonds must be retained so it is given lowest score.
        elif card == '0D':
            retain_list += [(card, evals(card) / suits[card[1]] - 20)]
        # Lower heart cards are to be retained.
        elif card == '2H' or card == '3H' or card == '4H':
            retain_list += [(card, evals(card) / suits[card[1]])]
        # Other heart cards are to be passed.
        elif card[1] == 'H':
            pass_list += [(card, evals(card) / suits[card[1]])]
        else:
            retain_list += [(card, evals(card) / suits[card[1]])]

    # The lists are sorted in descending order of value of cards.
    retain_list = [x[0] for x in sorted(retain_list, key=itemgetter(1),
                   reverse=True)]
    pass_list = [x[0] for x in sorted(pass_list, key=itemgetter(1),
                 reverse=True)]

    if(len(pass_list) > 2):
        return pass_list[:3]
    # If pass_list does not have three cards then card(s) with highest
    # scores from retain_list are passed such that 3 cards are passed.
    else:
        index = 3 - len(pass_list)
        return pass_list + retain_list[:index]


# Answer 2 #####################################


def is_valid_play(played, hand, play, broken):
    """It  determines whether a play is valid or not for given
    hand and other factors."""
    if play not in hand:
        return False

    suits = suits_count(hand)
    penalty_cards = suits['H']  # number of penalty cards
    if 'QS' in hand:
        penalty_cards += 1

    hand_suits = [card[1] for card in hand]  # list of suits in hand

    if played:
        # If card with same suit as lead card is in hand, it must be played.
        if played[0][1] in hand_suits and play[1] != played[0][1]:
                return False

    elif not broken:
            # Play cannot be led by penalty cards unless you have  a hand with
            # only penalty cards when heart is not broken.
            if (play == 'QS' or play[1] == 'H') and penalty_cards < len(hand):
                return False

    return True


# Answer 3 #####################################


def get_valid_plays(played, hand, broken, is_valid=is_valid_play):
    """It returns a list of valid plays for given hand during gameplay."""

    return [card for card in hand if is_valid(played, hand, card, broken)]


# Answer 4 #####################################


def score_game(tricks_won):
    """It returns a list of 4 tuples. Each tuple represents the score
    of a player and boolean value which indicates whether he is a winner
    or loser."""

    def calc_score(tricks):
        """It returns the score of a single player."""

        score = 0
        reward = False
        for trick in tricks:
            for card in trick:  # Increments score card by card of tricks won
                if card[-1] == 'H':
                    score += 1
                elif card == 'QS':
                    score += 13
                elif card == '0D':
                    reward = True
                    score -= 10

        # Score is adjusted for moon shot.
        if score == 26 or (reward and score == 16):
            score -= 52

        return score

    scores = [calc_score(tricks_won[0]),
              calc_score(tricks_won[1]),
              calc_score(tricks_won[2]),
              calc_score(tricks_won[3])]
    result = []
    win_score = min(scores)
    # The player(s) with the minium score wins the game
    for score in scores:
        result += [(score, score == win_score)]

    return result


# Supporting Functions #########################


def cards_suit(hand, suit, inverse=False):
    """It returns the list of cards from hand of a particular suit if
    inverse is False. If inverse is True, it returns the list of cards of a
    particular suit which is absent from the hand."""
    if not inverse:
        suits = []
        for card in hand:
            if card[1] == suit:
                suits += [card]
        # The cards are sorted in order of strength.
        return sorted(suits, key=lambda s: evals(s))
    else:
        suits = [x + suit for x in ['2', '3', '4', '5', '6', '7', '8',
                                    '9', '10', 'J', 'Q', 'K', 'A']]
        return sorted((set(suits) - set(hand)), key=lambda s: evals(s))


def give_card(hand, lead, except_list, move_number, give_weak):
    """It returns strongest card which is weaker than lead and is not
    in the except_list. If no such card is found then it tries to return
    a card which can lose the round (the order of cards in except_list
    determines the priority). If it is not possible to win, then the first
    card of the except list which is available in hand is returned. If none
    of the conditions are possible then the strongest card is returned"""

    can_lose = False
    card_list = []
    lead_strength = evals(lead)
    # card list is sorted in reverse order of card strength
    hand = sorted(hand, key=lambda s: evals(s), reverse=True)

    for card in hand:
        card_strength = evals(card)
        # The strongest card which fulfils the condition below is found
        # it is returned.
        if card_strength < lead_strength:
            can_lose = True
            if (card not in except_list):
                return card

    # If it is possible to lose the round with a card which is in the
    # except list, then such card is returned
    if can_lose and card != '0D':
        for card in except_list:
            card_strength = evals(card)
            if card in hand and card_strength < lead_strength:
                return card

    # If it is not possible to lose the round at all, then strongest card
    # which is not in except list is returned if it is 4th move
    elif move_number == 4 or not give_weak:
        for card in hand:
            if card not in except_list:
                return card
    # If give_weak is False and it is not the final move then
    # weakest card which is not in except list is returned
    else:
        for card in hand[::-1]:
            if card not in except_list:
                return card
    # If it is not possible to lose and play a card outside of except list
    # then the first card from except list is returned.
    if except_list:
        for card in except_list:
            if card in hand:
                return card

    # If none of the conditions can be fulfilled then the strongest
    # card is returned
    return hand[0]


def make_play_list(hand, reward_used, suits):
    """ This function generates a list of cards from hand which can be played
    in which the first card is most desirable to be played and the last card
    is least desirable to be played."""

    play_list = []
    retain_list = []
    # If 10 of diamonds is played in current or previous trick(s)
    # then the score of each card depends on its value/abundance ratio.
    # The higher the score the more likely it is to be played.
    if reward_used:
        for card in hand:
            play_list += [(card, evals(card) / suits[card[1]])]
        return [x[0] for x in sorted(play_list, key=itemgetter(1),
                reverse=True)]
    else:
        # If 10 of diamonds is not played yet then a seperate list for high
        # diamonds is created which is added to the end of the play_list
        # as it is desirable to retain these cards if possible in order to
        # win the reward in a future trick.
        for card in hand:
            if card == 'JD' or card == 'QD' or card == 'AD' or card == 'KD' or\
               card == '0D':
                retain_list += [(card, evals(card) / suits[card[1]])]
            else:
                play_list += [(card, evals(card) / suits[card[1]])]
        play_list = [x[0] for x in sorted(play_list, key=itemgetter(1),
                     reverse=True)]
        retain_list = [x[0] for x in sorted(retain_list, key=itemgetter(1),
                                            reverse=True)]

        return play_list + retain_list


def chance_to_lose(card, others):
    """It determines the chance to lose a round when led. It returns the
    number of cards which are stronger than card to be led that are with
    the other players."""

    # List of cards which are stronger than the card to be led.
    stronger_cards = [x + card[1] for x in ['2', '3', '4', '5', '6', '7', '8',
                                            '9', '10', 'J', 'Q', 'K', 'A']
                      if evals(x + card[1]) > evals(card)]

    chance = 0
    # Chance is the number of cards which are with other players which
    # are stronger than the card to be led
    for entry in stronger_cards:
        if entry in others:
            chance += 1

    return chance


def make_lead_list(hand, qs_stack, qs_hand, reward_used, reward_valid,
                   used_dict, suits, other_dict):
    """ This function generates a list of cards from hand which can be led
    in which the first card is most desirable to be led and the last card
    is least desirable to be led."""

    play_list1 = []
    play_list2 = []
    # A retain list is created which is added to the end of the list to
    # be returned which contains cards that are not desirable to lead with.
    retain_list = ['AD', 'KD', 'QD', 'JD', '0D', 'AS', 'KS', 'QS']

    # If QS is used in a previous trick then high spades should
    # no longer be retained
    if qs_stack:
        retain_list.remove('AS')
        retain_list.remove('KS')
        retain_list.remove('QS')

    # If QS is in hand, then high spades other than  KS and AS should not be
    # retained.
    elif qs_hand:
        retain_list.remove('AS')
        retain_list.remove('KS')

    # If 10 of diamonds is not with any other player than high diamonds need
    # not be retained.
    if reward_used or reward_valid:
        retain_list.remove('AD')
        retain_list.remove('KD')
        retain_list.remove('QD')
        retain_list.remove('JD')
    # The retain list is updated so that it does not contain card which is not
    # in hand.
    delete_list = []
    for card in retain_list:
        if card not in hand:
            delete_list += [card]
    for card in delete_list:
        retain_list.remove(card)

    for card in hand:
        # If a suit has not been played, then it is most desirable to play
        # the highest card of such suit. Higher the value/abundance ratio of
        # of such card, the desirable it is to be played. play_list1 is a
        # separate list of such cards. High hearts are not led.
        if not used_dict[card[1]] and (card not in retain_list) and\
           suits[card[1]] < 4 and card[1] != 'H':
            play_list1 += [(card, evals(card) / suits[card[1]])]
        # If suit of the card has been played previously, then the card with
        # the least chance to win is preferred to be led.
        elif card not in retain_list:
            play_list2 += [(card, chance_to_lose(card, other_dict[card[1]]))]

    play_list1 = [x[0] for x in sorted(play_list1, key=itemgetter(1),
                                       reverse=True)]
    play_list2 = [x[0] for x in sorted(play_list2, key=itemgetter(1),
                                       reverse=True)]

    return play_list1 + play_list2 + retain_list


# Answer 5 #####################################


def play(tricks_won, played, hand, broken, is_valid=is_valid_play,
         valid_plays=get_valid_plays, score=score_game):
    """It returns a card from the list of valid playable cards of hand."""

    valid_moves = valid_plays(played, hand, broken, is_valid)
    hand_suits = suits_count(hand)  # suit count of hand
    valid_suits = suits_count(valid_moves)  # suit count of playable cards

    # Stack is the list of all the cards that have been played previously.
    stack = []
    for tricks in tricks_won:
        for trick in tricks:
            stack += trick

    used_suits = suits_count(stack + played)  # suit of cards already played
    move_number = len(played) + 1  # move number for current round

    lead_suit = ''
    if move_number > 1:
        lead = played[0]
        lead_suit = played[0][1]
        potentials = [card for card in played if card[1] == lead_suit]
        # Strongest card is the card with highest value in played which
        # has the same suit as the lead.
        strongest = sorted(potentials, key=lambda s: evals(s))[-1]

    # Initializing dictionary for list of cards
    valid_dict, hand_dict, used_dict, other_dict = {}, {}, {}, {}

    # Dictionaries of lists of cards of particular suits which can be played
    valid_dict['S'] = cards_suit(valid_moves, 'S')
    valid_dict['D'] = cards_suit(valid_moves, 'D')
    valid_dict['H'] = cards_suit(valid_moves, 'H')
    valid_dict['C'] = cards_suit(valid_moves, 'C')

    # Dictionaries of lists of cards of particular suits which are in hand
    hand_dict['S'] = cards_suit(hand, 'S')
    hand_dict['D'] = cards_suit(hand, 'D')
    hand_dict['H'] = cards_suit(hand, 'H')
    hand_dict['C'] = cards_suit(hand, 'C')

    # Dictionaries of lists of cards of particular suits which already played
    # in current and previous tricks
    used_dict['S'] = cards_suit(stack + played, 'S')
    used_dict['D'] = cards_suit(stack + played, 'D')
    used_dict['H'] = cards_suit(stack + played, 'H')
    used_dict['C'] = cards_suit(stack + played, 'C')

    # Dictionaries of lists of cards of particular suits which are with
    # other players
    other_dict['S'] = cards_suit(hand_dict['S'] + used_dict['S'], 'S', True)
    other_dict['D'] = cards_suit(hand_dict['D'] + used_dict['D'], 'D', True)
    other_dict['H'] = cards_suit(hand_dict['H'] + used_dict['H'], 'H', True)
    other_dict['C'] = cards_suit(hand_dict['C'] + used_dict['C'], 'C', True)

    # suit count of cards which are with other players
    other_suits = suits_count(other_dict['S'] + other_dict['D'] +
                              other_dict['H'] + other_dict['C'])

    # Initializing boolean variables for conditions of queen of spades,
    # 10 of diamonds etc.
    qs_played = qs_stack = qs_valid = qs_with_other = ks_as_valid\
              = high_h_valid = heart_played = reward_used = qs_hand\
              = reward_valid = reward_stack = reward_played = False

    for card in played:
        if card[1] == 'H':
            heart_played = True

    # If QS is played in current trick...
    if 'QS' in played:
        qs_played = True
    # If QS is played in previous tricks...
    if 'QS' in stack:
        qs_stack = True
    # If QS is a valid playable card for current trick...
    if 'QS' in valid_moves:
        qs_valid = True
    if 'QS' in hand:
        qs_hand = True
    # If any other player has QS...
    if 'QS' in other_dict['S']:
        qs_with_other = True
    if 'KS' in valid_moves or 'AS' in valid_moves:
        ks_as_valid = True
    # If hearts with high values are valid playable cards...
    if 'JH' in valid_moves or 'QH' in valid_moves or 'KH' in valid_moves\
       or 'AH' in valid_moves or '0H' in valid_moves or '9H' in valid_moves:
        high_h_valid = True
    # If 10 of diamonds is played in previous or current trick(s)..
    if '0D' in stack or '0D' in played:
        reward_used = True
    if '0D' in valid_moves:
        reward_valid = True
    if '0D' in stack:
        reward_stack = True
    if '0D' in played:
        reward_played = True

    # Special list of diamonds desirable to be retained in some cases
    # in order to win reward.
    diamonds_retain = ['JD', 'QD', 'KD', 'AD', '0D']

    # play_reward determines when to play 10 of diamonds
    play_reward = True
    for card in diamonds_retain[:-1]:
        # If high diamond is played, 0D will not be played
        if card in played:
            play_reward = False
            break

    if play_reward:
        # If high diamond is among others but it is not played, 0D will not
        #vbe played. If it is not the final move of the trick.
        for card in diamonds_retain[:-1]:
            if card in other_dict['D']:
                play_reward = False
                break
        if move_number == 4:
            play_reward = True

    # When you are not leading...
    if move_number > 1:
        if lead_suit == 'C':
            if valid_suits['C']:
                # When clubs is led and there is clubs in hand, if
                # penalty card is played or there is a chance of penalty
                # of penalty card to be played, then strongest card is returned
                # such that the trick will be lost (if possible).
                if qs_played or heart_played:
                    return give_card(valid_dict['C'], strongest,
                                     [], move_number, True)
                elif qs_with_other and other_suits['C'] < 9 and\
                        move_number != 4:
                    return give_card(valid_dict['C'], strongest,
                                     [], move_number, True)
                # If there is no danger of penalty, then the strongest card is
                # played
                else:
                    return valid_dict['C'][-1]

            # If there is no clubs in hand, then if QS is in hand it is played.
            elif qs_valid:
                return 'QS'
            # If possible KS and AS are dumped as they can potentially win
            # QS if an other player has QS...
            elif ks_as_valid and qs_with_other:
                return valid_dict['S'][-1]
            # If there are hearts with high values then strongest such heart
            # is returned
            elif high_h_valid:
                return valid_dict['H'][-1]
            else:
                # If none of the conditions are fulfilled then card
                # with highest value/abundance ratio is played with the
                # exception of high diamonds which depends on whether
                # 10 of diamonds has been previously played or not.
                return make_play_list(valid_moves, reward_used, hand_suits)[0]

        if lead_suit == 'D':
            if valid_suits['D']:
                if qs_played:
                    return give_card(valid_dict['D'], strongest,
                                     diamonds_retain, move_number,
                                     True)
                # If 10 of diamonds is played, strongest diamond is returned
                elif '0D' in played:
                    return valid_dict['D'][-1]
                elif heart_played or (qs_with_other and
                                      other_suits['D'] < 8 and
                                      move_number != 4):
                    return give_card(valid_dict['D'], strongest,
                                     diamonds_retain, move_number,
                                     True)
                # If it is likely that  other player will play 10 of diamonds
                # after your move then highest diamond is played...
                elif '0D' in other_dict['D'] and move_number > 2\
                     and qs_stack and other_dict['D'] < 3:
                    return valid_dict['D'][-1]
                # If it is possible to win the reward by playing '0D',
                # it is done so...
                elif '0D' in valid_moves and play_reward:
                    return '0D'
                else:
                    # If none of the above conditions apply then strongest card
                    # which is weaker than 0D is returned
                    return give_card(valid_dict['D'], '0D',
                                     diamonds_retain, move_number,
                                     False)

            elif qs_valid:
                return 'QS'
            elif ks_as_valid and qs_with_other:
                return valid_dict['S'][-1]
            elif high_h_valid:
                return valid_dict['H'][-1]
            else:
                return make_play_list(valid_moves, False, valid_suits)[0]

        if lead_suit == 'S':
            if valid_suits['S']:
                if qs_played or heart_played:
                    return give_card(valid_dict['S'], strongest, [],
                                     move_number, True)
                # If 'KS' or 'AS' is played in current round, then
                # QS is played if possible in order to dump it to someone else.
                elif ('KS' in played or 'AS' in played) and qs_valid:
                    return 'QS'
                elif qs_stack:
                    return valid_dict['S'][-1]
                # In the final move, stongest spade other than QS
                # is attempted.
                elif move_number == 4:
                    return give_card(valid_dict['S'], 'XS', ['QS'],
                                     move_number, True)
                # If QS is not used up, the strongest card weaker than
                # QS is preferrably played.
                else:
                    return give_card(valid_dict['S'], 'QS', ['QS'],
                                     move_number, False)

            elif high_h_valid:
                return valid_dict['H'][-1]
            else:
                return make_play_list(valid_moves, reward_used, valid_suits)[0]

        if lead_suit == 'H':
            if valid_suits['H']:
                # If it is possible to win reward when there is no danger of QS
                # then highest heart is played.
                if not qs_played and (move_number == 4 or qs_stack) and\
                   reward_played:
                    return valid_dict['H'][-1]
                # When heart is the lead card then the strongest
                # heart which can lose the trick is returned if possible.
                return give_card(valid_dict['H'], strongest, [],
                                 2, True)

            elif qs_valid:
                return 'QS'
            elif ks_as_valid and qs_with_other:
                return valid_dict['S'][-1]
            else:
                return make_play_list(valid_moves, reward_used, hand_suits)[0]

    else:
        # If any other player does not have a higher diamond than 0D then
        # the latter must be played if it is in hand.

        if reward_valid:
            lead_0D = True
            for card in diamonds_retain[:-1]:
                if card in other_dict['D']:
                    lead_0D = False
                    break

            if lead_0D:
                return '0D'

        # The list below contains a list of cards from a card which is most
        # desirable to be led to the card which is least desirable to be led.
        # If a suit has not been played, then it is most desirable to play
        # the highest card of such suit. Higher the value/abundance ratio of
        # of such card, the desirable it is to be played. If all suits has been
        # played then cards with low chance to win have preference for leading.
        # Depending on conditions of QS and 10 of diamonds, the position
        # of some cards in the list the such as high diamonds are manipulated.

        return make_lead_list(valid_moves, qs_stack, qs_hand, reward_used,
                              reward_valid, used_dict, hand_suits,
                              other_dict)[0]


# Bonus ########################################


def predict_score(hand):
    """It predicts the final score with given hand of cards."""

    hand_suits = suits_count(hand)  # suit count of hand
    score = 0
    reward_chance = 0  # chance of winning 10 of diamond
    danger_13 = 0  # chance of winning queen of spades

    # Number of high diamonds  and the abundance of
    # of diamonds determine the chance to win 0D of diamonds.
    if 'AD'in hand:
        reward_chance += 5
    if 'KD' in hand:
        reward_chance += 5
    if 'QD' in hand:
        reward_chance += 4
    if 'JD' in hand:
        reward_chance += 4
    if '0D' in hand:
        reward_chance += 5

    if hand_suits['D'] < 3:
        reward_chance -= 5

    if reward_chance > 0:
        score -= 10

    # Amount of high spades and the abundance of
    # spades determine the chance of winning QS.
    if 'KS' in hand:
        danger_13 += 2 - hand_suits['S']
    if 'AS' in hand:
        danger_13 += 2 - hand_suits['S']
    if 'QS' in hand:
        danger_13 += 2 - hand_suits['S']

    if danger_13 > 0:
        score += 13

    high_hearts = ['8H', '9H', '0H', 'JH', 'QH', 'KH', 'AH']
    for card in high_hearts:
        if card not in hand:
            high_hearts.remove(card)

    # The number of high hearts determine the amount
    # of hearts the player may win.
    if len(high_hearts) > 1 and hand_suits['H'] > 3:
        score += len(high_hearts) * 2

    return score
