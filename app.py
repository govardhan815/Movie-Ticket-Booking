from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'adminsecretkey'

def init_db():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        movie TEXT,
        seats INTEGER,
        timeslot TEXT
    )""")
    conn.commit()
    conn.close()

movies = {
    "Devara": "https://pbs.twimg.com/media/GGdZwHjXEAAHMzs.jpg",
    "Pokiri": "https://i.ytimg.com/vi/w4l6yDmoepA/maxresdefault.jpg",
    "Bahubali": "https://m.media-amazon.com/images/I/71i8a-PnChL._UF1000,1000_QL80_.jpg",
    "RRR": "https://upload.wikimedia.org/wikipedia/en/d/d7/RRR_Poster.jpg",
    "Kingdom": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXqYxNRbuH13Cl0xnS1d78zvppTZuH8986nQ&s",
    "War": "https://m.media-amazon.com/images/M/MV5BNjY5OTg4NTYtZjVkZS00YTZmLWIwNDEtM2Y0ODQyMzM2NTJiXkEyXkFqcGc@._V1_.jpg",
    "Eega": "https://m.media-amazon.com/images/M/MV5BMTA0MDFmMDMtMTE5OC00YWQ0LWIwZTUtOWIwMjk4Yjc3NGY1XkEyXkFqcGc@._V1_.jpg",
    "War2": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRtqormZphfLK5O4SdlhddPAFlaHojQ_sjl9w&s",
    "Guntur Karam": "https://i.redd.it/4pokemhpc2hb1.jpg",
    "Maharshi": "https://upload.wikimedia.org/wikipedia/en/thumb/3/37/Maharshi_poster.jpg/250px-Maharshi_poster.jpg",
    "Hit": "https://upload.wikimedia.org/wikipedia/en/1/12/HIT_The_First_Case.jpg",
    "Srimanthudu": "https://upload.wikimedia.org/wikipedia/en/thumb/8/87/Srimanthudu_poster.jpg/250px-Srimanthudu_poster.jpg",
    "Khaleja": "https://sund-images.sunnxt.com/10412/1600x1200_Khaleja_10412_ea25451b-7549-42c4-abcd-0b26f968dc06.jpg",
    "Businessman": "https://w0.peakpx.com/wallpaper/485/997/HD-wallpaper-mahesh-babu-businessman-charming-handsome-handsomehunk-maheshbabu-prince-stylish-superstar-tollywood.jpg",
    "Athadu": "https://m.media-amazon.com/images/M/MV5BYzU5YmY2NzQtZTVhZS00ZDQyLWI1YTQtZTI4MzYxOTcxMmM3XkEyXkFqcGc@._V1_.jpg",
    "Dookudu": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHqjmRioTr9e9SSycfKSnncoJTeFHXy_AAAA&s"
}


@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/book/<movie>', methods=['GET', 'POST'])
def book(movie):
    if request.method == 'POST':
        name = request.form['name']
        seats = request.form['seats']
        timeslot = request.form['timeslot']
        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, movie, seats, timeslot) VALUES (?, ?, ?, ?)",
                  (name, movie, seats, timeslot))
        conn.commit()
        conn.close()
        return render_template('success.html', movie=movie)
    return render_template('book.html', movie=movie)

@app.route('/view')
def view():
    if not session.get('admin'):
        return redirect('/admin')
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return render_template('view.html', bookings=bookings)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['username'] == 'govardhan' and request.form['password'] == 'govardhan@5c7':
            session['admin'] = True
            return redirect('/view')
        else:
            return "Invalid credentials"
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
