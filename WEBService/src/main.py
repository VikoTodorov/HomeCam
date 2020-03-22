from flask import *
import database 

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')


@app.route('/logout')
def logout():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)
