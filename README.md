# Python_FinalProject

This is Final Project for advanced programming in python course, this program can build a web server with login and coin pages, after successfully logged in, enter a coin name then after press check button in coin page, it will return a bunch of paragraph related to entered coin from coinmarketcap.com then get summary by summarizer also data will be saved in database

## Installation

Make sure that you have installed pyjwt, beautifulsoup4 , flask , sqlalchemy, psycopg2, tensorflow libraries and postgreSQL

```
pip install pyjwt

pip install beautifulsoup4

pip install Flask

pip install Flask-SQLAlchemy

pip install psycopg2-binary

pip install TensorFlow

```
Dowanload file and open FinalProject.py and make some changes
```
# connect to your database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yourUsername:yourPassword@localhost/yourDBName'
```

## Example

After launch FinalProject.py you will have a link in terminal

```
http://127.0.0.1:5000/                              -- default page
http://127.0.0.1:5000/login                         -- login page
http://127.0.0.1:5000/coin                          -- default coin page
http://127.0.0.1:5000/protected?token='tokenValue'  -- coin page with token
```
