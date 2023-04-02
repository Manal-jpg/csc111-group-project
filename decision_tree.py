"""
CSC111 Winter 2023 Project:
MelodyMatch: Tailored Music Recommendations Derived From Your Spotify Habits

This Python module contains the DecisionTree class and a collection

Contributors: Manaljav Munkhbayar, Kevin Hu, Stanley Pang, Jaeyong Lee.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
and faculty members at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Manaljav Munkhbayar, Kevin Hu, Stanley Pang, Jaeyong Lee.
"""
from __future__ import annotations
import pandas as pd   #todo: add to project requirements if needed
import csv
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
        - all(key == self._subtrees[key].value for key in self._subtrees)
    """
    value: Optional[set[Song] | tuple]

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the decision trees after sorting the song by its attribute value.

    _subtrees: [list[DecisionTree]]

    def __init__(self, subtrees: list, value: set[Song] | tuple = DECISION_TREE_ROOT) -> None:
        """Initialize a new game tree.
        """
        self.value = value
        self._subtrees = subtrees

    def is_empty(self):
        """Return whether the tree is empty or not"""
        return self.value is None

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self.value}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def __len__(self) -> int:
        """Return the number of items contained in this tree.
        """
        if self.is_empty():
            return 0
        else:
            return 1 + sum(subtree.__len__() for subtree in self._subtrees)

    def get_subtrees(self) -> list[DecisionTree]:
        """Return the subtrees of a Decision Tree"""
        return self._subtrees

    def add_subtree(self, subtree: DecisionTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)

    def find_songs_for_user(self, tree: DecisionTree, user: User, depth: int = 1) -> set[Song]: # add tree attribute
        """Return a set of songs tailored to the User's calculated preference values.
        >>> user = User(None)
        >>> user.user_acousticness = 0.5
        >>> user.user_danceability = 0.5
        >>> user.user_energy = 0.5
        >>> user.user_instrumentalness = 0.5
        >>> user.user_liveness = 0.5
        >>> user.user_loudness = 0
        >>> user.user_speechiness = 0.5
        >>> user.user_valence = 0.5
        >>> read_and_write_csv("/Users/kevinhu/PycharmProjects/csc111-group-project/data/songs_normalize.csv")
        >>> songs = songs_final_csv_to_songs()
        >>> songs = list(songs)
        >>> tree = generate_decision_tree((0,0), 1)
        >>> tree.insert_songs(songs)
        >>> tree.find_songs_for_user(tree, user, 1)
        >>> user = User(None)
        >>> user.user_acousticness = 1
        >>> user.user_danceability = 1
        >>> user.user_energy = 1
        >>> user.user_instrumentalness = 1
        >>> user.user_liveness = 1
        >>> user.user_loudness = 10
        >>> user.user_speechiness = 1
        >>> user.user_valence = 1
        >>> tree.find_songs_for_user(tree, user, 1)
        >>> len(tree.find_songs_for_user(tree, user, 1))
        10
        >>> list_of_leafs = get_song_sets(tree)
        >>> len(list_of_leafs)
        >>> len(songs)
        >>> read_and_write_csv('/Users/kevinhu/Downloads/tracks_features.csv')
        >>> songs = songs_final_csv_to_songs()
        >>> songs = list(songs)
        >>> tree = generate_decision_tree((0,0), 1)
        >>> tree.insert_songs(songs)
        >>> tree.find_songs_for_user(tree, user, 1)
        >>> len(tree.find_songs_for_user(tree, user, 1))
        10
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

    # def insert_songs(self, list_songs: list[Song]) -> None:
    #     """Insert a list of songs into the decision tree so that each song gets sorted into a specific song set.
    #     >>> tree = generate_decision_tree([0], (0,0), 1)
    #     >>> song1 = Song('I hate MAT137', 0, 0, -60, 0, 0, 0, 0, 0)
    #     >>> song2 = Song('I hate MAT223', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
    #     >>> song3 = Song('I hate IMM250', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
    #     >>> tree.insert_songs([song1, song2, song3])
    #     """
    #     for song in list_songs:
    #         self.insert_song(song, 1)

    def insert_songs(self, list_songs: list[Song]) -> None:
        """Insert a list of songs into the decision tree so that each song gets sorted into a specific song set.
        >>> tree = generate_decision_tree((0,0), 1)
        >>> song1 = Song('I hate MAT137', 0, 0, -60, 0, 0, 0, 0, 0)
        >>> song2 = Song('I hate MAT223', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
        >>> song3 = Song('I hate IMM250', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
        >>> tree.insert_songs([song1, song2, song3])
        >>> l = get_song_sets(tree)
        >>> [song for song in l[0][1]][0].name
        'I hate MAT137'
        >>> [song for song in l[1][1]][0].name
        'I love IMM250'
        """
        i = [0]
        for song in list_songs:
            self.insert_song(i, song, 1)

    # def insert_song(self, song: Song, depth: int = 1) -> None:
    #     """Insert a song into the decision tree by recursing through the tree until it gets added to a specific song
    #     set.
    #
    #     >>> tree = generate_decision_tree([0], (0,0), 1)
    #     >>> song1 = Song('I hate MAT137', 0, 0, -60, 0, 0, 0, 0, 0)
    #     >>> tree.insert_song(song1, 1)
    #     >>> song2 = Song('I hate MAT223', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
    #     >>> tree.insert_song(song2, 1)
    #     >>> song3 = Song('I hate IMM250', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
    #     >>> tree.insert_song(song3, 1)
    #     """
    #     score = 0
    #
    #     if depth == 10:
    #         self.value[1].add(song)
    #     else:
    #         if depth == 1:
    #             score = song.danceability
    #
    #         elif depth == 2:
    #             score = song.energy
    #
    #         elif depth == 3:
    #             score = song.loudness
    #
    #             if -60 <= score <= -42.5:
    #                 self._subtrees[0].insert_song(song, depth + 1)
    #             elif -42.4 <= score <= -25:
    #                 self._subtrees[1].insert_song(song, depth + 1)
    #             elif -24.9 <= score <= -7.5:
    #                 self._subtrees[2].insert_song(song, depth + 1)
    #             else:
    #                 self._subtrees[3].insert_song(song, depth + 1)
    #
    #         elif depth == 4:
    #             score = song.speechiness
    #
    #         elif depth == 5:
    #             score = song.acousticness
    #
    #         elif depth == 6:
    #             score = song.instrumentalness
    #
    #         elif depth == 7:
    #             score = song.valence
    #
    #         elif depth == 8:
    #             score = song.liveness
    #
    #     if depth != 3 and depth <= 9:
    #         if 0 <= score <= 0.25:
    #             self._subtrees[0].insert_song(song, depth + 1)
    #         elif 0.26 <= score <= 0.5:
    #             self._subtrees[1].insert_song(song, depth + 1)
    #         elif 0.51 <= score <= 0.75:
    #             self._subtrees[2].insert_song(song, depth + 1)
    #         else:
    #             self._subtrees[3].insert_song(song, depth + 1)

    #todo: remove index attribute
    def insert_song(self, index: list, song: Song, depth: int = 1) -> None:
        """Insert a song into the decision tree by recursing through the tree until it gets added to a specific song
        set.

        >>> tree = generate_decision_tree((0,0), 1)
        >>> song1 = Song('I hate MAT137', 0, 0, -60, 0, 0, 0, 0, 0)
        >>> tree.insert_song([0], song1, 1)
        >>> song2 = Song('I hate MAT223', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
        >>> tree.insert_song([0], song2, 1)
        >>> song3 = Song('I hate IMM250', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
        >>> tree.insert_song([0], song3, 1)
        """
        score = 0

        if depth == 9:
            if len(self._subtrees) == 0:
                self.add_subtree(DecisionTree(value={song}, subtrees=[]))
                index.append(0)
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
                    self._subtrees[0].insert_song(index, song, depth + 1)
                elif -42.4 <= score <= -25:
                    self._subtrees[1].insert_song(index, song, depth + 1)
                elif -24.9 <= score <= -7.5:
                    self._subtrees[2].insert_song(index, song, depth + 1)
                else:
                    self._subtrees[3].insert_song(index, song, depth + 1)

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

        if depth != 3 and depth <= 8:  # changed from 9 to 8
            if 0 <= score <= 0.25:
                self._subtrees[0].insert_song(index, song, depth + 1)
            elif 0.26 <= score <= 0.5:
                self._subtrees[1].insert_song(index, song, depth + 1)
            elif 0.51 <= score <= 0.75:
                self._subtrees[2].insert_song(index, song, depth + 1)
            else:
                self._subtrees[3].insert_song(index, song, depth + 1)

    def return_songs(self, songs_to_return: set, tree: DecisionTree) -> set[Song]:
        """Return a set of songs with length 10"""
        if len(songs_to_return) == 10:
            return songs_to_return
        elif len(songs_to_return) > 10:
            new_songs = set()
            for _ in range(0, 10):
                song = random.choice(list(songs_to_return))
                new_songs.add(song)
            return new_songs
        else:
            all_songs = get_song_sets(tree)  # returns a list of all song sets in the tree
            next_leaf_index = self.find_index_of_next_song_set(all_songs, songs_to_return)
            while len(songs_to_return) != 10:
                additional_songs = self.find_next_song_set(all_songs, next_leaf_index)
                for _ in range(0, len(additional_songs)):
                    songs_to_return.add(random.choice(list(additional_songs)))
                next_leaf_index += 1

            return songs_to_return

    def find_next_song_set(self, all_songs: list[set], index: int) -> set:
        """Return the next leaf of the tree that is a set of songs"""
        index = index % len(all_songs)
        return all_songs[index]

    def find_index_of_next_song_set(self, all_songs: list[set], current_set: set) -> int:
        """Return the index of the next song set given the list of all the song sets"""
        index = all_songs.index(current_set)
        return index + 1

# Generate decision tree but without index numbers for the leaves!
# def generate_decision_tree(value: tuple[int, set[Song]] | tuple, depth: int = 1, i: int = 0) -> DecisionTree:
#     """Add all the tuples and empty song sets into the decision tree."""
#     decision_tree = DecisionTree(value=value, subtrees=[])
#
#     if depth == 9:
#         decision_tree.add_subtree(DecisionTree(value=(i, set()), subtrees=[]))
#         return decision_tree
#     else:
#         if depth == 3:  # Loudness
#             ranges = [(-60.0, -42.5), (-42.4, -25.0), (-24.9, -7.50), (-7.40, 10.0)]
#             subtrees = [generate_decision_tree(value, depth + 1) for value in ranges]
#
#         else:  # Everything else
#             ranges = [(0.00, 0.25), (0.26, 0.50), (0.51, 0.75), (0.76, 1.00)]
#             subtrees = [generate_decision_tree(value, depth + 1) for value in ranges]
#
#         for subtree in subtrees:
#             decision_tree.add_subtree(subtree)
#
#         return decision_tree


# def generate_decision_tree(indexes_so_far: list, value: tuple[int, set[Song]] | tuple, depth: int = 1) \
#         -> DecisionTree:
#     """Add all the tuples and empty song sets into the decision tree.
#
#     >>> tree = generate_decision_tree([0], (0,0), 1, 0)
#     >>> get_song_sets(tree)
#
#     >>> read_and_write_csv("/Users/jaeyonglee/Desktop/csc111-group-project/data/songs_normalize.csv")
#     >>> songs = songs_final_csv_to_songs()
#     >>> songs = list(songs)
#     >>> tree = generate_decision_tree([0], (0,0), 1)
#     >>> tree.insert_songs(songs)
#     >>> list_of_leafs = get_song_sets(tree)
#     >>> songs = [tuple[1] for tuple in list_of_leafs if tuple[1] != set()]
#     >>> sum([len(set) for set in songs])
#     """
#     decision_tree = DecisionTree(value=value, subtrees=[])
#
#     if depth == 9:
#         index = indexes_so_far[len(indexes_so_far) - 1] + 1
#         indexes_so_far.append(index)
#         decision_tree.add_subtree(DecisionTree(value=(index, set()), subtrees=[]))
#         return decision_tree
#     else:
#         if depth == 3:  # Loudness
#             ranges = [(-60.0, -42.5), (-42.4, -25.0), (-24.9, -7.50), (-7.40, 10.0)]
#             subtrees = [generate_decision_tree(indexes_so_far, value, depth + 1) for value in ranges]
#
#         else:  # Everything else
#             ranges = [(0.00, 0.25), (0.26, 0.50), (0.51, 0.75), (0.76, 1.00)]
#             subtrees = [generate_decision_tree(indexes_so_far, value, depth + 1) for value in ranges]
#
#         for subtree in subtrees:
#             decision_tree.add_subtree(subtree)
#
#         return decision_tree
#

def generate_decision_tree(value: set[Song] | tuple, depth: int = 1) -> DecisionTree:
    """Add all the tuples and empty song sets into the decision tree.

    >>> tree = generate_decision_tree((0,0), 1)
    >>> get_song_sets(tree)
    >>> read_and_write_csv("/Users/kevinhu/PycharmProjects/csc111-group-project/data/songs_normalize.csv")
    >>> songs = songs_final_csv_to_songs()
    >>> songs = list(songs)
    >>> tree = generate_decision_tree((0,0), 1)
    >>> tree.insert_songs(songs)
    >>> list_of_leafs = get_song_sets(tree)
    >>> len(list_of_leafs)
    352
    >>> len(songs)
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


# def get_song_sets(decision_tree: DecisionTree) -> list:
#     """Return a list of all the leaf values in the decision tree which are sets of Song objects
#     that have been sorted."""
#     song_sets = []
#
#     if decision_tree.get_subtrees() == []:
#         song_sets.append(decision_tree.value)
#     else:
#         for subtree in decision_tree.get_subtrees():
#             song_sets.extend(get_song_sets(subtree))
#
#     return song_sets

def get_song_sets(decision_tree: DecisionTree) -> list[set]:
    """Return a list of all the leaf values in the decision tree which are sets of Song objects
    that have been sorted.

    >>> tree = generate_decision_tree((0,0), 1)
    >>> song1 = Song('I hate MAT137', 0, 0, -60, 0, 0, 0, 0, 0)
    >>> song2 = Song('I hate MAT223', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
    >>> song3 = Song('I hate IMM250', 0.5, 0.3, -8, 1.0, 0.9, 0.4, 0.3, 0.2)
    >>> song4 = Song('I love IMM250', 1.0, 1.0, 10, 1.0, 1.0, 1.0, 1.0, 1.0)
    >>> tree.insert_songs([song1, song4])
    >>> l = get_song_sets(tree)
    >>> [song for song in l[0]][0].name
    'I hate MAT137'
    >>> [song for song in l[1]][0].name
    'I love IMM250'

    """
    song_sets = []

    if not decision_tree.get_subtrees() and isinstance(decision_tree.value, set):
        song_sets.append(decision_tree.value)
    else:
        for subtree in decision_tree.get_subtrees():
            song_sets.extend(get_song_sets(subtree))

    return song_sets


#todo: delete function later
def check_correctedness(decision_tree: DecisionTree) -> bool:
    """Temporary. Checks if leaves are correct."""
    leaves = get_song_sets(decision_tree)
    value = 1

    for leaf in leaves:
        if leaf[0] != value:
            return False
        value += 1

    return True


def read_large_csv():
    """Read the 1.2 million spotify song dataset"""
    df = pd.read_csv('/Users/kevinhu/Downloads/tracks_features.csv') # may need to change this depending on user's file path
    return df   # This returns everything in the csv file


def read_and_write_csv(csv_file: str) -> None:
    """Loads data from a CSV file, and writes a new CSV file called songs_final.csv.
    songs_final.csv will include only the songs and catergories we plan to use.

    Preconditions:
       - csv_file refers to a valid CSV file in the format described in the project proposal
    """
    with open(csv_file) as input_file, open('data/songs_final.csv', 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file, delimiter=',')
        # Writes the Header
        writer.writerow(['Name', 'Genre', 'Artist', 'Danceability', 'Energy', 'Loudness', 'Speechiness', 'Acousticness',
                         'Instrumentalness', 'Valence', 'Liveness'])
        # Skips the Header
        next(reader)

        names_so_far = set()
        for row in reader:
            # Avoids Duplicate Songs
            if row[1] not in names_so_far:
                names_so_far.add(row[1])
                row_to_write = [row[1], row[17], row[0], row[6], row[7], row[9],
                                row[11], row[12], row[13], row[15], row[14]]
                writer.writerow(row_to_write)


def songs_final_csv_to_songs() -> set[Song]:
    """Reads rows from songs_final.csv and converts each row into a Song object.
    All Song objects will be put into a set."""
    with open('data/songs_final.csv') as file:
        final_csv_reader = csv.reader(file)

        # Skips Header
        next(final_csv_reader)

        songs_so_far = set()
        for song in final_csv_reader:
            songs_so_far.add(Song(name=song[0],
                                  danceability=round(float(song[3]), 2),
                                  energy=round(float(song[4]), 2),
                                  loudness=round(float(song[5]), 1),
                                  speechiness=round(float(song[6]), 2),
                                  acousticness=round(float(song[7]), 2),
                                  instrumentalness=round(float(song[8]), 2),
                                  valence=round(float(song[9]), 2),
                                  liveness=round(float(song[10]), 2),
                                  genre=song[1],
                                  artist=song[2]
                                  )
                             )
        return songs_so_far
