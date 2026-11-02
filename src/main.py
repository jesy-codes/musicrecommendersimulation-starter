"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded {len(songs)} songs from the dataset.")
    user_prefs = {
        "favorite_genre": "rock",
        "second_favorite_genre": "metal",
        "morning_mood": "intense",
        "night_mood": "melancholy",
        "target_energy": 0.85,
        "time_of_day": "morning",
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop {len(recommendations)} recommendations ({user_prefs['time_of_day']})")
    print("=" * 44)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']:<28} Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
