import copy
import enum
from functools import cached_property, cmp_to_key

import structlog

log = structlog.get_logger()


class Rank(enum.IntEnum):
    """
    Various types of hands ordered from weakest to strongest.
    """

    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


class Hand:
    """
    Represents a simple playing card hand. Ranks of cards are standard with aces
    being high.
    """

    values = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    def __init__(self, hand: str, bid: str):
        self.hand = hand
        self.bid = int(bid)

    @cached_property
    def rank(self) -> enum.IntEnum:
        if self.is_five_of_a_kind:
            return Rank.FIVE_OF_A_KIND
        elif self.is_four_of_a_kind:
            return Rank.FOUR_OF_A_KIND
        elif self.is_full_house:
            return Rank.FULL_HOUSE
        elif self.is_three_of_a_kind:
            return Rank.THREE_OF_A_KIND
        elif self.is_two_pair:
            return Rank.TWO_PAIR
        elif self.is_pair:
            return Rank.PAIR
        return Rank.HIGH_CARD

    @cached_property
    def is_five_of_a_kind(self) -> bool:
        """
        Does the hand contain five of a kind.
        """
        for v in self.values:
            if self.hand.count(v) == 5:
                return True
        return False

    @cached_property
    def is_four_of_a_kind(self) -> bool:
        """
        Does the hand contain four of a kind.
        """
        for v in self.values:
            if self.hand.count(v) == 4:
                return True
        return False

    @cached_property
    def is_three_of_a_kind(self) -> bool:
        """
        Does the hand contain three of a kind.
        """
        for v in self.values:
            if self.hand.count(v) == 3:
                return True
        return False

    @cached_property
    def is_full_house(self) -> bool:
        """
        Does the hand contain a full house.
        """
        for v in self.values:
            if self.hand.count(v) == 3:
                c = copy.copy(self.values)
                c.remove(v)
                for v2 in c:
                    if self.hand.count(v2) == 2:
                        return True
        return False

    @cached_property
    def is_two_pair(self) -> bool:
        """
        Does the hand contain two pair.
        """
        for v in self.values:
            if self.hand.count(v) == 2:
                c = copy.copy(self.values)
                c.remove(v)
                for v2 in c:
                    if self.hand.count(v2) == 2:
                        return True
        return False

    @cached_property
    def is_pair(self) -> bool:
        """
        Does the hand contain a pair.
        """
        for v in self.values:
            if self.hand.count(v) == 2:
                return True
        return False

    @classmethod
    def compare(cls, self, o) -> int:  # type: ignore
        if self.rank > o.rank:
            return 1
        elif self.rank < o.rank:
            return -1

        # compare the hands card by card
        for i in range(5):
            if cls.values.index(self.hand[i]) < o.values.index(o.hand[i]):
                return 1
            elif cls.values.index(self.hand[i]) > o.values.index(o.hand[i]):
                return -1

        # same hand
        return 0


class HandWithJokers(Hand):
    """
    Represents a playing card hand that contains jokers. The ranks are mostly
    the same except 'J' is the weakest card and represents a joker instead
    of a Jack.
    """

    values = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

    @cached_property
    def rank(self) -> enum.IntEnum:
        """
        Get the rank of the card by examining how many jokers are in the hand
        and applying them to the rest of the cards without considering the
        jokers.

        NOTE - you can never have a full house with a joker (becomes four of
        a kind).
        """
        if self.hand.count("J") in [4, 5]:
            return Rank.FIVE_OF_A_KIND

        if self.hand.count("J") == 3:
            if self.is_pair:
                return Rank.FIVE_OF_A_KIND
            return Rank.FOUR_OF_A_KIND

        if self.hand.count("J") == 2:
            if self.is_three_of_a_kind:
                return Rank.FIVE_OF_A_KIND
            if self.is_pair:
                return Rank.FOUR_OF_A_KIND
            return Rank.THREE_OF_A_KIND

        if self.hand.count("J") == 1:
            if self.is_four_of_a_kind:
                return Rank.FIVE_OF_A_KIND
            if self.is_three_of_a_kind:
                return Rank.FOUR_OF_A_KIND
            if self.is_two_pair:
                return Rank.FULL_HOUSE
            if self.is_pair:
                return Rank.THREE_OF_A_KIND
            return Rank.PAIR

        return super().rank

    @cached_property
    def is_four_of_a_kind(self) -> bool:
        """
        Does the hand contains 4 of the same non-joker cards.
        """
        for v in self.values:
            if self.hand.count(v) == 4 and v != "J":
                return True
        return False

    @cached_property
    def is_three_of_a_kind(self) -> bool:
        """
        Does the hand contain 3 of the same non-joker cards.
        """
        for v in self.values:
            if self.hand.count(v) == 3 and v != "J":
                return True
        return False

    @cached_property
    def is_two_pair(self) -> bool:
        """
        Does the hand contain 2 pairs of non-joker cards.
        """
        for v in self.values:
            if self.hand.count(v) == 2 and v != "J":
                c = copy.copy(self.values)
                c.remove(v)
                for v2 in c:
                    if self.hand.count(v2) == 2 and v != "J":
                        return True
        return False

    @cached_property
    def is_pair(self) -> bool:
        """
        Does the hand contains 1 pair of non-joker cards.
        """
        for v in self.values:
            if self.hand.count(v) == 2 and v != "J":
                return True
        return False


def solve(hand_cls: type[Hand]) -> int:
    """
    Sort all the hands globally then multiply each bid by the
    global rank.
    """
    s = 0
    hands = []
    with open("puzzle", "r") as f:
        for line in f:
            hands.append(hand_cls(*line.strip().split()))

    for rank, hand in enumerate(sorted(hands, key=cmp_to_key(hand_cls.compare))):
        s += hand.bid * (rank + 1)

    return s


def part1() -> int:
    return solve(Hand)


def part2() -> int:
    return solve(HandWithJokers)


if __name__ == "__main__":
    print(part1())
    print(part2())
