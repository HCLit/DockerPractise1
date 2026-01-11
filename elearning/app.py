from flask import Flask, render_template, send_from_directory, url_for, redirect
from models import Course, Lesson
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os

app = Flask(__name__, static_folder='static')
BASE_DIR = Path(__file__).parent
DB_URL = os.environ.get('ELEARN_DB', 'sqlite:///elearning/elearning.db')

engine = create_engine(DB_URL, connect_args={})
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    session = Session()
    courses = session.query(Course).all()
    return render_template('index.html', courses=courses)

@app.route('/courses/<int:course_id>')
def course(course_id):
    session = Session()
    course = session.query(Course).get(course_id)
    if not course:
        return redirect('/')
    return render_template('course.html', course=course)

@app.route('/lessons/<int:lesson_id>')
def lesson(lesson_id):
    session = Session()
    lesson = session.query(Lesson).get(lesson_id)
    if not lesson:
        return redirect('/')
    return render_template('lesson.html', lesson=lesson)

@app.route('/static/courses/<path:filename>')
def course_static(filename):
    return send_from_directory(BASE_DIR / 'static' / 'courses', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5011)), debug=True)
