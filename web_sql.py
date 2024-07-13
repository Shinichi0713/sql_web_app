from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chinook.db'  # SQLiteデータベースを使用
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    director = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)

@app.route('/movies', methods=['POST'])
def add_movie():
    movie_data = request.get_json()
    new_movie = Movie(title=movie_data['title'], director=movie_data['director'], genre=movie_data['genre'])
    db.session.add(new_movie)
    db.session.commit()
    return {'id': new_movie.id}

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return {'movies': [{ 'title': movie.title, 'director': movie.director, 'genre': movie.genre } for movie in movies]}

@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    movie_data = request.get_json()
    movie = Movie.query.get(id)
    if 'title' in movie_data:
        movie.title = movie_data['title']
    if 'director' in movie_data:
        movie.director = movie_data['director']
    if 'genre' in movie_data:
        movie.genre = movie_data['genre']
    db.session.commit()
    return {'message': 'Movie updated'}

@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return {'message': 'Movie deleted'}

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)