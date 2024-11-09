from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector # type: ignore

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',        # Your MySQL host, usually localhost
        user='root',    # Your MySQL username
        password='root', # Your MySQL password
        database='music_db'      # Your database name
    )
    return conn

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', user=session['user_name'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        conn.close()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Music Library Endpoint
@app.route("/library")
@app.route('/library', methods=['GET', 'POST'])
def library():
    if 'user_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            title = request.form['title']
            artist = request.form['artist']
            album = request.form['album']
            year = request.form['year']
            genre = request.form['genre']
           

            
        # Get all songs from the database
        cursor.execute('SELECT * FROM songs')
        songs = cursor.fetchall()
        conn.close()

        return render_template('library.html', songs=songs)
    
    
    return redirect(url_for('login'))
  
@app.route('/artist')
def artist():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT artist_id, artist_name, debut_year FROM artist')  # Querying the 'artist' table
    artists = cursor.fetchall()  # Fetching data as 'artists' to match template context
    conn.close()
    return render_template('artist.html', artists=artists)



@app.route('/album')
def album():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT album_id, title, release_date FROM album')  # Querying the 'album' table
    albums = cursor.fetchall()  # Storing data as 'albums' to match the template
    conn.close()
    return render_template('album.html', albums=albums)





    return redirect(url_for('login'))





if __name__ == '__main__':
    app.run(debug=True, port=3000)  # Enable debug mode
