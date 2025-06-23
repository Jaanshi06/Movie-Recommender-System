import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=9035960329ec86a7b12b5714b2328c32&language=en-US'.format(
            movie_id))
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Then load them
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Title
st.title('🎬 Movie Recommender System')

#css
st.markdown("""
    <style>
        /* Darker gradient background */
        .stApp {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            background-attachment: fixed;
            font-family: 'Segoe UI', sans-serif;
            color: #ffffff;
        }

        /* Title styling */
        h1 {
            color: #ffffff;
            font-size: 48px;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        /* Label text */
        label, .css-1cpxqw2, .css-14xtw13 {
        font-size: 34px !important;
        color: #bbdefb !important;
        font-weight: 600;
        }


        /* Selectbox */
        .stSelectbox > div {
            background-color: #0d47a1;
            color: #ffffff;
            font-size: 18px;
            border-radius: 8px;
        }

        /* Recommend Button */
        .stButton>button {
            background-color: #64b5f6;
            color: #0d47a1;
            font-size: 18px;
            padding: 12px 28px;
            border-radius: 10px;
            border: none;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.4);
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #42a5f5;
            color: white;
        }

        /* Poster cards */
        .css-1v0mbdj img {
            margin: auto;
            display: block;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6);
        }

        .css-1v0mbdj p {
            text-align: center;
            font-size: 16px;
            color: #ffffff;
            font-weight: 500;
            margin-top: 10px;
        }

        /* Mobile responsive layout */
        @media screen and (max-width: 768px) {
             .element-container > div {
                 flex-direction: column !important;
                 align-items: center !important;
             }
        }
        @media screen and (max-width: 480px) {
             .css-1v0mbdj img {
                width: 90% !important;
             }

            .css-1v0mbdj p {
               font-size: 14px !important;
            }

            label, .css-1cpxqw2, .css-14xtw13 {
                font-size: 24px !important;
            }

            h1 {
                font-size: 32px !important;
            }
        }


    </style>
""", unsafe_allow_html=True)




# UI elements
selected_movie_name = st.selectbox('Select a Movie from the list:', movies['title'].values)
#st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)

# Recommendation button logic
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.markdown(
                f"<p style='text-align: center; font-size: 15px; margin-top: 8px;'>{names[idx]}</p>",
                unsafe_allow_html=True
            )