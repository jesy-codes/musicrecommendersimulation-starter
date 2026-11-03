"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

profile_1 = {
    "favorite_genre": "pop",
    "second_favorite_genre": "indie",
    "morning_mood": "calm",
    "night_mood": "intense",
    "target_energy": 0.85,
    "time_of_day": "night"}
profile_2 = {
    "favorite_genre": "rock",
    "second_favorite_genre": "metal",
    "morning_mood": "intense",
    "night_mood": "melancholy",
    "target_energy": 0.85,
    "time_of_day": "morning"}
profile_3 = {
    "favorite_genre": "jazz",
    "second_favorite_genre": "classical",
    "morning_mood": "calm",
    "night_mood": "calm",
    "target_energy": 0.5,
    "time_of_day": "night"}

# Adversarial / edge-case profiles: each one targets a weakness in the scoring.
adversarial_profiles = {
    # Conflict: wants very high energy, but every melancholy song in the catalog is quiet.
    "High energy + sad mood": {
        "favorite_genre": "classical",
        "second_favorite_genre": "blues",
        "morning_mood": "melancholy",
        "night_mood": "melancholy",
        "target_energy": 0.9,
        "time_of_day": "morning"},
    # Nothing matches: genre and mood aren't in the catalog, so only energy counts.
    "Unknown genre and mood": {
        "favorite_genre": "k-pop",
        "second_favorite_genre": "opera",
        "morning_mood": "sad",
        "night_mood": "sad",
        "target_energy": 0.5,
        "time_of_day": "night"},
    # Near miss: "Rock" and "indie" look right but don't exactly match "rock" or "indie pop".
    "Capitalized / partial genre": {
        "favorite_genre": "Rock",
        "second_favorite_genre": "indie",
        "morning_mood": "Intense",
        "night_mood": "happy",
        "target_energy": 0.8,
        "time_of_day": "morning"},
    # Genre vs. mood: loves classical but wants euphoric, high-energy music.
    "Genre loyalty vs. mood": {
        "favorite_genre": "classical",
        "second_favorite_genre": "",
        "morning_mood": "euphoric",
        "night_mood": "euphoric",
        "target_energy": 0.9,
        "time_of_day": "morning"},
    # Out of range energy: 1.5 isn't a valid energy, so energy points go negative.
    "Energy out of range (1.5)": {
        "favorite_genre": "metal",
        "second_favorite_genre": "punk",
        "morning_mood": "angry",
        "night_mood": "angry",
        "target_energy": 1.5,
        "time_of_day": "morning"},
    # Bad time of day: "evening" isn't morning or night.
    "Time of day = evening": {
        "favorite_genre": "lofi",
        "second_favorite_genre": "jazz",
        "morning_mood": "focused",
        "night_mood": "chill",
        "target_energy": 0.4,
        "time_of_day": "evening"},
    # Missing key: no second favorite genre given at all.
    "Missing second genre": {
        "favorite_genre": "pop",
        "morning_mood": "happy",
        "night_mood": "happy",
        "target_energy": 0.8,
        "time_of_day": "morning"},
}

def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded {len(songs)} songs from the dataset.")

    for user_prefs in [profile_1, profile_2, profile_3]:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\nTop {len(recommendations)} recommendations ({user_prefs['time_of_day']})")
        print("=" * 44)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']:<28} Score: {score:.2f}")
            for reason in explanation.split("; "):
                print(f"   - {reason}")
            print()

    print("\n" + "#" * 44)
    print("ADVERSARIAL / EDGE-CASE PROFILES")
    print("#" * 44)
    for name, user_prefs in adversarial_profiles.items():
        print(f"\n{name}")
        print("=" * 44)
        try:
            recommendations = recommend_songs(user_prefs, songs, k=5)
        except Exception as error:
            print(f"   CRASHED: {type(error).__name__}: {error}")
            continue
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']:<24} {song['genre']:<10} {song['mood']:<11} "
                  f"energy {song['energy']:.2f}  Score: {score:.2f}")
            print(f"   {explanation}")

if __name__ == "__main__":
    main()
