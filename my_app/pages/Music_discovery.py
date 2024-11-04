import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.header("Use this function to get music recommendation based on music genre")
st.subheader("Insert 3 songs to get more recommendations")

input1 = st.text_input("First Song", placeholder="Press enter to input")
input2 = st.text_input("Second Song", placeholder="Press enter to input")
input3 = st.text_input("Third Song", placeholder="Press enter to input")

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
