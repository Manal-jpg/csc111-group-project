"""
CSC111 Winter 2023 Project:
MelodyMatch: Tailored Music Recommendations Derived From Your Spotify Habits

This Python module contains the DecisionTree class and a collection of functions that help with
sorting songs using the decision tree and returning the recommended songs tailored to the user's
preferences.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use by students and faculty
of the CSC111 course department at the University of Toronto. All forms of distribution
of this code, whether as is or with changes, are prohibited. For more information on
copyright for this project's materials, please contact the developers directly.

This file is Copyright (c) 2023 Manaljav Munkhbayar, Kevin Hu, Stanley Pang, Jaeyong Lee.
"""
from __future__ import annotations
import random
from user import User
from typing import Optional

from song import Song


DECISION_TREE_ROOT = (0, 0)


class DecisionTree:
    """A decision tree for organizing our songs.

    Each node in the tree either stores a range of numbers or a set of songs.

    Instance Attributes:
        - value: a range of floats represented as a tuple or a set of songs if it is the leaf of the decision tree.

    Representation Invariants:
        - isinstance(self.value, set) or isinstance(self.value, tuple) or self.value is None
        - self._value is not None or self._subtrees == []
    """
    value: Optional[set | tuple]

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the decision trees after sorting the song by its attribute value.
    #      The decision trees are stored in a list.
    _subtrees: list[DecisionTree]

    def __init__(self, subtrees: list, value: set | tuple = DECISION_TREE_ROOT) -> None:
        """Initialize a new game tree.
        """
        self.value = value
        self._subtrees = subtrees

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def is_empty(self):
        """Return whether the tree is empty or not.
        """
        return self.value is None

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.

        Preconditions:
            - depth >= 0
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self.value}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def __len__(self) -> int:
        """Return the number of items contained in this tree.
        """
        if self.is_empty():
            return 0
        else:
            return 1 + sum(subtree.__len__() for subtree in self._subtrees)

    def get_subtrees(self) -> list[DecisionTree]:
        """Return the subtrees of a Decision Tree.
        """
        return self._subtrees

    def add_subtree(self, subtree: DecisionTree) -> None:
        """Add a subtree to this decision tree.
        """
        self._subtrees.append(subtree)

    def find_songs_for_user(self, tree: DecisionTree, user: User, depth: int = 1) -> set[Song]:
        """Return a set of songs tailored to the User's calculated preference values.

        Preconditions:
            - depth == 1
            - tree refers to a DecisionTree instance generated by the generate_decision_tree function
        """
        score = 0

        if depth == 10:
            songs_to_return = self.value
            return self.return_songs(songs_to_return, tree)
        else:
            if depth == 1:
                score = user.user_danceability

            elif depth == 2:
                score = user.user_energy

            elif depth == 3:
                score = user.user_loudness

                if -60 <= score <= -42.5:
                    return self._subtrees[0].find_songs_for_user(tree, user, depth + 1)
                elif -42.4 <= score <= -25:
                    return self._subtrees[1].find_songs_for_user(tree, user, depth + 1)
                elif -24.9 <= score <= -7.5:
                    return self._subtrees[2].find_songs_for_user(tree, user, depth + 1)
                else:
                    return self._subtrees[3].find_songs_for_user(tree, user, depth + 1)

            elif depth == 4:
                score = user.user_speechiness

            elif depth == 5:
                score = user.user_acousticness

            elif depth == 6:
                score = user.user_instrumentalness

            elif depth == 7:
                score = user.user_valence

            elif depth == 8:
                score = user.user_liveness

        if depth != 3 and depth <= 9:
            if depth == 9 and len(self._subtrees) == 0:
                self.add_subtree(DecisionTree(value=set(), subtrees=[]))
                return self._subtrees[0].find_songs_for_user(tree, user, depth + 1)
            if 0 <= score <= 0.25:
                return self._subtrees[0].find_songs_for_user(tree, user, depth + 1)
            elif 0.26 <= score <= 0.5:
                return self._subtrees[1].find_songs_for_user(tree, user, depth + 1)
            elif 0.51 <= score <= 0.75:
                return self._subtrees[2].find_songs_for_user(tree, user, depth + 1)
            else:
                return self._subtrees[3].find_songs_for_user(tree, user, depth + 1)

    def insert_songs(self, list_songs: list[Song]) -> None:
        """Insert a list of songs into the decision tree so that each song gets sorted into a specific song set.
        """
        for song in list_songs:
            self.insert_song(song, 1)

    def insert_song(self, song: Song, depth: int = 1) -> None:
        """Insert a song into the decision tree by recursing through the tree until it gets added to a specific song
        set.

        Preconditions:
            - depth == 1
        """
        score = 0

        if depth == 9:
            if len(self._subtrees) == 0:
                self.add_subtree(DecisionTree(value={song}, subtrees=[]))
            else:
                self._subtrees[0].value.add(song)
        else:
            if depth == 1:
                score = song.danceability

            elif depth == 2:
                score = song.energy

            elif depth == 3:
                score = song.loudness

                if -60 <= score <= -42.5:
                    self._subtrees[0].insert_song(song, depth + 1)
                elif -42.4 <= score <= -25:
                    self._subtrees[1].insert_song(song, depth + 1)
                elif -24.9 <= score <= -7.5:
                    self._subtrees[2].insert_song(song, depth + 1)
                else:
                    self._subtrees[3].insert_song(song, depth + 1)

            elif depth == 4:
                score = song.speechiness

            elif depth == 5:
                score = song.acousticness

            elif depth == 6:
                score = song.instrumentalness

            elif depth == 7:
                score = song.valence

            elif depth == 8:
                score = song.liveness

        if depth != 3 and depth <= 8:
            if 0 <= score <= 0.25:
                self._subtrees[0].insert_song(song, depth + 1)
            elif 0.26 <= score <= 0.5:
                self._subtrees[1].insert_song(song, depth + 1)
            elif 0.51 <= score <= 0.75:
                self._subtrees[2].insert_song(song, depth + 1)
            else:
                self._subtrees[3].insert_song(song, depth + 1)

    def return_songs(self, songs_to_return: set, tree: DecisionTree) -> set[Song]:
        """Return a set containing ten songs to recommend to the user.

        Preconditions:
            - decision_tree refers to a DecisionTree instance generated by the generate_decision_tree function
        """
        if len(songs_to_return) == 10:
            return songs_to_return
        elif len(songs_to_return) > 10:
            new_songs = set()
            for _ in range(0, 10):
                song = random.choice(list(songs_to_return))
                new_songs.add(song)
                songs_to_return.remove(song)
            return new_songs
        else:
            all_songs = get_song_sets(tree)  # returns a list of all song sets in the tree
            leaf_index = self.find_index_of_next_song_set(all_songs, songs_to_return) - 1
            next_leaf_index = self.find_index_of_next_song_set(all_songs, songs_to_return)
            while len(songs_to_return) != 10:
                additional_songs = self.find_next_song_set(all_songs, next_leaf_index)
                for _ in range(0, len(additional_songs)):
                    songs_to_return.add(random.choice(list(additional_songs)))
                    if len(songs_to_return) == 10:
                        return songs_to_return

                if next_leaf_index < leaf_index:
                    next_leaf_index -= 1
                else:
                    next_leaf_index += 1
                if next_leaf_index == len(all_songs):
                    next_leaf_index = leaf_index - 1

    def find_next_song_set(self, all_songs: list[set], index: int) -> set:
        """Return the next leaf of the tree that is a set of songs.
        """
        index = index % len(all_songs)
        return all_songs[index]

    def find_index_of_next_song_set(self, all_songs: list[set], current_set: set) -> int:
        """Return the index of the next song set given the list of all the song sets.
        """
        index = all_songs.index(current_set)
        return index + 1


def generate_decision_tree(value: set[Song] | tuple, depth: int = 1) -> DecisionTree:
    """Add all the tuples and empty song sets into the decision tree.

    Preconditions:
        - depth == 1
        - value == (0, 0)
    """
    decision_tree = DecisionTree(value=value, subtrees=[])

    if depth == 9:
        return decision_tree
    else:
        if depth == 3:  # Loudness
            ranges = [(-60.0, -42.5), (-42.4, -25.0), (-24.9, -7.50), (-7.40, 10.0)]
            subtrees = [generate_decision_tree(value, depth + 1) for value in ranges]

        else:  # Everything else
            ranges = [(0.00, 0.25), (0.26, 0.50), (0.51, 0.75), (0.76, 1.00)]
            subtrees = [generate_decision_tree(value, depth + 1) for value in ranges]

        for subtree in subtrees:
            decision_tree.add_subtree(subtree)

        return decision_tree


def get_song_sets(tree: DecisionTree) -> list[set]:
    """Return a list of all the leaf values in the decision tree which are sets of Song objects
    that have been sorted.

    Preconditions:
       - decision_tree refers to a DecisionTree instance generated by the generate_decision_tree function
    """
    song_sets = []

    if not tree.get_subtrees() and isinstance(tree.value, set):
        song_sets.append(tree.value)
    else:
        for subtree in tree.get_subtrees():
            song_sets.extend(get_song_sets(subtree))

    return song_sets


def load_tree_with_songs(songs: list[Song]) -> DecisionTree:
    """Generate a decision tree and insert the given list of songs.
    """
    tree = generate_decision_tree((0, 0), 1)
    tree.insert_songs(songs)
    return tree


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
