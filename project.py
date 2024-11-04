# Required Libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy

from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID = '53074fbca7704aef8ff5e43f4371bca2'
SPOTIPY_CLIENT_SECRET = '30a69a1e644640168c85054e1c53b0c3'
SPOTIPY_REDIRECT_URI = 'http://localhost:8505'

scope = "user-top-read playlist-modify-public playlist-modify-private"




auth_manager = SpotifyOAuth(client_id = SPOTIPY_CLIENT_ID, 
                            client_secret = SPOTIPY_CLIENT_SECRET,
                            redirect_uri= SPOTIPY_REDIRECT_URI,
                            scope= scope)



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

else: st.sidebar.error("Please log in to access Spotify features.")


st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go To", ["Home", "Search by type", "Music Discovery"])

# Tab Title


#for background [this is to change the color of the pages, look on internet for CSS colors codes]
if page == "Home":
    background_color = "#F4DEB3" #yellowish
elif page == "Search by type":
    background_color = "#F0EAAC" #light yellowish
elif page == "Music Discovery":
    background_color = "#CCE0AC" #greensish

page_background = f"""
<style>
    .stApp {{
        background-color: {background_color};
    }}
</style>
"""

st.markdown(page_background, unsafe_allow_html=True)

 
#home pagez

if page == "Home":

    st.header("Welcome to Spoolify")
    st.subheader("find the perfect tune")
    st.text("new music is just a search away form you")
    st.divider()

elif page == "Search by type":

    st.title("Use this function to get more information about your favorite songs/artist/albums")
    
    search_choice =  ['Song', 'Artist', 'Album']

    selected_search = st.selectbox('What would you like to search for?', 
                                search_choice, 
                                index = None,
                                placeholder = "please select a search method")

    st.write('You selected:', selected_search)



    if selected_search == 'Song':
        Song_name = st.text_input(':guitar: which song are you looking for?',
                   placeholder= 'Please insert the name of a song')
        if Song_name != '': 
            buttclick = st.button("let's GO :fire:")
    


    elif selected_search == 'Artist':
        Artist_name= st.text_input(':singer: Which artist are you looking for?',
                    placeholder = 'Please insert an artist/band name')
        if Artist_name != '': 
            buttclick = st.button("let's GO :fire:")

            if buttclick: 
                results = sp.search(q=Artist_name, type='artist', limit = 1)

                if results['artists']['items']:
                    artist = results['artists']['items'][0]
                    artist_name = artist['name']
                    artist_followers = artist['followers']['total']
                    artist_genres = ", ".join(artist['genres'])
                    artist_popularity = artist['popularity']
                    artist_image_url = artist['images'][0]['url'] if artist['images'] else None
                    

                    st.subheader(f"Artist name: {artist_name}")

                    if artist_image_url:
                            st.image(artist_image_url, width=300)
                        
                            st.write(f"**Followers**: {artist_followers:,}")
                            st.write(f"**Genres**: {artist_genres}")
                            st.write(f"**Popularity**: {artist_popularity} / 100")
                            
                            st.divider()

                            st.subheader(f"Top 5 Albums by {artist_name}:")
                            top_tracks_results = sp.artist_top_tracks(artist['id'])
                            top_tracks = top_tracks_results['tracks']


                            album_popularity = {}
                            
                            for track in top_tracks:  
                                    album_id = track['album']['id']
                                    album_name = track['album']['name']
                                    release_date = track['album']['release_date']
                                    album_image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                                    track_popularity = track['popularity'] 

                                    

                                    tracks_results = sp.album_tracks(album_id)
                                    tracks = tracks_results['items']

                                    if album_id in album_popularity: 
                                        album_popularity[album_id]['total_popularity'] += track_popularity
                                        album_popularity[album_id]['total_tracks'] += 1
                                    else: 
                                        album_popularity[album_id] = {
                                             'name' : album_name,
                                             'release_date': release_date,
                                             'total_popularity': track_popularity,
                                             'total_tracks': 1,
                                             'image_url': album_image_url
                                            
                                        }
                            album_popularity_sorted = sorted(album_popularity.values(), key=lambda x: x['total_popularity'], reverse=True)       
                                             
                                   
                            #show top 5 (we can change the top X)
                            for idx, album in enumerate (album_popularity_sorted[:5], start=1):
                                    st.write(f"**{idx}. Album Name**: {album['name']}")
                                    st.write(f"**Release Date**: {album['release_date']}")
                                    st.write(f"**Total Tracks in Top 10**: {album['total_tracks']}")
                                    st.write(f"**Total Popularity (Sum of all tracks)**: {album['total_popularity']}")

                                    if album['image_url']:
                                        st.image(album['image_url'], width=200)
                                    st.divider()




    elif selected_search == 'Album':
        Album_name = st.text_input(':cd: Which album are you looking for?',
                    placeholder= "Please insert an album name")
        if Album_name: 
            search_button =  st.button("let's GO :fire:")
            
            if search_button: 
                results = sp.search(q= Album_name, type='album', limit = 12)

                if results['albums']['items']: 
                    st.subheader(f'results for {Album_name}:')
                    
                    albums = results['albums']['items']
                    num_albums = len(albums)

                
                    for album in results['albums']['items']: 
                            album_name = album['name']
                            album_artist = album['artists'][0]['name']
                            album_release_date = album['release_date']
                            album_image_url = album['images'][0]['url']
                    
                
                            if album_image_url: 
                                st.image(album_image_url, width= 150)
                            st.write(f"**Album**:  {album_name}")
                            st.write(f"**Artist**: {album_artist}")
                            st.write(f"**Release Date:** {album_release_date}")
                            st.markdown("---")


elif page == "Music Discovery":
     st.header("Use this function to get music recomandation based on music genre")
     st.subheader("insert 3 songs to get more recomendations")
     
     input1 = st.text_input("First Song",
                            placeholder="press enter to input")
     input2 = st.text_input("Second Song",
                            placeholder="press enter to input")
     input3 = st.text_input("Third Song",
                            placeholder="press enter to input")
     
     if st.button("Get Recommendations!"):
          if input1 and input2 and input3: 
                 with st.spinner("Fetching recommendations..."):
                
                    def get_song_info(song_name): 
                         results = sp.search(q=song_name, type='track', limit= 1)
                         if results['tracks']['items']:
                              track = results['tracks']['items'][0]
                              return track['id'], track['artists'][0]['id']
                         return None, None
                    

                    song1_id, artist1_id = get_song_info(input1)
                    song2_id, artist2_id = get_song_info(input2)
                    song3_id, artist3_id = get_song_info(input3)

                    if song1_id and song2_id and song3_id:
                        artist1_info = sp.artist(artist1_id)
                        artist2_info = sp.artist(artist2_id)
                        artist3_info = sp.artist(artist3_id)


                        genres = set(artist1_info['genres'] + artist2_info['genres'] + artist3_info['genres'])

                        if genres: 
                             genres = list(genres)[:2]  #this is to limit to 5 recomendation, we can change that after
                             st.write(f"Genres detected: {', '.join(genres)}")

                             #this is the beating art of the recomendation system, here we can fine tune the system if needed.
                             # now the recomendation system relies on the genres that is taken by the artist, and also a recomendation based on the artists themselves   
                             
                             recommendations = sp.recommendations(seed_genres=genres,
                                                                  seed_artists= [artist1_id, artist2_id, artist3_id], 
                                                                  limit= 12)
                                                                  
                             

                             st.subheader("Recommended Songs: ") #this is to same tracks in a list to then print out in spotify

                             if 'track_ids' not in st.session_state: 
                                  st.session_state.track_ids = []

                             st.session_state.track_ids = [track['id'] for track in recommendations['tracks']]
                                  

                             

                             num_columns = 3
                             rows = len(recommendations['tracks']) // num_columns + (len(recommendations['tracks']) % num_columns > 0)

                             for row in range(rows):
                                cols = st.columns(num_columns)
                                for idx, track in enumerate(recommendations['tracks'][row * num_columns: (row + 1) * num_columns]):
                                    with cols[idx % num_columns]:
                                        track_name = track['name']
                                        artist_name = track['artists'][0]['name']
                                        album_image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
                                        track_spotify_url = track['external_urls']['spotify']

                                        st.write(f"**{track_name}** by **{artist_name}**")
                                        if album_image_url:
                                            st.image(album_image_url, width=150)
                                        st.markdown(f"[Listen on Spotify]({track_spotify_url})")
                                        st.markdown("<br>", unsafe_allow_html=True)

                                       

                        playlist_name = st.text_input("Give your new playlist a wonderful name:")

                        if st.button("Make me a wonderful playlist"):
                             if playlist_name: 
                                user_id = sp.me()['id']
                                playlist_description = "Playlist created by SPoolify"

                                new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)
                                sp.user_playlist_add_tracks(user=user_id, playlist_id=new_playlist['id'], tracks=st.session_state.track_ids)
                                st.success("Playlist created and songs added! Let's Jam!")

                             else: st.warning("please enter a name for your playlist")


                                        
                        
                    




         

     
