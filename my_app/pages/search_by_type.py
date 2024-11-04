import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("Use this function to get more information about your favorite songs/artist/albums")

search_choice = ['Song', 'Artist', 'Album']
selected_search = st.selectbox('What would you like to search for?', search_choice, placeholder="Please select a search method")
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
