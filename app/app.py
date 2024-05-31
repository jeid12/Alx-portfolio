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
    query = f"{song_name} {artist} official audio"
    search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(search_url)
    video_link = search_url  # Simplified example
    return video_link

def get_music_recommendations(emotion):
    if emotion == 'Happy':
        playlist_id = '37i9dQZF1DXdPec7aLTmlC'
    elif emotion == 'Sad':
        playlist_id = '37i9dQZF1DX7qK8ma5wgG1'
    else:
        playlist_id = None

    if playlist_id:
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
                'youtube_link': youtube_link,
                'emotion': emotion
            })
        return recommendations
    else:
        return []

def get_news_recommendations(emotion):
    api_key = 'pub_4527685dd93bbe0abba82751512fa7eee9089'
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={emotion}"
    response = requests.get(url).json()
    articles = response.get('results', [])
    news_recommendations = []
    for article in articles:
        news_recommendations.append({
            'title': article['title'],
            'description': article['description'],
            'link': article['link']
        })
    return news_recommendations

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

                    timestamp = int(time.time())
                    img_path = os.path.join('static/captured', f'{timestamp}.jpg')
                    cv2.imwrite(img_path, frame)
                    captured_data.append((img_path, label))

                    recommendations = get_music_recommendations(label)
                    print(recommendations)
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

@app.route('/recommendations')
def recommendations():
    emotion = 'Happy'  # Default emotion for general recommendations
    music_recommendations = get_music_recommendations(emotion)
    news_recommendations = get_news_recommendations(emotion)
    return render_template('music.html', music_recommendations=music_recommendations, news_recommendations=news_recommendations)

@app.route('/stories')
def stories():
    if captured_data:
        latest_capture = captured_data[-1]
        emotion = latest_capture[1]
        news_recommendations = get_news_recommendations(emotion)
        return render_template('story.html', news_recommendations=news_recommendations, emotion=emotion)
    else:
        return "No captured data available."

if __name__ == '__main__':
    if not os.path.exists('static/captured'):
        os.makedirs('static/captured')
    app.run(debug=True)
