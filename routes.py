from flask import render_template, request, redirect, url_for, jsonify
from app import app, db
from models import Post, Event
from werkzeug.utils import secure_filename
import os

# Configure upload folder for images
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    posts = Post.query.all()
    events = Event.query.all()
    return render_template('index.html', posts=posts, events=events)

@app.route('/api/events')
def get_events():
    events = Event.query.all()
    events_list = [{"title": e.title, "start": e.date, "description": e.description, "image_url": e.image_url} for e in events]
    return jsonify(events_list)

@app.route('/admin', methods=['GET'])
def admin():
    posts = Post.query.all()
    events = Event.query.all()
    return render_template('admin.html', posts=posts, events=events)

@app.route('/admin/posts', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/events', methods=['POST'])
def add_event():
    title = request.form['title']
    date = request.form['date']
    description = request.form['description']
    image = request.files['image']

    # Save the image file if it's allowed
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_event = Event(title=title, date=date, description=description, image_url=filename)
        db.session.add(new_event)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_event/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('admin'))
