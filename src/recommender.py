import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import asdict, dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    second_favorite_genre: str = ""
    night_mood: Optional[str] = None
    time_of_day: str = "morning"

    def to_prefs(self) -> Dict:
        """Convert the profile to the dictionary score_song expects, using favorite_mood as the morning mood."""
        return {
            "favorite_genre": self.favorite_genre,
            "second_favorite_genre": self.second_favorite_genre,
            "morning_mood": self.favorite_mood,
            "night_mood": self.night_mood or self.favorite_mood,
            "target_energy": self.target_energy,
            "time_of_day": self.time_of_day,
        }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for the user, ranked by recommend_songs."""
        song_dicts = [asdict(song) for song in self.songs]
        return [Song(**song) for song, _, _ in recommend_songs(user.to_prefs(), song_dicts, k)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the reasons behind a song's score as one string."""
        _, reasons = score_song(user.to_prefs(), asdict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dictionaries with numeric fields converted."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return the score with its reasons."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 1.5
        reasons.append("genre match (+1.5)")
    elif song["genre"] == user_prefs["second_favorite_genre"]:
        score += 0.75
        reasons.append("second favorite genre match (+0.75)")

    current_mood = user_prefs[f"{user_prefs['time_of_day']}_mood"]
    if song["mood"] == current_mood:
        score += 1.5
        reasons.append(f"{user_prefs['time_of_day']} mood match (+1.5)")

    energy_points = 1 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top k as (song, score, explanation) tuples."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(
        scored,
        key=lambda item: (
            -item[1],
            abs(item[0]["energy"] - user_prefs["target_energy"]),
            item[0]["title"],
        ),
    )
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
