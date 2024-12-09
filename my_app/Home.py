import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope
import os


auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=scope,
                            )




#page background here to change color if needed use hexadecimal
##aggiungere un bel po di cose, come immagini e scritte ceh descrivono cosa fa il programma
page_background = f"""
<style>
    .stApp {{
        background-color:  #d6eaf8    ; 
    }}
</style>
"""
st.markdown(page_background, unsafe_allow_html=True)



            
#header
st.markdown("""
            <h1 style='font-size: 50px; 
            color: Black; 
            background:
                linear-gradient(120deg, #FFFFFF,  #d6eaf8);    
            padding: 100px; 
            border-radius: 15px;
            '>Welcome to XXX</h1>
            """, unsafe_allow_html=True)
#this is made in HTML to increase flexibility, it is self explanatory, change X px to increase/decrease font size
#padding is to tell how much larger the area of the background color should be, while border radius is to smooth the curves at the edges of the background color
#in this case h1 is the reference for a HEADER

#subheader
st.markdown("""
            <h2 style='font-size: 30px;
            color: black;
            font-weight: bold;
            text-allign: center;'
            >Find the Perfect Tune</h2>
            """, unsafe_allow_html=True)

#text        
st.markdown("""
            <p style='font-size: 20px; 
            color: black;
            text-allign: center;'
            >New music is just is just a click away from you</p>
            """, unsafe_allow_html=True)

st.divider()

st.markdown("""
            <p style='font-size: 17px;
            color: black;
            text-allign: center;'
            >In order to access all feature we suggest you log in with your spotify account</p>
            """, unsafe_allow_html=True)




#this is to log in to spotify, the user gets redirected to the original spotify authentication page and then redirected back to the website, 
#note: the website MUST run on server.port localhost:8505 otherwise the redirect will fail


if st.button("**Login with Spotify :notes:**" ,help="click to login"):
    auth_url = auth_manager.get_authorize_url()
    st.write(f'<meta http-equiv="refresh" content="0; url={auth_url}" />', unsafe_allow_html=True)


code = st.query_params.get("code")
 
if code:
    try:
        token_info = auth_manager.get_access_token(code)
        if token_info and "access_token" in token_info:
            st.session_state.access_token = token_info["access_token"]
            sp = spotipy.Spotify(auth=st.session_state.access_token)
            st.session_state.user_profile = sp.current_user()
            st.success(f"Successfully authenticated as {st.session_state.user_profile['display_name']}!")
        else:
            st.error("Authentication failed. Please try again.")
    except Exception as e:
        st.error(f"An error occurred during authentication: {e}")


