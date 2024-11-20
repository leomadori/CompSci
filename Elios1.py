mport streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope

# OAuth authentication manager
auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)

# Function to get track compatibility
def track_compatibility(sp):
    top_genres = []
    songs = []
    top_artists = []
    total_tracks = sp.current_user_saved_tracks(limit=50)
    saved_tracks = total_tracks['total']
    offset = 0

    while offset < saved_tracks:
        results = sp.current_user_saved_tracks(limit=50, offset=offset)
        for item in results['items']:
            track = item['track']
            songs.append(track['name'])
            for artist in track['artists']:
                artist_characteristics = sp.artist(artist['id'])
                top_genres.extend(artist_characteristics['genres'])
                top_artists.append(artist['name'])
        offset += 50

    # Return genre counts and song list
    number_common_genres = dict(Counter(top_genres))
    return number_common_genres, songs, top_artists

# Function to find common data
def track_common_data(player1_data, player2_data):
    top_genres_player1, songs_player1, top_artists_player1 = player1_data
    top_genres_player2, songs_player2, top_artists_player2 = player2_data

    # Find common genres, songs, and artists
    top_common_genres = set(top_genres_player1).intersection(set(top_genres_player2))
    common_songs = set(songs_player1).intersection(set(songs_player2))
    top_common_artists = set(top_artists_player1).intersection(set(top_artists_player2))

    return {
        "top_common_genres": top_common_genres,
        "common_genres_count": len(top_common_genres),
        "common_songs": common_songs,
        "common_songs_count": len(common_songs),
        "common_artists": top_common_artists,
        "common_artists_count": len(top_common_artists),
    }

# Streamlit UI setup
if 'token_info_player1' not in st.session_state:
    st.session_state.token_info_player1 = None
if 'token_info_player2' not in st.session_state:
    st.session_state.token_info_player2 = None

st.title("Spotify Songs, Artist & Top Genres Match")

# Player 1 settings
st.header("Player 1 Settings")
time_range_player1 = st.slider("Player 1: Select time range (months)", 1, 12, 6)
track_limit_player1 = st.slider("Player 1: Number of tracks to analyze", 1, 50, 20)

# Player 2 settings
st.header("Player 2 Settings")
time_range_player2 = st.slider("Player 2: Select time range (months)", 1, 12, 6)
track_limit_player2 = st.slider("Player 2: Number of tracks to analyze", 1, 50, 20)

# Player login buttons
if st.button("Player 1: Log in to Spotify"):
    auth_player1 = auth_manager.get_authorize_url()
    st.session_state.authorize_url_player1 = auth_player1
    st.write("Player 1, please click the link to log in:")
    st.markdown(f"[Log in to Spotify]({auth_player1})", unsafe_allow_html=True)

if st.button("Player 2: Log in to Spotify"):
    auth_player2 = auth_manager.get_authorize_url()
    st.session_state.authorize_url_player2 = auth_player2
    st.write("Player 2, please click the link to log in:")
    st.markdown(f"[Log in to Spotify]({auth_player2})", unsafe_allow_html=True)

# Handle OAuth callback after logging in
if 'token_info_player1' in st.session_state:
    sp_player1 = spotipy.Spotify(auth=st.session_state.token_info_player1['access_token'])
    # Fetch track data for Player 1
    st.subheader("Player 1 Results")
    top_genres_player1, songs_player1, top_artists_player1 = track_compatibility(sp_player1)
    st.write("Top genres:", top_genres_player1)
    st.write("Number of common songs:", len(songs_player1))
    st.write("Top artists:")
