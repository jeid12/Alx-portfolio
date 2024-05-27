from flask import Flask, render_template, Response
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import os
import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Initialize Spotify API client
client_credentials_manager = SpotifyClientCredentials(client_id='b654b88b6ce043cc83b8e46dc7d493a4', client_secret='0394f353b6574c189ede048b699bbb55')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

face_classifier = cv2.CascadeClassifier(r'C:\Users\user\Desktop\Emotion_Detection_CNN-main\haarcascade_frontalface_default.xml')
classifier = load_model(r'C:\Users\user\Desktop\Emotion_Detection_CNN-main\model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)

captured_data = []
def get_youtube_link(song_name, artist):
    # You can use the YouTube Data API to search for the song
    # Here's a simplified example using YouTube's search URL
    query = f"{song_name} {artist} official audio"
    search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(search_url)
    # Parse the response to extract the YouTube video link
    # This can be more complex depending on the actual response format
    # For simplicity, let's assume the first video link is the one we want
    video_link = search_url  # Example link
    return video_link

def get_music_recommendations(emotion):
    # You need to define mappings from detected emotions to Spotify playlists or genres
    # This is a simplified example
    if emotion == 'Happy':
        playlist_id = '37i9dQZF1DXdPec7aLTmlC'  # Example: Happy playlist
    elif emotion == 'Sad':
        playlist_id = '37i9dQZF1DX7qK8ma5wgG1'  # Example: Sad playlist
    else:
        playlist_id = None  # You need to define other emotions
        
    if playlist_id:
        # Retrieve playlist tracks
        playlist_tracks = sp.playlist_tracks(playlist_id)
        recommendations = []
        for track in playlist_tracks['items']:
            song_name = track['track']['name']
            artist = track['track']['artists'][0]['name']
            album = track['track']['album']['name']
            youtube_link = get_youtube_link(song_name, artist)
            recommendations.append({
                'name': song_name,
                'artist': artist,
                'album': album,
                'youtube_link': youtube_link
        })
        return recommendations
    else:
        return []

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    prediction = classifier.predict(roi)[0]
                    label = emotion_labels[prediction.argmax()]
                    label_position = (x, y)
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Save the captured image and emotion
                    timestamp = int(time.time())
                    img_path = os.path.join('static/captured', f'{timestamp}.jpg')
                    cv2.imwrite(img_path, frame)
                    captured_data.append((img_path, label))

                    # Get music recommendations based on emotion
                    recommendations = get_music_recommendations(label)
                    print(recommendations)  # For testing
                else:
                    cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/captured')
def captured():
    return render_template('captured.html', captured_data=captured_data)

@app.route('/recommendations/<emotion>')
def recommendations(emotion):
    recommendations = get_music_recommendations(emotion)
    return render_template('music.html', recommendations=recommendations)

if __name__ == '__main__':
    if not os.path.exists('static/captured'):
        os.makedirs('static/captured')
    app.run(debug=True)
