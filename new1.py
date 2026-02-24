import pickle
import streamlit as st
import requests

TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
PLACEHOLDER = "https://via.placeholder.com/300x450?text=No+Poster"

# ---------------- FETCH POSTER ----------------
def fetch_poster(title):
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": title}
        res = requests.get(url, params=params, timeout=5).json()

        if res.get("results") and res["results"][0].get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + res["results"][0]["poster_path"]
        else:
            return PLACEHOLDER
    except:
        return PLACEHOLDER


# ---------------- RECOMMEND ----------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_indices = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    names = []
    posters = []

    for i in movie_indices:
        title = movies.iloc[i[0]]['title']
        names.append(title)
        posters.append(fetch_poster(title))  # ALWAYS URL STRING

    return names, posters


# ---------------- UI ----------------
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommender System")

movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
