from flask import *
import database 

from user import User


app = Flask(__name__)


@app.route('/', endpoint="index")
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        if request.form['fname'] != "" and request.form['lname'] != "" and \
        request.form['email'] != "" and request.form['psw'] != "":
            user = User.find_user(request.form['email'])
            if not user:
                values = (None, request.form['fname'],
                          request.form['lname'],
                          request.form['email'],
                          request.form['password'])
                user(*values).create()
                session[request.form['email']] = values[1]
                return redirect(url_for('homepage'))
            else:
                return render_template('register.html', error="You can't use \
                                       that email")
        else:
            return render_template('register.html', error="You can't use \
                                  that email")


@app.route('/homepage', endpoint= "homepage")
def homepage():
    if user.getEmail() in session:
        return render_template('homepage.html')
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)
