
from flask import Flask, flash, redirect, render_template, Response, request, session, url_for
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import os
import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# Disable TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
app = Flask(__name__)
# Set a secret key
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change to your database username
app.config['MYSQL_PASSWORD'] = 'password'  # Change to your database password
app.config['MYSQL_DB'] = 'moodmatch'

mysql = MySQL(app)



# Initialize Spotify API client
client_credentials_manager = SpotifyClientCredentials(client_id='b654b88b6ce043cc83b8e46dc7d493a4', client_secret='0394f353b6574c189ede048b699bbb55')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

face_classifier = cv2.CascadeClassifier(r'../app/static/haarcascade_frontalface_default.xml')
classifier = load_model(r'../app/static/model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)

captured_data = []
detected_emotions = set()

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
                    detected_emotions.add(label)
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

@app.route('/user')
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
    music_recommendations = []
    news_recommendations = []
    for emotion in detected_emotions:
        music_recommendations.extend(get_music_recommendations(emotion))
        news_recommendations.extend(get_news_recommendations(emotion))
    return render_template('music.html', music_recommendations=music_recommendations, news_recommendations=news_recommendations, emotions=detected_emotions)

@app.route('/stories')
def stories():
    if captured_data:
        latest_capture = captured_data[-1]
        news_recommendations = []
        for emotion in detected_emotions:
            news_recommendations.extend(get_news_recommendations(emotion))
        return render_template('story.html', news_recommendations=news_recommendations, emotions=detected_emotions)
    else:
        return "No captured data available."
@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'full_name' in request.form and 'email' in request.form and 'password' in request.form:
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()

        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not full_name or not email or not password:
            flash('Please fill out the form!')
        else:
            cursor.execute('INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)', (full_name, email, password,))
            mysql.connection.commit()
            flash('You have successfully registered!')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session['full_name'] = account['full_name']
            return redirect(url_for('index'))  # Redirect to index route after successful login
        else:
            flash('Incorrect email/password!')

    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('full_name', None)
    return redirect(url_for('login'))


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        fname = request.form['cfname']
        lname = request.form['clname']
        email = request.form['cemail']
        message = request.form['cmessage']

        # Insert form data into the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO contact (firstname, lastname, email, message) VALUES (%s, %s, %s, %s)', (fname, lname, email, message))
        mysql.connection.commit()
        cursor.close()

        # Optionally, you can redirect the user to a thank you page or back to the contact page
        flash('Your message has been sent successfully!')
        return redirect(url_for('index'))  # Assuming 'index' is the route to your home page

    

   

if __name__ == '__main__':
    if not os.path.exists('static/captured'):
        os.makedirs('static/captured')
    app.run(debug=True)