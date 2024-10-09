# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from class_data import Class
import threading
from telegram_bot import start_telegram_bot, send_message
import time
import state

app = Flask(__name__)

lecture3 = Class("lecture_list.csv")

def start_bot():
    start_telegram_bot(lecture3)

telegram_thread = threading.Thread(target=start_bot)
telegram_thread.daemon = True
telegram_thread.start()

@app.route('/')
def index():
    return render_template('index.html', students=lecture3.data.reset_index().to_dict('records'))

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    lecture3.add_person(name)
    return redirect(url_for('index'))

@app.route('/remove_student', methods=['POST'])
def remove_student():
    name = request.form.get('name')
    try:
        lecture3.remove_person(name=name)
    except Exception as e:
        print(e)
    return redirect(url_for('index'))

@app.route('/volunteer', methods=['POST'])
def volunteer():
    name = request.form.get('name')
    try:
        lecture3.volunteer(name=name)
        send_message(f"Volunteered: {name}")
    except Exception as e:
        print(e)
    return redirect(url_for('index'))

@app.route('/select_student', methods=['POST'])
def select_student():
    if state.selection_in_progress:
        return jsonify({'status': 'Selection already in progress'})

    state.selection_in_progress = True
    time.sleep(2)
    state.selected_student = lecture3.choose_random()
    state.selection_in_progress = False
    send_message(f"Selected student: {state.selected_student}")
    return jsonify({'selected_student': state.selected_student})

@app.route('/get_students')
def get_students():
    return jsonify({'students': lecture3.data.reset_index().to_dict('records')})

@app.route('/status')
def status():
    return jsonify({
        'selection_in_progress': state.selection_in_progress,
        'selected_student': state.selected_student
    })
    
@app.route('/animate_selection', methods=['POST'])
def animate_selection():
    selected_student = request.json.get('selected_student')
    if selected_student:
        state.selected_student = selected_student
        return jsonify({"status": "success", "selected_student": selected_student})
    return jsonify({"status": "error", "message": "No student provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
