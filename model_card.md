# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

caamp-music-recommender-v0

---

## 2. Intended Use  

This recommender suggests five songs from a small catalog that best match a listener's taste. Each suggestion comes with the reasons it was picked. It's content-based: it looks only at what a song is like (its genre, mood and energy), not at what other listeners played. This gives lesser-known artists the same chance as popular ones.

**Who it's for:** this is a classroom project for exploring how recommender systems work. It isn't meant for real users. The catalog is too small and the scoring too simple to stand in for a real music app.

**What it assumes about the listener:**

- They can name a favorite genre and, optionally, a second favorite.
- Their taste can be described by one mood for the morning, one for the night, and one energy level.
- Genre and mood together matter more than energy. Each match is worth 1.5 points, while energy is worth at most 2.
- Someone tells it whether it's morning or night. It doesn't check the clock.

---

## 3. How the Model Works  

The recommender compares every song in the catalog to the listener's taste and gives it a score: the more a song has in common with what the listener likes, the higher it scores. It then sorts the songs by score and recommends the top five.

**What it knows about each song:** its genre, its mood, and its energy (a number from 0 to 1, where a quiet ambient track is low and a loud metal track is high). The catalog also lists tempo, valence (how positive a song sounds), danceability and acousticness, but the score doesn't use them yet.

**What it knows about the listener:** their favorite genre, their second favorite genre, the mood they want in the morning, the mood they want at night, and how much energy they want. It also needs to be told whether it's morning or night.

**How a song earns points:**

- **Genre:** 1.5 points for the favorite genre, or 0.75 for the second favorite.
- **Mood:** 1.5 points if the song matches the mood for the current time of day.
- **Energy:** up to 2 points, calculated as 2 × (1 − the gap between the song's energy and the listener's target). The closer the song, the more it earns.

The highest possible score is 5 points. For example, take a listener who loves rock, wants intense music in the morning, and wants an energy level of 0.85. In the morning, the rock song Storm Runner gets 1.5 points for its genre and 1.5 for its intense mood. Its energy of 0.91 is very close to the target, which adds 1.88, for a total of 4.88. At night, that listener wants melancholy music, so the same song loses its mood points and drops to 3.38.

**Breaking ties:** if two songs have the same score, the one closer to the target energy comes first. If they're still tied, they go in alphabetical order by title, so the results are the same on every run.

**Why each song was picked:** every recommendation lists the reasons behind its score, such as "genre match (+1.5)", so the listener can see exactly where the points came from.

**Changes from the starter logic:** the starter profile had one genre, one mood and one energy level. I added a second favorite genre so that related music can earn partial credit, and separate morning and night moods because what people want to hear can change during the day. I also lowered the favorite genre from 2 points to 1.5 so that it counts the same as a mood match and doesn't outweigh it. Later I doubled the weight of energy (from up to 1 point to up to 2), so that among songs with the same labels, the one closest to the listener's energy wins more clearly. I also tried halving genre, but then the top song matched the listener's favorite genre only 10–23% of the time, so I changed genre back to 1.5.

---

## 4. Data  

The catalog is `data/songs.csv`: 30 songs by 28 artists. Each song has a genre, a mood, and five numbers between 0 and 1 (energy, valence, danceability, acousticness, plus tempo in BPM). The score only uses genre, mood and energy.

**What's in it:**

- **23 genres**, from pop, rock and hip hop to bossa nova, gospel, bluegrass and drum and bass. Lofi has the most songs (3). Pop, hip hop, country, classical and reggae have 2 each, and the other 17 genres have just 1.
- **16 moods.** Chill and melancholy have 3 songs each, most others have 2, and relaxed, moody, focused and confident have only 1.
- **Energy** runs from 0.18 (Winter Psalm) to 0.97 (Iron Cathedral), but it leans high: 14 songs are at 0.7 or above and only 7 are below 0.4.

**Changes to the data:** the starter catalog had 10 songs (ids 1 to 10). I added 20 more (ids 11 to 30) to cover genres and moods the starter didn't have, such as hip hop, country, classical, metal, reggae and gospel.

**What's missing:**

- **Common mood words.** There are no "calm", "sad" or "energetic" songs. A listener who asks for "calm" (like profile 3) can never get mood points.
- **Depth in each genre.** With only one song in most genres, a fan of metal or jazz gets one genre match and then filler.
- **Loud sad songs and quiet happy ones.** Every melancholy song has energy below 0.5, so some combinations of mood and energy don't exist.
- **Anything beyond the labels:** lyrics, language, vocals vs. instrumental, release year, popularity, and the fact that a song can fit more than one genre or mood.

---

## 5. Strengths  

**Listeners whose tastes agree with each other.** The system works best when the favorite genre, mood and energy all point at the same songs. The rock lover (rock, intense, energy 0.85) gets Storm Runner first with 4.88 out of 5, then Gym Hero (intense, 0.93). That's exactly the list I'd expect for someone who wants loud, intense music.

**Time of day really changes the results.** The same rock lover gets Storm Runner at 4.88 in the morning, but at night, when they want melancholy music, it drops to 3.38. One profile can cover two different listening moments.

**Partial credit for a second genre.** A rock fan who also likes metal gets Iron Cathedral at #3 for its genre match, ahead of songs that only match on energy. The list feels related to their taste without repeating one genre.

**It's easy to see why a song was picked.** Every result lists its points, for example "genre match (+1.5); morning mood match (+1.5); energy closeness (+1.88)". When a result looked wrong during testing, I could tell right away which rule caused it.

**Sensible fallback.** When nothing matches the genre or mood, the list falls back to songs with the closest energy. A listener who asks for medium energy gets medium-energy songs, not random ones.

**Same results every time.** Ties are broken by energy and then by title, so running the same profile twice always gives the same list. That made it easy to compare runs when I changed the weights.

---

## 6. Limitations and Bias 

We have a small dataset so the catalog leans toward loud songs, so listeners who want quiet music have very few songs near their energy target: three quiet tracks (Spacewalk Thoughts, Winter Psalm and Areia Clara) show up in 25–34% of all top-five lists, whatever genre the listener likes.
In terms of the model, Genres and moods have to match the catalog's labels exactly, and 17 of the 23 genres have only one song, so fans of rare genres, or anyone who types "Rock", "indie" or "calm", get one match or none and then filler. The system also ignores the `likes_acoustic` preference, never mixes in anything new, and gives the same profile the same five songs every time, which keeps listeners inside what they already said they like.

---

## 7. Evaluation  

### Profiles I tested

I tested 10 profiles. Three are normal listeners: a pop lover, a rock lover and a calm jazz listener. Seven are edge cases. They try to trick the scoring with conflicting tastes, unknown labels, typos, bad numbers and missing info. I also ran a quick "happy pop" check. The full output is under Test results below.

### What I looked for

- Does the #1 song match the genre, mood and energy the listener asked for?
- Do the reasons add up to the score?
- When I change one thing in a profile, does the list change in a way that makes sense?

### Comparing the profiles

**Pop lover vs. rock lover.** Both want intense, loud music (energy 0.85). Only the genre is different. So Gym Hero (pop) and Storm Runner (rock) swap places at the top. The last two songs are the same for both. 

**Rock lover vs. calm jazz listener.** These two want opposite things. The rock lover gets loud songs. The jazz listener gets quiet jazz and classical songs. No song is on both lists. This makes sense. Energy pulls them to opposite ends of the catalog.

**Pop lover vs. calm jazz listener.** Both listen at night. The pop lover gets intense songs, because that's their night mood. The jazz listener asked for "calm" songs. But the catalog has no calm songs. So their list only matches on genre and energy. This surprised me.

**Rock lover vs. "High energy + sad".** Both want loud music. But the second one also wants melancholy music. All the melancholy songs are quiet. So their list is full of quiet, sad songs. The mood points beat the energy points. The listener gets sad songs, but not loud ones.

**Metal fan with energy 1.5 vs. rock lover.** Energy only goes up to 1, so 1.5 is not valid. The system didn't crash. It still found the right songs (metal and angry). But every song lost energy points, and quiet songs got negative points.

**"Time of day = evening" and "Missing second genre".** Both crashed. "Evening" isn't morning or night, so the system can't find a mood. Leaving out the second genre also breaks it. Both should have a default instead.

### What surprised me

A **data issue** comes from what's in `songs.csv`. A **model issue** comes from how the scoring works.

- **Model issue:** A song with the wrong mood can still rank high. It only needs the right genre and energy. The scoring treats each label on its own, so it can't tell that "intense" is far from "happy".
- **Model issue:** The same two filler songs (Banjo Breakneck and Afterglow Protocol) show up for both the pop and rock lovers. Once genre and mood stop matching, only energy decides. Nothing in the scoring adds variety.
- **Data issue:** "Calm" isn't a mood in the catalog. So a calm listener never gets mood points.
- **Model issue:** A capital letter was enough to lose every match. The scoring compares labels letter by letter.
- **Model issue:** A bad energy number didn't crash anything, but "evening" did. The code doesn't check its inputs.

### Other checks

- I ran the 5 tests in `tests/test_recommender.py`. They all pass.
- I compared the output before and after changing the weights. Halving genre made the top song match the listener's genre only 10–23% of the time, down from about 50%. So I changed genre back to 1.5.

### Test results

All results below are the terminal output of `python3 -m src.main`, using the current weights (genre 1.5, mood 1.5, energy up to 2).

#### Standard profiles

**Profile 1: pop lover at night** (pop / indie, morning mood calm, night mood intense, energy 0.85, night)

```text
Top 5 recommendations (night)
============================================
1. Gym Hero                     Score: 4.84
   - genre match (+1.5)
   - night mood match (+1.5)
   - energy closeness (+1.84)

2. Sunrise City                 Score: 3.44
   - genre match (+1.5)
   - energy closeness (+1.94)

3. Storm Runner                 Score: 3.38
   - night mood match (+1.5)
   - energy closeness (+1.88)

4. Banjo Breakneck              Score: 1.96
   - energy closeness (+1.96)

5. Afterglow Protocol           Score: 1.94
   - energy closeness (+1.94)
```

**Profile 2: rock lover in the morning** (rock / metal, morning mood intense, night mood melancholy, energy 0.85, morning)

```text
Top 5 recommendations (morning)
============================================
1. Storm Runner                 Score: 4.88
   - genre match (+1.5)
   - morning mood match (+1.5)
   - energy closeness (+1.88)

2. Gym Hero                     Score: 3.34
   - morning mood match (+1.5)
   - energy closeness (+1.84)

3. Iron Cathedral               Score: 2.51
   - second favorite genre match (+0.75)
   - energy closeness (+1.76)

4. Banjo Breakneck              Score: 1.96
   - energy closeness (+1.96)

5. Afterglow Protocol           Score: 1.94
   - energy closeness (+1.94)
```

**Profile 3: calm jazz listener at night** (jazz / classical, calm morning and night, energy 0.5, night)

```text
Top 5 recommendations (night)
============================================
1. Coffee Shop Stories          Score: 3.24
   - genre match (+1.5)
   - energy closeness (+1.74)

2. Ascension in D               Score: 2.51
   - second favorite genre match (+0.75)
   - energy closeness (+1.76)

3. Winter Psalm                 Score: 2.11
   - second favorite genre match (+0.75)
   - energy closeness (+1.36)

4. Island Time Again            Score: 2.00
   - energy closeness (+2.00)

5. Slow Burn Letter             Score: 1.96
   - energy closeness (+1.96)
```

#### Adversarial / edge-case profiles

**High energy + sad mood:** classical / blues, melancholy, energy 0.9, morning. Wants sad music that is also loud.

```text
High energy + sad mood
============================================
1. Winter Psalm             classical  melancholy  energy 0.18  Score: 3.56
   genre match (+1.5); morning mood match (+1.5); energy closeness (+0.56)
2. Crossroads Whiskey       blues      melancholy  energy 0.46  Score: 3.37
   second favorite genre match (+0.75); morning mood match (+1.5); energy closeness (+1.12)
3. Ascension in D           classical  uplifting   energy 0.62  Score: 2.94
   genre match (+1.5); energy closeness (+1.44)
4. Last Exit Home           country    melancholy  energy 0.38  Score: 2.46
   morning mood match (+1.5); energy closeness (+0.96)
5. Bassline Sunrise         drum and bass euphoric    energy 0.90  Score: 2.00
   energy closeness (+2.00)
```

**Unknown genre and mood:** k-pop / opera, mood sad, energy 0.5, night. None of these are in the catalog.

```text
Unknown genre and mood
============================================
1. Island Time Again        reggae     carefree    energy 0.50  Score: 2.00
   energy closeness (+2.00)
2. Slow Burn Letter         soul       romantic    energy 0.52  Score: 1.96
   energy closeness (+1.96)
3. Velvet Hours             r&b        romantic    energy 0.48  Score: 1.96
   energy closeness (+1.96)
4. Crossroads Whiskey       blues      melancholy  energy 0.46  Score: 1.92
   energy closeness (+1.92)
5. Dusty Porch Swing        country    nostalgic   energy 0.55  Score: 1.90
   energy closeness (+1.90)
```

**Capitalized / partial genre:** "Rock" / "indie", morning mood "Intense", energy 0.8, morning. Close to real values, but not exact.

```text
Capitalized / partial genre
============================================
1. Sunrise City             pop        happy       energy 0.82  Score: 1.96
   energy closeness (+1.96)
2. Concrete Crown           hip hop    confident   energy 0.78  Score: 1.96
   energy closeness (+1.96)
3. Banjo Breakneck          bluegrass  carefree    energy 0.83  Score: 1.94
   energy closeness (+1.94)
4. Rooftop Lights           indie pop  happy       energy 0.76  Score: 1.92
   energy closeness (+1.92)
5. Night Drive Loop         synthwave  moody       energy 0.75  Score: 1.90
   energy closeness (+1.90)
```

**Genre loyalty vs. mood:** classical / none, mood euphoric, energy 0.9, morning. Favorite genre and mood point in different directions.

```text
Genre loyalty vs. mood
============================================
1. Bassline Sunrise         drum and bass euphoric    energy 0.90  Score: 3.50
   morning mood match (+1.5); energy closeness (+2.00)
2. Afterglow Protocol       house      euphoric    energy 0.88  Score: 3.46
   morning mood match (+1.5); energy closeness (+1.96)
3. Ascension in D           classical  uplifting   energy 0.62  Score: 2.94
   genre match (+1.5); energy closeness (+1.44)
4. Winter Psalm             classical  melancholy  energy 0.18  Score: 2.06
   genre match (+1.5); energy closeness (+0.56)
5. Storm Runner             rock       intense     energy 0.91  Score: 1.98
   energy closeness (+1.98)
```

**Energy out of range (1.5):** metal / punk, mood angry, energy 1.5, morning. Energy is outside the 0 to 1 range.

```text
Energy out of range (1.5)
============================================
1. Iron Cathedral           metal      angry       energy 0.97  Score: 3.94
   genre match (+1.5); morning mood match (+1.5); energy closeness (+0.94)
2. Riot Receipt             punk       angry       energy 0.94  Score: 3.13
   second favorite genre match (+0.75); morning mood match (+1.5); energy closeness (+0.88)
3. Gym Hero                 pop        intense     energy 0.93  Score: 0.86
   energy closeness (+0.86)
4. Storm Runner             rock       intense     energy 0.91  Score: 0.82
   energy closeness (+0.82)
5. Bassline Sunrise         drum and bass euphoric    energy 0.90  Score: 0.80
   energy closeness (+0.80)
```

**Time of day = evening:** lofi / jazz, energy 0.4, time of day "evening". Only morning and night are supported.

```text
Time of day = evening
============================================
   CRASHED: KeyError: 'evening_mood'
```

**Missing second genre:** pop, mood happy, energy 0.8, morning, with no second favorite genre given.

```text
Missing second genre
============================================
   CRASHED: KeyError: 'second_favorite_genre'
```

---

## 8. Future Work  
We need more diverse music and data, more songs per genre, more quiet songs, a variety of moods and mixes of energy (such as louc sad songs). We also need other listeners'play history if we ever want to build a collaborative filtering algorithm.
In the model, we don't have valence, danceability as features... or a maping of how some genres could be close together.
In the future, with more complete data on the catalog and users' history we could build a composite score model that uses both content-based and collaborative. 
Adding a stochastic component would also help listeners discover new songs instead of getting the same five every time.
Finally, making sure the model accounts for corner cases, such as evening mood, missing genre.

---

## 9. Personal Reflection  
I learned that recommender systems can use content-based filtering, collaborative filtering, or a mix of both. With a simple scoring algorithm, I only tried to match a content-based methodology, given that the only data we had was the song catalog.

Something unexpected was that the same three quiet songs showed up in a third of all lists.

It did change how I think about music and video apps. Now I'm more aware of where a recommendation could be coming from.