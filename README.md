 # Spotify Ranker
  #### Video Demo:  <https://youtu.be/R6aT9UI27AY>
  ## Purpose:
  Creating a python and streamlit web app that accesses spotify data through spotify API and manipulates the data for display. The aim is to create an app that ranks an artists albums according to an algorithm of my making. This is a personal project and for the moment serves the purpose of the developer as the algorithm cannot be adjusted for different users tastes and is built according to that of the developer, however, the code was written in a way where it can easily be adjusted in the future to enable it to be adjusted to different users tastes.

  ## Overview
  This project is a Streamlit application that interacts with the Spotify API to search for artists, retrieve their albums, and evaluate the likeability of their albums based on audio features. It allows users to search for an artist, select from the returned results, view the artist's albums, and then see a ranked list of these albums based on a custom likeability score.

  ## Features
  - Search for artists using the Spotify API.
  - Choose from top results using selectable images.
  - Select an artist and their albums are returned ranked from best to worse based on a calculated likeability score.

  ## Installation
  To run this application, you'll need Python installed on your system. After cloning the repository, install the required dependencies:
 
  ```bash
  pip install -r requirements.txt
  ```
  ## Usage
  Before running the application, set up your Spotify API credentials. Create a .env file in the root directory and add your Spotify CLIENT_ID and CLIENT_SECRET:

  ```env
  CLIENT_ID=your_spotify_client_id
  CLIENT_SECRET=your_spotify_client_secret
  ```

  To start the Streamlit application, run:

  ```bash
  streamlit run project.py
  ```
  ## API Endpoints Used
  - Get Artist's Albums: https://api.spotify.com/v1/artists/{id}/albums
  - Search for Artist by ID: https://api.spotify.com/v1/search?q={query}&type=artist
  - Get Album's Tracks: https://api.spotify.com/v1/albums/{id}/tracks
  - Get Tracks' Audio Features: https://api.spotify.com/v1/audio-features?ids={ids}

  ## Functionality
  1. Get Access Token: Authenticate with the Spotify API.
  2. Artist Search: Search for artists based on user input.
  3. Artist Selection: Display artist images and names for selection.
  4. Album Retrieval: Get albums of the selected artist.
  5. Track Retrieval: Retrieve tracks from the selected album.
  6. Likeability Score Calculation: Evaluate albums based on audio features.

  ## Limitations
  The limitation of the process is the rate limit where there is a limit to the amount of times a user can do the requests and if the user uses the program too many times it stops. That is however not a big problem since this is a small program for now and has only one user(the developer). However, a prevention method was inserted in the code nonetheless where if the request returns a `429 error` (which is a rate limit) it does a `retry-after` function. A `retry-after` function retrys a function after a certain amount of time if it does not succeed the first time, the time set for the repetition is 100000 seconds.

  ## Note
  The application uses Spotify API, which requires an access token that expires periodically.
  Always keep your Spotify CLIENT_ID and CLIENT_SECRET confidential.

  ## Author
  Laith AL Far





