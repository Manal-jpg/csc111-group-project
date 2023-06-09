"""
CSC111 Winter 2023 Project:
MelodyMatch: Tailored Music Recommendations Derived From Your Spotify Habits

This Python module contains the User class, which represents the user of our program
along with all of their preferred attributes in the songs they listen to.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use by students and faculty
of the CSC111 course department at the University of Toronto. All forms of distribution
of this code, whether as is or with changes, are prohibited. For more information on
copyright for this project's materials, please contact the developers directly.

This file is Copyright (c) 2023 Manaljav Munkhbayar, Kevin Hu, Stanley Pang, Jaeyong Lee.
"""
from typing import Optional

from song import Song
import csv


def read_top_songs_csv(file_name: str):
    """This function reads the user's top songs csv file, which contains the songs along with their attributes.

    It then returns a list of Song objects contructed using the data, which will later be used for the song
    recommendation algorithm
    """
    top_tracks_ids = []
    top_tracks_names = []
    top_tracks_danceability = []
    top_tracks_energy = []
    top_tracks_loudness = []
    top_tracks_speechiness = []
    top_tracks_acousticness = []
    top_tracks_instrumentalness = []
    top_tracks_valence = []
    top_tracks_liveness = []
    top_tracks_tempo = []

    with open(file_name, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            top_tracks_ids.append(row[0])
            top_tracks_names.append(row[1])
            top_tracks_danceability.append(float(row[2]))
            top_tracks_energy.append(float(row[3]))
            top_tracks_loudness.append(float(row[4]))
            top_tracks_speechiness.append(float(row[5]))
            top_tracks_acousticness.append(float(row[6]))
            top_tracks_instrumentalness.append(float(row[7]))
            top_tracks_valence.append(float(row[8]))
            top_tracks_liveness.append(float(row[9]))
            top_tracks_tempo.append(float(row[10]))

    top_songs = []
    for i in range(len(top_tracks_ids)):
        song = Song(name=top_tracks_names[i], danceability=top_tracks_danceability[i], energy=top_tracks_energy[i],
                    loudness=top_tracks_loudness[i], speechiness=top_tracks_speechiness[i],
                    acousticness=top_tracks_acousticness[i], instrumentalness=top_tracks_instrumentalness[i],
                    valence=top_tracks_valence[i], liveness=top_tracks_liveness[i])
        top_songs.append(song)

    return top_songs


class User:
    """A class that represents the user and stores their unique preferences

        Instance Attributes:
        - top_listened_songs:
            The user's top 50 most-listened songs
        - user_danceability:
            Average danceability of the 50 most-listened songs of the user
        - user_energy:
            Average energy of the 50 most-listened songs of the user
        - user_loudness:
            Average loudness of the 50 most-listened songs of the user
        - user_speechiness:
            Average speechiness of the 50 most-listened songs of the user
        - user_acousticness:
            Average acousticness of the 50 most-listened songs of the user
        - user_instrumentalness:
            Average instrumentalness of the 50 most-listened songs of the user
        - user_valence:
            Average valence of the 50 most-listened songs of the user
        - user_liveness:
            Average liveness of the 50 most-listened songs of the user

        Representation Invariants:
        - len(self.top_listened_songs) == 50
        - all(type(song) == Song for song in self.top_listened_songs)
        - 0.0 <= self.user_danceability <= 1.0
        - 0.0 <= self.user_energy <= 1.0
        - -60.0 <= self.user_loudness <= 10.0
        - 0.0 <= self.user_speechiness <= 1.0
        - 0.0 <= self.user_acousticness <= 1.0
        - 0.0 <= self.user_instrumentalness <= 1.0
        - 0.0 <= self.user_valence <= 1.0
        - 0.0 <= self.user_liveness <= 1.0
    """
    top_listened_songs: Optional[list[Song]]
    user_danceability: float
    user_energy: float
    user_loudness: float
    user_speechiness: float
    user_acousticness: float
    user_instrumentalness: float
    user_valence: float
    user_liveness: float

    def __init__(self, top_listened_songs: Optional[list[Song]]) -> None:
        """Initialize a new user.

        Preconditions:
            - self.top_listened_songs is not None
        """
        self.top_listened_songs = top_listened_songs
        self.create_user_profile()

    def create_user_profile(self) -> None:
        """Create the user's profile by finding the average values of the 50 most-listened songs of the user.
        """
        total_danceability = 0
        total_energy = 0
        total_loudness = 0
        total_speechiness = 0
        total_acousticness = 0
        total_instrumentalness = 0
        total_valence = 0
        total_liveness = 0

        for song in self.top_listened_songs:
            total_danceability += song.danceability
            total_energy += song.energy
            total_loudness += song.loudness
            total_speechiness += song.speechiness
            total_acousticness += song.acousticness
            total_instrumentalness += song.instrumentalness
            total_valence += song.valence
            total_liveness += song.liveness

        self.user_danceability = total_danceability / len(self.top_listened_songs)
        self.user_energy = total_energy / len(self.top_listened_songs)
        self.user_loudness = total_loudness / len(self.top_listened_songs)
        self.user_speechiness = total_speechiness / len(self.top_listened_songs)
        self.user_acousticness = total_acousticness / len(self.top_listened_songs)
        self.user_instrumentalness = total_instrumentalness / len(self.top_listened_songs)
        self.user_valence = total_valence / len(self.top_listened_songs)
        self.user_liveness = total_liveness / len(self.top_listened_songs)


def generate_user(example_dataset: bool) -> User:
    """This function creates an instance of the User class using the top song data generated from accessing their
    Spotify account details.

    After retrieving all necessary information, this function returns an instance of the User class.

    The example_dataset parameter is a boolean that is True if the user wishes to use our provided
    example_user_top_songs.csv file rather than generating a csv file of their own via their Spotify account.
    """
    if example_dataset:
        top_songs = read_top_songs_csv('data/example_user_top_songs.csv')
    else:
        top_songs = read_top_songs_csv('data/user_top_songs.csv')

    user_profile = User(top_songs)
    return user_profile


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
