# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of the recommender as a judge at a talent show. It looks at every song in the catalog, one at a time, and gives each a score based on how well it fits the listener. Then it lines the songs up from highest score to lowest and shows the top five.

**What it knows about each song:** its genre, its mood, and its energy (a number from 0 to 1, where a quiet ambient track is low and a loud metal track is high). The catalog also lists tempo, valence (how positive a song sounds), danceability and acousticness, but the score doesn't use them yet.

**What it knows about the listener:** their favorite genre, their second favorite genre, the mood they want in the morning, the mood they want at night, and how much energy they want. It also needs to be told whether it's morning or night.

**How a song earns points:**

- **Genre:** 1.5 points for the favorite genre, or 0.75 for the second favorite.
- **Mood:** 1.5 points if the song matches the mood for the current time of day.
- **Energy:** up to 1 point. The closer the song is to the energy the listener wants, the more it earns.

The highest possible score is 4 points. For example, take a listener who loves rock, wants intense music in the morning, and wants an energy level of 0.85. In the morning, the rock song Storm Runner gets 1.5 points for its genre and 1.5 for its intense mood. Its energy of 0.91 is very close to the target, which adds 0.94, for a total of 3.94. At night, that listener wants melancholy music, so the same song loses its mood points and drops to 2.44.

**Breaking ties:** if two songs have the same score, the one closer to the target energy comes first. If they're still tied, they go in alphabetical order by title, so the results are the same on every run.

**Why each song was picked:** every recommendation lists the reasons behind its score, such as "genre match (+1.5)", so the listener can see exactly where the points came from.

**Changes from the starter logic:** the starter profile had one genre, one mood and one energy level. I added a second favorite genre so that related music can earn partial credit, and separate morning and night moods because what people want to hear can change during the day. I also lowered the favorite genre from 2 points to 1.5 so that it counts the same as a mood match and doesn't outweigh it.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
