 # Spotify Ranker
  #### Video Demo:  <https://youtu.be/R6aT9UI27AY>
  #### Description:
  # Purpose:
  This project creates a python and streamlit web app that accesses spotify data through spotify API and manipulates the data for display. The aim is to create an app that ranks an artists albums according to an algorithm of my making. This is a personal project and for the moment serves the purpose of the developer as the algorithm cannot be adjusted for different tastes and is built according to that of the users, however, it is built in a way where it can easily be adjusted in the future to include that.

  # Development stage:
  ## Setup the project
  The first step is setting up a python project and importing streamlit for UI. As soon as you run the project the first time using the command `streamlit run “filename”` it will display a URL in the CLI to access the web page of the app which will also be used setting up the app on the developers page on spotify.

  The developers page must be setup to access the API by generating an access token. The web page developer.spotify.com is accessed through a web browser, an account is logged into and the overview option is chosen from the side menu where the page will look as follows:



  ![developers.spotify.com Overview page with sidebar showing](Overview.png)


  The steps under “Getting started” are followed which will take the developer to dashboard where they press create an app and are presented with the following text fields to fill:

  ![Form that has to be filled to create an app connected to spotify API](spotify_create_app_form.png)

  For the website field in the photo above, the app URL from the first step is used, and in this case the developer does not have a redirect URI, so `{{EDUCATIVE_LIVE_VM_URL}}/callback`is used instead, which works as an alternative. This gives the developer access to the client ID and client secret for their project by accessing through the websites dashboard.

  ## Authorization
  The authorization chosen is the client credentials flow which is the simplest because the program does not need advanced authorization. You can read about different authorization methods [here](https://developer.spotify.com/documentation/web-api/concepts/authorization). Client ID and Client Secret are used to get the access token by creating a function called `get_access_token()` which can be seen in more detail in the project file. This function creates a string from client ID and client secret then encodes it into utf-8 format then encode it using base64 library then decode it into utf-8 format again and using it in a request.post function which can be seen in more detail in the project file. This process returns the access token needed for the get requests to get access to API data. Below is an example of an authorization request in javascript.

  ![The authorization function to get the access token in javascript format](authorization_post_function.png)

  The documentation is the gateway to all the answers, you can see all the documentation in the spotify.developers page with access to all the documentation by accessing different sectors of the left sidebar. This provides access to documentation of different capabilities and what to avoid and more.

  ![Documentation details example showcasing the get artist page](documentation_details.png)

  The get section tells you what variables can be inserted into the get request, as seen below:

  ![Get request possible variables](get_section.png)

  The documentation for the response from that get request and the variables available in the response can be seen right below it, where 200 is if the request is valid and the rest of the numbers show documentation on different errors for example 401, 403, 429.


  ![Response variables and possible errors](get_section.png)


  ## Get Requests
  Now that the documentation has been discussed, remember once the access token function is set up the requests.get() function must be used to access data and you specify the data extracted by manipulating the URL(endpoint) of the website (this is how it is done for most APIs as well).

  ### Get Artist
  By accessing the documentation it can read how the URL must be modified for an API. For example for the Spotify get artists albums you can see the documentation [here](https://developer.spotify.com/documentation/web-api/reference/get-an-artists-albums), where the endpoint URL {id} must be replaced with the artists id to get artist albums. You can also make the URL return more specific data by adding ? followed by certain variables appointed values in the URL. For the get artist function these specific variables are `include_groups, market, limit, and offset`. All of which you can read about in the get artists name documentation. You can access an artist’s ID with the following steps:

1- Search artists name on spotify web.

  ![Artist spotify page example](artist_page.png)

  2-	Get the alphnum combination at the end of the URL.

  ![Artist ID example](Artist_id.png)

  The request.get() is then supplied with the URL and a map for the headers variable as follows:

  ![Authorization example](auth_example.png)
  And all album IDs are accessed and printed as follows:

  ![Accessing data from json format](access_data_example.png)
  Note that the print is replaced with a return most of the time.

  ### Search item
  However, it is more convenient if the artist can be accessed from the UI and the artists ID does not have to be searched for manually. This was done by allowing user input from streamlit UI library using st.text_input(). A “search for item” request is executed with the users input once it has been collected. We get the endpoint for that function from the documentation and add the user input to it (and this case more specific data using variables `limit` and `type`). Remember that is there is more than one variable you separate them using “&” for example `&type=artist&limit=4`). This will return the 4 top results of artists according to user input for the search.

  The options returned are displayed on the website using the `image_select()` function for the user to choose a specific artist from you can read about [here](https://github.com/jrieke/streamlit-image-select) and in more detail [here](https://image-select.streamlit.app/). The documentation makes it clear that a list of images url has to be supplied to the function to display and a list of the text you want under each of these images. Both are extracted from the json response by extracting the first image of each artist and inserting it in a list then their name and placing that in a separate list both of which are used in the `image_select()` function. In the case the artist does not have an image, a “NO IMAGE” image is inserted into the list for that artist, which was made on this site.

  From the options displayed, the user can choose the artist whose albums need to be ranked by clicking on his photo. This will cause the image_select() function to return the image url for the artist which can be used to extract the id for that artist, as a dict was made earlier where the key is the image of the url and the values are the artists’ id. Once the image is chosen and the image url is used to extract the id of the artist, the artist id is used as the return value of the function. By which point the process of ranking that artist’s albums starts as soon as the user presses the rank albums button. Until the process is done a loading spinner is displayed.

  ### Get artist's albums and Get albums' tracks id
  The process goes as follows, once the artist id is returned it is used to do the request for that artists’ albums but now much like th get reponse for the artist, we have the perk of letting the user choose the artist they want. Once the dict of album ids is returned it is used to perform another get request to get each albums tracks and extract each tracks id from the json. Every album’s tracks ids are all placed inside a list and that list is implemented as values in a dict where each list can be accessed by a key which would be the albums name. As soon as an albums list is created each element is inserted into a function that performs an evaluation of each track and grants it a score out of 10. The scales for the score are appointed by the developer keeping in mind what he prefers.

  ### Get the audio features
  The traits of a track are extracted by doing an audio features get request which returns a json with the tracks characteristics such as danceability, speechiness, etc.. Once a track is appointed a score it is added with all the other album track score and the average is calculated and stored inside a dict with the key being the albums name and the value the overall average score of that album. That is done for all albums then they are displayed in order from highest score to least.

  ## Design Choices
  When possible, batch API requests are implemented, which was a design choice in order to avoid exceeding rate limit. Batch APIs is requesting a batch of data at once for example get tracks' audio features instead of get track's audio features. This is important because rate limit depends on the amount of API requests done in a 30 seconds period. This is important step to avoid any problems with the app although it might make the code a bit more complicated to debug.


  The API requests were put in different functions to allow for more concise testing of the functionality. Placing them in one function makes it harder to test the code in detail and makes it harder to debug in case of an error occuring.

  ## Limitations
  The limitation of the process is the rate limit where there is a limit to the amount of times a user can do the requests and if the user uses the program too many times it stops. That is however not a big problem since this is a small program for now and has only one user(the developer). However, a prevention method was inserted in the code nonetheless where if the request returns a `429 error` (which is a rate limit) it does a `retry-after` function. A `retry-after` function retrys a function after a certain amount of time if it does not succeed the first time, the time set for the repetition is 100000 seconds.

  ## Testing
  Testing was conducted on project where the 4 functions `get_artist(), get_artists_albums(), get_album_tracks() and tracks_likeability()` were tested. After having some trouble for a while, I realized that I had to remove `__init__.py` file as it caused the program not recognize the functions.to go into more details the test conducted on the four functions:

  1- `get_artist()` try valid artist and trying a non-meaningful search

  2- `get_artists_albums()` try valid artist, try artist with zero albums, and try invalid artist id

  3- `get_album_tracks()` try valid request, try album with more than 40(the limit) tracks, try album with less than 5 tracks, and try invalid album id

  4- `tracks_likeability()` try couple of valid list of tracks and a track with an invalid track in between





