# Sharing Moments🌅🎶

###### ----Sunrise & Sunset Spotify API Interface

**Spotify_flask_suntime** is a personalized music interface that integrates the **Spotify API** and **Sunrise & Sunset API**. This project allows users to create curated playlists tailored to their location and input hometown's sunrise and sunset times, bringing a connection between user's environment and music.

This project is based on the [Jiya_Spotify_API](https://github.com/JiyaZhang0306/Jiya_Spotify_API) .



### Contents:

1.Features

2.Setup

3.Interface

4.Conclusion



##  Features

- **Personalized Playlists**: Generate playlists that align with current location and hometown's sunrise and sunset times.

- **Dynamic API Integration**: Combines the Spotify API with the Sunrise & Sunset API for a seamless experience. Also use Google API to locate user's IP location and find the input address.

- **Flask**: Uses Flask to serve a user-friendly web interface.

- **Real-Time Location Support**: Fetch location data to customize playlists according to local solar events.

  

##  Installation & Setup

### Environments

- Python 3.7+
- Spotify Developer Account (for API credentials)
- Flask



### Keys Settings

Check  [Jiya_Spotify_API](https://github.com/JiyaZhang0306/Jiya_Spotify_API): API Setup



### Steps

1. **Set Up a Virtual Environment** :

   ```
   virtualenv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies**:

   ```
   pip install -r requirements.txt
   ```

3. **Run the Flask Application**:

   ```
   flask run
   ```

   Visit `http://127.0.0.1:5000` in your web browser to access the interface.



## Interface

The web interface provides an interactive user experience:

1. **Location-Based Customization**:
   - Automatically detects the user's location via browser permissions.
   - Displays the local sunrise and sunset times for reference.
2. **Enter Hometown City**
   - Allow users to enter hometown city at beginning to generate hometown playlists.
3. **Today's sunrise & sunset time**
   - Two separate sections show two cities sunrise and sunset time
4. **Playlist Generation**:
   - Two separate sections for **Sunrise Playlists** and **Sunset Playlists**.
   - Allows users to preview curated tracks and save the playlists directly to their Spotify account.



## Conclusion

**Spotify_flask_suntime** is a step towards creating a more personalized and immersive music experience, connecting users to their environment and their hometown through curated playlists based on sunrise and sunset times. 

Looking ahead, I plan to enhance the interface with more interactive and engaging features, including:

- **Time Difference Visualization**: Compare the sunrise and sunset times of two different cities to help users understand global time dynamics.
- **Real-Time Sunrise/Sunset Background**: Display live sunrise and sunset photos or dynamically adjust the background color to reflect the time of day.
- **Enhanced Playlist Customization**: Introduce more granular options for mood and genre selection based on user preferences.

Stay tuned for updates as I continue to develop and refine this project! Feel free to contribute your ideas or suggestions to make it even better. 😊