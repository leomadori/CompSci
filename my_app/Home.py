import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=scope)

st.sidebar.title("Spotify Login")
if st.sidebar.button("Login to Spotify"):
    auth_url = auth_manager.get_authorize_url()
    st.sidebar.write(f'<meta http-equiv="refresh" content="0; url={auth_url}" />', unsafe_allow_html=True)

code = st.query_params.get("code")
if code:
    token_info = auth_manager.get_access_token(code)
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        st.sidebar.success("You have successfully logged in!")



st.header("Welcome to Spoolify")
st.subheader("Find the perfect tune")
st.text("New music is just a search away.")
st.divider()
