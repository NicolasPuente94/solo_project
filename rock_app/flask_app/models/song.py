from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Song:
    db = "rock_app"

    def __init__(self, data):
        self.id = data['id']
        self.band = data['band']
        self.released_on = data['released_on']
        self.album = data['album']
        self.genre = data['genre']
        self.song = data['song']
        self.lyrics = data['lyrics']
        self.video = data['video']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.the_user = None #placeholder

    @classmethod
    def save_song(cls, data):
        query  = "INSERT INTO songs (band, released_on, album, genre, song, lyrics, video, user_id) VALUES (%(band)s, %(released_on)s, %(album)s, %(genre)s, %(song)s, %(lyrics)s, %(video)s, %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_one_song(cls, data):
        query = "SELECT * FROM songs WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        this_song = cls(results[0])
        this_song.the_user = user.User.get_by_id({'id':results[0]['user_id']})
        return this_song

    @classmethod
    def update_song(cls, data):
        query = "UPDATE songs SET band = %(band)s, released_on = %(released_on)s, album = %(album)s, genre = %(genre)s, song = %(song)s, lyrics = %(lyrics)s WHERE songs.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def delete_song(cls, data):
        query = "DELETE FROM songs WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
        
    @classmethod
    def get_all_songs_users(cls):
        query = "SELECT * FROM songs LEFT JOIN users ON users.id = user_id"
        results = connectToMySQL(cls.db).query_db(query)

        print(f"Results: {results}")

        all_songs = []
        for row in results:

            this_song = cls(row)

            user_info = {
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            this_user = user.User(user_info)

            this_song.the_user = this_user
            
            all_songs.append(this_song)
        return all_songs

    @staticmethod
    def validate_song(song):
        is_valid = True
        if len(song['band']) < 0:
            is_valid = False
            flash("Band must be greater than 0","song")
        if int(len(song['released_on'])) < 3:
            is_valid = False
            flash("Model must be at least 4 characters","song")
        if len(song['album']) < 3:
            is_valid = False
            flash("Album must be at least 4 characters","song")
        if len(song['genre']) < 0:
            is_valid = False
            flash("Genre must be greater than 0 characters","song")
        if len(song['song']) < 0:
            is_valid = False
            flash("Song must be greater than 0 characters","song")
        if len(song['lyrics']) < 9:
            is_valid = False
            flash("You shoud upload your lyrics","song")
        return is_valid
