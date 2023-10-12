from crypt import methods

from torch import mul
from flask import Flask, render_template, request, session, redirect, url_for
import csv
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

app.config['UPLOAD_FOLDER'] = 'multimedia'

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'mp3']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_flashcards(filename='flashcards.csv'):
    cards = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cards.append({
                'id': len(cards),
                'question': row['question'],
                'answer': row['answer'],
                'choices': row['choices'].split(';')
            })
    return cards

def save_flashcard(question, answer, choices, filename='flashcards.csv'):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([question, answer, ";".join(choices)])

def load_multimedia(filename='multimedia.csv'):
    multimedia = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            multimedia.append({
                'id': len(multimedia),
                'file_type': row['file_type'],
                'file_name': row['file_name']
            })
    return multimedia

def save_multimedia(file_type, file_name, filename='multimedia.csv'):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([file_type, file_name])

@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create_flashcard', methods=['POST'])
def create_flashcard():
    question = request.form['question']
    answer = request.form['answer']
    choices = request.form.getlist('choices')
    save_flashcard(question, answer, choices)
    return redirect(url_for('select'))

@app.route('/create_multimedia', methods=['POST'])
def create_multimedia():
    file = request.files['file']
    if file and allowed_file(file.filename):
        file_name = file.filename
        file_type = file_name.split('.')[-1]
        save_multimedia(file_type, file_name)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename));
    return redirect(url_for('select'))

@app.route('/select')
def select():
    flashcards = load_flashcards()
    multimedia = load_multimedia()
    return render_template('select.html', flashcards=flashcards)

@app.route('/add_to_base', methods=['POST'])
def add_to_base():
    flashcards = load_flashcards()
    selected_ids = request.form.getlist('selected')
    session['question_base'] = [flashcards[int(i)] for i in selected_ids]
    session['current_index'] = 0
    session['correct_answers'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'current_index' not in session or session['current_index'] >= len(session['question_base']):
        return render_template('result.html', correct=session['correct_answers'], total=len(session['question_base']))

    current_flashcard = session['question_base'][session['current_index']]
    if request.method == 'POST':
        if request.form.get('choice') == current_flashcard['answer']:
            session['correct_answers'] += 1
        session['current_index'] += 1
        return redirect(url_for('quiz'))

    return render_template('quiz.html', 
                           flashcard=current_flashcard, 
                           progress=session['current_index'], 
                           total=len(session['question_base']),
                           correct=session['correct_answers'])

if __name__ == '__main__':
    app.run(debug=True)