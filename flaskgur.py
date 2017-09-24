from flask import Flask, request, g, redirect, url_for, abort, render_template, send_from_directory
from werkzeug.utils import secure_filename
from hashlib import md5
from PIL import Image
import os
import time
import psycopg2

DEBUG = False
BASE_DIR = '/var/www/flaskgur'
UPLOAD_DIR = os.path.join(BASE_DIR, 'pics')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DB_STRING = "dbname=fgschema user=fguser password=fgpw host=localhost"

app = Flask(__name__)
app.config.from_object(__name__)


# Make sure extension is in the ALLOWED_EXTENSIONS set
def check_extension(extension):
    return extension in ALLOWED_EXTENSIONS


def connect_db():
    return psycopg2.connect(DB_STRING)


# Return a list of the last 25 uploaded images	
def get_last_pics():
    g.cur.execute('select name, extension from fgPics order by id desc limit 25')
    filenames = [row[0] + '.' + row[1] for row in g.cur.fetchall()]
    return filenames


# Insert filename into database	
def add_pic(name, extension):
    g.cur.execute('insert into fgPics (name, extension) values (%s, %s)', (name, extension,))
    g.conn.commit()


# Generate thumbnail image
def gen_thumbnail(filename):
    height = width = 200
    original = Image.open(os.path.join(app.config['UPLOAD_DIR'], filename))
    thumbnail = original.resize((width, height), Image.ANTIALIAS)
    thumbnail.save(os.path.join(app.config['UPLOAD_DIR'], 'thumb_'+filename))


# Taken from flask example app
@app.before_request
def before_request():
    g.conn = connect_db()
    g.cur = g.conn.cursor()


# Taken from flask example app
@app.teardown_request
def teardown_request(_):
    cur = getattr(g, 'cur', None)
    conn = getattr(g, 'conn', None)
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def upload_pic():
    if request.method == 'POST':
        new_file = request.files['file']
        extension = None
        try:
            extension = new_file.filename.rsplit('.', 1)[1].lower()
        except IndexError:
            abort(404)
        if new_file and check_extension(extension):
            # Salt and hash the file contents
            name = md5(new_file.read() + str(round(time.time() * 1000))).hexdigest()
            filename = name + '.' + extension
            new_file.seek(0)  # Move cursor back to beginning so we can write to disk
            new_file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
            add_pic(name, extension)
            gen_thumbnail(filename)
            return redirect(url_for('show_pic', filename=filename))
        else:  # Bad file extension
            abort(404)
    else:
        return render_template('upload.html', pics=get_last_pics())


@app.route('/show')
def show_pic():
    filename = request.args.get('filename', '')
    return render_template('upload.html', filename=filename)


@app.route('/pics/<filename>')
def return_pic(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], secure_filename(filename))
