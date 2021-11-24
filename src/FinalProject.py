import jwt
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from functools import wraps
from datetime import datetime, timedelta
import requests
import logging
from transformers import pipeline


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:er2003618@localhost/PythonFlask'

db = SQLAlchemy(app)

# summarizer
summarizer = pipeline('summarization')
article = '''
'''

# get summarized value
def get_summary(article):
    summary = summarizer(article, min_length=5, max_length=20, do_sample=False)
    # get first value
    return summary[0]['summary_text']

# coin table
class Coin(db.Model):
    __tablename__ = 'coin'

    id = db.Column('id', db.Integer, primary_key=True)
    coin_name = db.Column('coin_name', db.Unicode)
    text = db.Column('paragraph', db.TEXT)

    def __init__(self, id, coin_name, text):
        self.id = id
        self.coin_name = coin_name
        self.text = text

# user table
class User(db.Model):
    __tablename__ = 'user_table'
    id = db.Column('id', db.Integer, primary_key=True)

    login = db.Column('login', db.Unicode)

    password = db.Column('password', db.Unicode)

    token = db.Column('token', db.Unicode)

    def __init__(self, id, login, password, token):

        self.id = id

        self.login = login

        self.password = password

        self.token = token

# decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # request token value from url
        token = request.args.get('token')

        # if token is missing
        if not token:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        except Exception as e:
            logging.exception(e)
            return jsonify({'message': 'Hello, Could not verify the token'}), 403

        return f(*args, **kwargs)

    return decorated

# coin page
@app.route('/coin', methods=['POST', 'GET'])
@token_required
def coin():

    # tagArray for bs4 to db
    tagArray = []
    # summaryList for db to summarizer
    summaryList = []
    if request.method == 'POST':
        # request data from html
        inputCoin = request.form['coin']

        # get content of coin using bs4
        url = 'https://coinmarketcap.com/currencies/' + inputCoin + '/'
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        # save all paragraph of content in tagArray
        for tags in soup.find_all('p'):
             tagArray.append(tags.text)

        # save coin info to db
        obj = Coin.query.all()
        lastId = obj[-1].id
        #                  id       coin        text
        new_coin = Coin(lastId+1, inputCoin, tagArray)
        db.session.add(new_coin)
        db.session.commit()

        # get coin info from db
        coinInfo = Coin.query.filter_by(id=lastId+1).first()
        txt = coinInfo.text
        # split text into list
        lst = txt.split('","')

        # send every list element to summarizer
        for x in lst:
            summary = get_summary(x)
            # save summary into summaryList
            summaryList.append(summary)

        # combine two list become a tuple
        lst_tuple = list(zip(lst, summaryList))

        # send tuple to html
        return render_template('index.html', content=lst_tuple)
    else:
        return render_template('index.html')

# login page
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        # request value from html
        inputLogin = request.form['username']
        inputPassword = request.form['password']
        user = User.query.filter_by(login=inputLogin).first()
        # check
        if inputLogin == user.login and inputPassword == user.password:
            token = jwt.encode({'user': inputLogin, 'exp': datetime.utcnow() + timedelta(minutes=10)},
                                   app.config['SECRET_KEY'])
            # save token in db
            user.token = token
            db.session.commit()

            # turn to login page
            return redirect(url_for('coin', token=token))
        else:
            return render_template('login.html', content="The username or password was wrong")

    else:
        return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
