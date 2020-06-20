from flask import Flask, flash, render_template, request, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from passlib.hash import sha256_crypt

jali = Flask(__name__)

#Config MYSQL
jali.config['MYSQL_HOST'] = 'localhost'
jali.config['MYSQL_USER'] = 'root'
jali.config['MYSQL_PASSWORD'] = '12345678'
jali.config['MYSQL_DB'] = 'jalibaba'
jali.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MySQL

mysql = MySQL(jali)





@jali.route('/')
def home():
    return render_template('home.html')

@jali.route('/bawal')
def bawal():
    return render_template('bawal.html')

@jali.route('/photos')
def photos():
    return render_template('photos.html')

class RegisterForm(Form):
    name = StringField(u'Name', [validators.length(min=1, max=50)])
    username = StringField(u'Username', [validators.length(min=3, max=30)])
    email = StringField(u'Email', [validators.length(min=6, max=50)])
    password = PasswordField(u'Password', [
        validators.data_required(),
        validators.EqualTo(u'confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirm Password')

@jali.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create the cursor
        
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(username, name, email, password) VALUES(%s, %s, %s, %s)", (username, name, email, password))

        #Commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('You\'re now registered and can login.', 'success')

        redirect(url_for('login'))
        
        return render_template('register.html',form = form)
    return render_template('register.html',form = form)
@jali.route('/login')
def login():
    return render_template('login.html')

@jali.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@jali.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    return "The email is {} and the password is {}".format(email,password)



if __name__  == '__main__':
    jali.secret_key = 'secret123'
    jali.run(debug = True)
