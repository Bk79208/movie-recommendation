import pickle
import streamlit as st
import requests
import random

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

error_shown = False
def fetch_poster(movie_id):
    global error_shown
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url)
        data.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = data.json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except requests.exceptions.ConnectionError:
        if not error_shown:
            st.error("No internet connection at present. Unable to fetch images.")
            error_shown = True  # Set the flag to True after showing the error
        return "https://via.placeholder.com/150"  # Return a placeholder image URL
    except requests.exceptions.RequestException as e:
        if not error_shown:
            st.error(f"An error occurred while fetching the images: {e}")
            error_shown = True  # Set the flag to True after showing the error
        return "https://via.placeholder.com/150"  # Return a placeholder image URL


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    # recommended_movie_tag = []
    recommended_movie_genres = []

    for i in distances[1:6]:
           
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_genres.append(movies.iloc[i[0]].genres)

    return recommended_movie_names,recommended_movie_posters,recommended_movie_genres

def recommendFromGenres(genre):
    index = movies[movies['genres'] == genre].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    # recommended_movie_tag = []
    recommended_movie_genres = []

    # for i in distances[1:6]:
    for i in random.sample(distances[1:20], 5):
        
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        # recommended_movie_tag.append(movies.iloc[i[0]].tags)
        recommended_movie_genres.append(movies.iloc[i[0]].genres)

    return recommended_movie_names,recommended_movie_posters,recommended_movie_genres


st.header('Movie Recommendation System')
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
movies['genres'] = movies['genres'].apply(lambda x: x.replace(' ', ', '))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))
movie_genres = pickle.load(open('artifacts/genres_list.pkl','rb'))

def switch_case(value):
    
    if value == "Movies":
        
        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown",
            movie_list
        )

        if st.button('Show Recommendation'):
            recommended_movie_names,recommended_movie_posters,recommended_movie_genres = recommend(selected_movie)
            # ConnectionError: HTTPSConnectionPool(host='api.themoviedb.org', port=443): Max retries exceeded with url: /3/movie/58?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x0000020632CBFC20>: Failed to resolve 'api.themoviedb.org' ([Errno 11001] getaddrinfo failed)"))
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])
                st.text(recommended_movie_genres[0])
            with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])
                st.text(recommended_movie_genres[1])

            with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
                st.text(recommended_movie_genres[2])
            with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
                st.text(recommended_movie_genres[3])
            with col5:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])
                st.text(recommended_movie_genres[4])

    elif value == "Genres":
        
            genres_list = movie_genres['genre'].values
            # genres_list = movie_genres.get('genres', [movie_genres['genre']])
            selected_genre = st.selectbox(
                "Type or select a genre from the dropdown",
                genres_list
            )

            if st.button('Show Recommendation'):
                recommended_movie_names,recommended_movie_posters,recommended_movie_genres = recommendFromGenres(selected_genre)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.text(recommended_movie_names[0])
                    st.image(recommended_movie_posters[0])
                    # st.text(recommended_movie_genres[0])
                with col2:
                    st.text(recommended_movie_names[1])
                    st.image(recommended_movie_posters[1])
                    # st.text(recommended_movie_genres[1])

                with col3:
                    st.text(recommended_movie_names[2])
                    st.image(recommended_movie_posters[2])
                    # st.text(recommended_movie_genres[2])
                with col4:
                    st.text(recommended_movie_names[3])
                    st.image(recommended_movie_posters[3])
                    # st.text(recommended_movie_genres[3])
                with col5:
                    st.text(recommended_movie_names[4])
                    st.image(recommended_movie_posters[4])
                    # st.text(recommended_movie_genres[4])        

value = st.selectbox(
    "Recommendation form Movies or Genres",
    ['Movies', 'Genres']
)
# Handling the selection
result = switch_case(value)
st.write(result)



