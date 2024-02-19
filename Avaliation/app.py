from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 comments TEXT,
                 rating INTEGER,
                 ratingFrontEnd INTEGER, 
                 ratingBackEnd INTEGER,
                 ratingStand INTEGER)''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    comments = request.form['comments']
    ratingFrontEnd = request.form['ratingFrontEnd']
    ratingBackEnd = request.form['ratingBackEnd']
    ratingStand = request.form['ratingStand']
    ratingProjeto = request.form['ratingProjeto']
    
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('INSERT INTO reviews (name, comments, ratingFrontEnd, ratingBackEnd, ratingStand, ratingProjeto) VALUES (?, ?, ?, ?, ?, ?)', (name, comments, ratingFrontEnd, ratingBackEnd, ratingStand, ratingProjeto))
    conn.commit()
    conn.close()

    return redirect(url_for('thank_you'))





@app.route('/thank_you')
def thank_you():
    return render_template('thanks.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
