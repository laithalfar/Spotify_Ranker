import requests
import streamlit as st
import base64
import time
from streamlit_image_select import image_select
from dotenv import dotenv_values


Temp = dotenv_values(".env")

#endpoints for getting data
SPOTIFY_GET_ARTISTS_ALBUMS_URL = 'https://api.spotify.com/v1/artists/'
SPOTIFY_GET_ARTISTS_ID = 'https://api.spotify.com/v1/search?q='
SPOTIFY_GET_ALBUMS_TRACKS_URL = 'https://api.spotify.com/v1/albums/'
SPOTIFY_GET_TRACKS_AUDIO_FEATURES_URL = 'https://api.spotify.com/v1/audio-features?ids='


#get access token
def get_access_token():
    #needed for authorization
    client_id = Temp["CLIENT_ID"]
    client_secret = Temp["CLIENT_SECRET"]

    # Encode client_id and client_secret to create the authorization header
    credentials = f"{client_id}:{client_secret}"
    base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    authorization_header = f"Basic {base64_credentials}"

    # Define the authentication options
    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers': {
            'Authorization': authorization_header
        },
        'data': {
            'grant_type': 'client_credentials'
        }
    }

    # Send the POST request to obtain the access token
    response = requests.post(**auth_options)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the access token from the response
        print(response.json()['access_token'])
        return( response.json()['access_token'] )
        #print(f"Access Token: {token}")
    else:
        print(f"Error: {response.status_code} - {response.text}")


# gets the artists id from spotidy search
def get_artist(input, token):

    #request artists information
    response = requests.get(
        SPOTIFY_GET_ARTISTS_ID + input + "&type=artist&limit=4", #uses user search and the type is limited to artist while the amount is limited to 4
        headers = {
            "Authorization" : f"Bearer {token}"
        },
    )

    json_format = response.json()


    return_id = {}
    artists_img = []
    artists = []

    #for loop that puts artists images, and artists names into lists and
    #creates a dict with the key being the artists name and the image being
    for c in range(len(json_format["artists"]["items"])):

        #if there is an image for the artist then the process goes normally
        if json_format["artists"]["items"][c]["images"]:
            artists_img.append(json_format["artists"]["items"][c]["images"][0]["url"])
            artists.append(json_format["artists"]["items"][c]["name"])
            return_id[json_format["artists"]["items"][c]["images"][0]["url"]] = json_format["artists"]["items"][c]["id"]
        #if there is no image for the artist then a "NO IMAGE" image is inserted instead
        else:
            artists_img.append("https://dummyimage.com/300x200/ffffff/000000&text=NO+IMAGE")
            artists.append(json_format["artists"]["items"][c]["name"])
            return_id["https://dummyimage.com/300x200/ffffff/000000&text=NO+IMAGE"] = json_format["artists"]["items"][c]["id"]

    if artists_img:

    #Each artist image and name are displayed for the user to choose for
        img = image_select("Choose your artist", artists_img, captions = artists)

    # return the artist that the user chose
        #print(f" : {return_id[img]}")
        return return_id[img]
    else:
        st.write("No results")
        return ''



# get that artists albums
def get_artists_albums(token, ID):

    #request artists albums
    response = requests.get(
        SPOTIFY_GET_ARTISTS_ALBUMS_URL + ID + "/albums?include_groups=album", # uses the artist ID and only get albums
        headers = {
            "Authorization" : f"Bearer {token}"
        },
    )
    #print(response)
    # if the rate limit is exceeded retry-after statement applied
    if response.status_code == 429:
        # Rate limit exceeded, wait for the specified duration
        retry_after = int(response.headers.get('Retry-After', 100000))  # Default to 100000 seconds
        print(f"Rate limit exceeded. Waiting for {retry_after} seconds.")
        time.sleep(retry_after)
        # Retry the API request
        return get_artists_albums(token, ID)

    if response.status_code == 400:
        st.error('Sorry! Refresh something went wrong')
        return {}
    else:
        #change to json format
        json_format = response.json()
        #print(json_format)

        #get amount of albums and create list to store ids
        album_list_length = len(json_format.get("items", {}))
        album_ids = {}

        #extract album ids from the json
        if album_list_length != 0:
            for i in range(album_list_length):
                album_ids[json_format["items"][i]["name"]] = json_format["items"][i]["id"]
                # print(json_format["items"][0])

        #return dict with key being artist name and value artist id
        #print(album_ids)
        return album_ids



# get artists albums
def get_album_tracks(token, album):

    #request albums tracks
    response = requests.get(
        SPOTIFY_GET_ALBUMS_TRACKS_URL + f"{album}/tracks?limit=40",
        headers = {
            "Authorization" : f"Bearer {token}"
        },
    )


    #print(json_format)
    if response.status_code == 429:
        # Rate limit exceeded, wait for the specified duration
        retry_after = int(response.headers.get('Retry-After', 100000))  # Default to 10 seconds
        print(f"Rate limit exceeded. Waiting for {retry_after} seconds.")
        for remaining_seconds in range(retry_after, 0, -1):
            print(f"Remaining seconds: {remaining_seconds}", end='\r')
            time.sleep(1)
        # Retry the API request
        return get_album_tracks(token, album)

    if response.status_code == 400:
        st.error('Sorry! Refresh something went wrong')
        return []
    else:
        #change to json format
        json_format = response.json()
        #get amount of albums and create list to store ids
        track_list_length = len(json_format["items"])
        track_ids = []

        #extract album tracks ids from json
        if track_list_length != 0 and track_list_length >= 5:
            for i in range(track_list_length):
                track_ids.append(json_format["items"][i]["id"])
                #track_ids.append(json_format["items"][i]["id"])
                #print(track_ids)
            #print(track_ids)
            return track_ids
        else:
            return []
        # return list of ids



# evaluate albums score
def tracks_likeability(token, tracks):

    track_string = ','.join(tracks)

    #request tracks audio features
    response = requests.get(
        SPOTIFY_GET_TRACKS_AUDIO_FEATURES_URL + f"{track_string}",
        headers = {
            "Authorization" : f"Bearer {token}"
            },
    )

    if response.status_code == 429:
        # Rate limit exceeded, wait for the specified duration
        retry_after = int(response.headers.get('Retry-After', 100000))  # Default to 10 seconds
        print(f"Rate limit exceeded. Waiting for {retry_after} seconds.")
        for remaining_seconds in range(retry_after, 0, -1):
            print(f"Remaining seconds: {remaining_seconds}", end='\r')
            time.sleep(1)

        # Retry the API request
        return tracks_likeability(token, tracks)

    if response.status_code == 400:
        st.error('Sorry! Refresh something went wrong')
        return 0
    else:
        #change to json format
        json_format = response.json()


        #print("Track ",json_format, end= '\n\n')

        score = 0

        # Define scoring functions for each feature
        def score_danceability(value):
            return 10 if 0.3 <= value <= 0.7 else 5 if value > 0.7 else 0

        def score_energy(value):
            return 10 if 0.4 <= value <= 0.8 else 7 if value < 0.4 else 0

        def score_speechiness(value):
            return 7 if 0.25 <= value <= 0.5 else 10 if value < 0.25 else 0

        def score_acousticness(value):
            return 10 if 0.2 <= value <= 0.6 else 7 if value > 0.6 else 5 if 0.2 > value < 0.1 else 0

        def score_instrumentalness(value):
            return 8 if value < 0.25 else 4 if 0.25 <= value < 0.5 else 10 if 0.5 <= value < 0.75 else 0

        def score_liveness(value):
            return 10 if value < 0.8 else 0

        def score_tempo(value):
            return 7 if 130 <= value <= 180 else 10 if 80 <= value < 130 else 4 if value < 80 else 0

        total_score = 0
        #go through the audio features of tracks
        for i in json_format["audio_features"]:
            #to skip tracks that came back with NoneType because the Id was wrong
            if i:
                #Calculate score based on average of feature values
                score = (
                    score_danceability(i["danceability"]) +
                    score_energy(i["energy"]) +
                    score_speechiness(i["speechiness"]) +
                    score_acousticness(i["acousticness"]) +
                    score_instrumentalness(i["instrumentalness"]) +
                    score_liveness(i["liveness"]) +
                    score_tempo(i["tempo"])
                    # Add calls to other scoring functions for remaining features...
                )

                total_score += (score/7)

        #print(total_score)
        return total_score

# main
def main():
    st.title("Ranker")
    artists_albums_tracks = {}

    # get access token
    access_token = get_access_token()
    #print(access_token)
    user_input = st.text_input("Enter Artist Name") #text box search for artist

    #when artist name searched
    if user_input:

        #display options for user to choose from
        artist = get_artist(user_input, access_token)
        # print("artist ids: ", artist)

        sorted_descending_score = []

        # when artist chose rank albums
        if st.button("Rank Albums"):

            #show loading spinner until until the process is done
            with st.spinner(text="In progress..."):
                albums = get_artists_albums(access_token, artist) # returns dict of artists album names as keys and album id as value
                #albums = get_artists_albums(access_token, "5mZLaYqN0ZkjxfeUUmiuq")
                #print("Albums ids: ", albums, end = '\n\n')
                album_scores = {}
                #album_tracks = get_album_tracks(access_token, albums["Donda (Deluxe)"])

                # #for loop that goes through albums dict keys which are album names
                # #and also have values that can be accessed which are album ids
                for i in albums:
                    #print(i)
                    #get an albums
                    album_tracks = get_album_tracks(access_token, albums[i]) #returns a list of album tracks ids
                        #print("Album tracks: ", album_tracks, end = '\n\n')
                    album_size = len(album_tracks) # the albums size

                    if album_size != 0:
                        artists_albums_tracks[i] = album_tracks #create a dict of lists; key= album_name, value = list of albums tracks
                        

                        scores_of_all_album_tracks = tracks_likeability(access_token, artists_albums_tracks[i])

                        #stores album average score in dict with the key being the albums name
                        album_scores[i] = scores_of_all_album_tracks / album_size

                      # here the dictionary is sorted according to score from highest score to lowest
                      # where the .item() returns a list of tuples and the for loop goes through each item
                      # where the lambda sorts according to the second value of the tuple which is the value of the dict

                #display albums and their scores in descending order and write it
                for album in sorted(album_scores.items(), key=lambda item: item[1], reverse = True):
                    sorted_descending_score.append(album[0] + "  " + f"{album[1]}")

                st.write(sorted_descending_score)




if __name__ == "__main__":
    main()
