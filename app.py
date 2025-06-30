from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect('/products')
    else:
        return render_template('index.html', error="Invalid username or password")

@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    items = cursor.fetchall()
    conn.close()
    return render_template("products.html", username=session['username'], products=items)

if __name__ == '__main__':
    app.run(debug=True)
