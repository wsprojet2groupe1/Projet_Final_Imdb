import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour charger les données depuis un fichier CSV
@st.cache_resource
def load_data():
    # Chemin du fichier CSV
    movies_path = 'https://raw.githubusercontent.com/wsprojet2groupe1/Projet_Final_Imdb/main/df_with_recommendationsSfini.csv'
    
    # Lire les données
    movies = pd.read_csv(movies_path)
    
    return movies

# Charger les données
movies = load_data()

movies_list = movies['primaryTitle'].values

def recommend_movies(title, movies):
    # Vérifier si le titre existe
    if title not in movies['primaryTitle'].values:
        return pd.DataFrame()  # Return empty DataFrame if title not found
    
    # Trouver l'index du film sélectionné
    idx = movies[movies['primaryTitle'] == title].index[0]
    
    # Préparer les recommandations
    recommendations = []

    for i in range(1, 6):  # Les colonnes des films recommandés sont numérotées de 1 à 5
        recommended_title = movies[f'Film {i}'][idx]  # Get the recommended movie title
        recommended_idx = movies[movies['primaryTitle'] == recommended_title].index[0]  # Get the index of the recommended movie
        
        recommendations.append({
            'primaryTitle': recommended_title,
            'overview': movies[f'overview_{i}'][idx],
            'genresST': movies[f'genresST_{i}'][idx],
            'primaryName': movies[f'primaryName_{i}'][idx],
            'averageRating': movies[f'averageRating_{i}'][idx],
            'startYear': movies[f'startYear_{i}'][idx],
            'poster_path': movies[f'poster_path_{i}'][idx],
            'tconst': movies['tconst'][recommended_idx]  # Use the recommended movie's tconst
        })
    
    # Convert list of dictionaries to DataFrame
    recommendations_df = pd.DataFrame.from_records(recommendations)
    
    # Ajouter des URL pour les affiches des films
    base_url = "https://image.tmdb.org/t/p/original/"
    recommendations_df['poster_urls'] = recommendations_df['poster_path'].apply(
        lambda path: base_url + path.lstrip('/') if path else "https://via.placeholder.com/300x450"
    )

    return recommendations_df

# CSS personnalisé
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0e0e0;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        text-align: center;
    }
    .container {
        width: 100%;
        max-width: 100vw;
        padding: 0 20px;
    }
    .custom-title {
        font-family: 'Alata', sans-serif;
        color: #5ce1e6;
        font-size: 100px;
        margin: 40px 0 20px 0;
        text-transform: uppercase;
    }
    .custom-subtitle {
        font-family: 'Arial', sans-serif;
        color: #f0f0f0;
        font-size: 30px;
        margin-bottom: 40px;
    }
    .custom-selectbox {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
    }
    .custom-selectbox select {
        font-size: 22px;
        padding: 12px;
        border-radius: 8px;
        border: 2px solid #FFD700;
        background-color: #333;
        color: #FFD700;
        transition: all 0.3s ease;
    }
    .custom-selectbox select:hover {
        background-color: #444;
    }
    .recommendation-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        width: 100%;
    }
    .recommendation {
        display: flex;
        align-items: flex-start;
        border: 2px solid #FFD700;
        border-radius: 10px;
        background-color: #333;
        padding: 20px;
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .recommendation:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    }
    .recommendation img {
        border-radius: 10px;
        width: 250px;
        height: auto;
        margin-right: 20px;
    }
    .recommendation .info {
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: left;
    }
    .recommendation h3 {
        color: #FFD700;
        font-size: 24px;
        margin: 0;
    }
    .recommendation .genres {
        font-size: 20px;
        color: #f0f0f0;
        margin: 5px 0;
        display: flex;
        gap: 10px;
    }
    .recommendation .genres span {
        background-color: #444;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .recommendation .rating,
    .recommendation .year,
    .recommendation .actors,
    .recommendation .overview-text {
        color: #f0f0f0;
        font-size: 20px;
        margin: 5px 0;
    }
    .recommendation .year-title,
    .recommendation .actors-title,
    .recommendation .overview-title {
        color: #FFD700;
        font-size: 24px;
        margin: 10px 0 5px;
    }
    .stButton button {
        background-color: #6e00c7;
        color: #ffffff;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #b10000;
    }
    </style>
    <div class="container">
        <div class="custom-title">HELLO CINÉ</div>
        <div class="custom-subtitle">Find your next favorite Movie, and Enjoy! <span>🍿</span></div>
    </div>
    """, unsafe_allow_html=True)

# Sélection des films
st.markdown('<div class="custom-selectbox">', unsafe_allow_html=True)
selectvalues = st.multiselect("Select Movies", movies_list, label_visibility='collapsed')
st.markdown('</div>', unsafe_allow_html=True)

# Bouton de recommandation
if st.button("Show Recommendations", key="recommend_button", help="Click to get recommendations", use_container_width=True):
    if selectvalues:
        st.markdown('<div class="recommendation-container">', unsafe_allow_html=True)
        for selectvalue in selectvalues:
            st.markdown(f"<h2>Recommendations for {selectvalue}:</h2>", unsafe_allow_html=True)
            recommendations = recommend_movies(selectvalue, movies)
            if not recommendations.empty:
                for _, row in recommendations.iterrows():
                    imdb_url = f"https://www.imdb.com/title/{row['tconst']}/"
                    
                    st.markdown(f"""
                        <div class="recommendation">
                            <img src="{row['poster_urls']}" alt="{row['primaryTitle']}">
                            <div class="info">
                                <a href="{imdb_url}" target="_blank"><h3>{row['primaryTitle']}</h3></a>
                                <div class="genres">
                                    {''.join(f'<span>{genre.strip()}</span>' for genre in row['genresST'].strip("[]").replace("'", "").split(','))}
                                </div>
                                <div class="rating">⭐ {row['averageRating']}</div>
                                <div class="year-title">Year</div>
                                <div class="year">{row['startYear']}</div>
                                <div class="actors-title">Actors</div>
                                <div class="actors">{row['primaryName']}</div>
                                <div class="overview-title">Overview</div>
                                <div class="overview-text">{row['overview']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("<p>No recommendations available.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("<p>Please select at least one movie.</p>", unsafe_allow_html=True)
