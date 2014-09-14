"""Some helpful utility methods
"""
import copy

from pit import config


def swap_cards(cards1, trade1, cards2, trade2):
    """Swaps the traded cards between two lists"""
    [cards1.remove(card) for card in trade1]
    cards1.extend(trade2)
    [cards2.remove(card) for card in trade2]
    cards2.extend(trade1)

def has_cards(search_cards, cards, locked_groups):
    """Returns True if search_cards are in cards after removing locked cards

    locked_groups expected to be a list of objects with a 'cards' attribute.
    """
    cards = copy.copy(cards)
    [[cards.remove(card) for card in group.cards] for group in locked_groups]
    try:
        [cards.remove(card) for card in search_cards]
    except ValueError:
        return False
    return True

def is_winning_hand(cards):
    """Returns True if these cards represent a winning hand.
    """
    if config.BEAR in cards:
        return False
    count = cards.count(max(set(cards), key=cards.count))
    return count == config.COMMODITIES_PER_HAND or (
           count == (config.COMMODITIES_PER_HAND - 1) and config.BULL in cards)

def score_hand(cards):
    """Returns point value for this hand"""
    if is_winning_hand(cards):
        commodity = max(set(cards), key=cards.count)
        score = config.COMMODITIES[commodity]
        if cards.count(commodity) == config.COMMODITIES_PER_HAND and config.BULL in cards:
            score *= 2
    else:
        score = 0
        if config.BEAR in cards:
            score -= config.BEAR_PENALTY
        if config.BULL in cards:
            score -= config.BULL_PENALTY
    return score


def available_card_groups(cards, locked_cards):
    """Returns cards not in locked_cards, grouped into counts.

    This ignores errors caused if a locked card is no longer in cards.
    """
    cards = copy.copy(cards)
    for card in locked_cards:
        try:
            cards.remove(card)
        except ValueError:
            pass
    # could use a dict comprehension if python 2.7+
    card_groups = {}
    for card in set(cards):
        card_groups[card] = cards.count(card)
    return card_groups

def matching_groups(card_groups, quantity):
    """Returns list of groups whose length matches the given quantity"""
    return [[card] * quantity for card in card_groups.keys()
            if card_groups[card] == quantity]

def matching_groups_with(cards, card_groups, quantity):
    """Like matching_groups, but includes specific card(s) in matches if possible

    If cards >= quantity, only they will be returned (as many as possible)
    """
    if len(cards) >= quantity:
        return [cards[:quantity]]
    groups = card_groups.copy()
    for card in cards:
        del groups[card]
    matches = matching_groups(groups, quantity-len(cards))
    return [match + cards for match in matches]
