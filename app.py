from flask import Flask, render_template, redirect, url_for
import os
import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
import sqlite3
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkeyornot'

# Main

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    learn = conn.execute('SELECT * FROM learn').fetchall()
    df = pandas.read_sql("select * from learn", conn)
    print(df)
    conn.close()
    return render_template("index.html", learn=learn)

@app.route('/xd')
def xd():
    return render_template("xd.html")

# Forms

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com" and login_form.password.data == "12345678":
            return redirect(url_for("learn"))
        else:
            return render_template("denied.html")
    return render_template("login.html", login_form=login_form)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/learn', methods=["GET", "POST"])
def learn():

    form = X()
    if form.validate_on_submit():
                
        my_learn = form.my_learn.data
        string = '{}\n'.format(my_learn)
        conn = get_db_connection()
        conn.execute('INSERT INTO learn (title, content) VALUES (?, ?)', ('Jak mi dzisiaj idzie:', string))
        conn.commit()
        conn.close()

        return redirect( url_for('form_result'))

    return render_template("learn.html", form=form)
        

@app.route('/music', methods=["GET", "POST"])
def music():

    form = Y()
    if form.validate_on_submit():
        
        music_link = form.music_link.data
        string = '{}\n'.format(music_link)
        save_data(string)

        return redirect( url_for('form_result'))

    return render_template("music.html", form=form)

@app.route('/form_result')
def form_result():
    return render_template("form_result.html")


# Helpers

def save_data(string):
    
    if not 'dane' in os.listdir():
        os.mkdir('dane')
        if not 'notatnik.txt' in os.listdir('dane'):
             os.system('touch notatnik.txt')
            
    with open('dane/notatnik.txt', "a+") as f:
        f.write(string)


# Errors

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500


# Form

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log In")


class X(FlaskForm):
    x_options = [
            ('Okropnie','Okropnie'),
            ('Słabo','Słabo'),
            ('Dobrze','Dobrze'),
            ('Super','Super'),
    ]

    my_learn = SelectField('Jak mi dzisiaj idzie:', choices=x_options)

    button = SubmitField('Wyślij')

class Y(FlaskForm):
    
    music_link = StringField('Link do dobrej muzyki:', validators=[DataRequired()])
    button = SubmitField('Wyślij')

if __name__=="__main__":
    app.run(debug=True)
