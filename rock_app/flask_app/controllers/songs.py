from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.song import Song
from flask_app.models.user import User


# Creating a new song

@app.route('/new')
def new_song():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_song.html', user=User.get_by_id(data))

@app.route('/create_song', methods = ['POST'])
def create_song():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Song.validate_song(request.form):
        return redirect('/new')
    data = {
        "band": request.form["band"],
        "released_on": request.form["released_on"],
        "album": request.form["album"],
        "genre": request.form["genre"],
        "song": request.form["song"],
        "lyrics": request.form["lyrics"],
        "video": request.form['video'],
        "user_id": session["user_id"]
    }
    # pic_filename = secure_filename("image".filename)
    Song.save_song(data)
    return redirect('/dashboard')

# Reading a song

@app.route('/one_song/<int:song_id>')
def one_song(song_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': song_id,

    }
    one_song = Song.get_one_song(data)
    print(one_song)
    return render_template('single_song.html', one_song = one_song)

# Update a song

@app.route('/edit/<int:song_id>')
def edit_song(song_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data_song = {
        'id': song_id
    }
    user_data = {
        "id":session['user_id']
    }
    this_user = User.get_by_id(user_data)
    one_song = Song.get_one_song(data_song)
    return render_template('edit_song.html', one_song = one_song, this_user = this_user)

@app.route('/update_song/<int:song_id>', methods = ['POST'])
def update_one_song(song_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Song.validate_song(request.form):
        return redirect(f'/edit/{song_id}')
    data = {
        'id': song_id,
        "band": request.form["band"],
        "released_on": request.form["released_on"],
        "album": request.form["album"],
        "genre": request.form["genre"],
        "song": request.form["song"],
        "lyrics": request.form["lyrics"]
    }
    Song.update_song(data)
    return redirect(f'/one_song/{song_id}')

# Destroy a song

@app.route('/destroy_song/<int:song_id>')
def destroy_song(song_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': song_id
    }
    Song.delete_song(data)
    return redirect('/dashboard')
