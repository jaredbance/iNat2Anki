from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
from flask import Flask, render_template, request
import io
import sys
import flashcardMaker
from flashcardMaker import mycoMatchFields
import webbrowser
from threading import Timer
import killport
import os
import signal

app = Flask(__name__)
socketio = SocketIO(app)

processing = False

def background_task():
    captured_output = io.StringIO()
    sys.stdout = captured_output
    while True:
        time.sleep(0.1)
        output = captured_output.getvalue()
        socketio.emit('update', {'data': output})

@app.route('/')
def index():
  return render_template('index.html')

@socketio.on('submit_input')
def handle_input(data):
    global processing
    if processing:
        print("<span style='color:red;inline'>YOU CAN ONLY PROCESS ONE REQUEST AT A TIME</span>")
        return
    processing = True
    with open('input.txt', 'w') as f:
      f.write(data['text'])
    flashcardMaker.run()
    processing = False

def open_browser():
  webbrowser.open_new("http://127.0.0.1:5000")

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    os.kill(os.getpid(), signal.SIGTERM)

if __name__ == '__main__':
    killport.kill_ports(ports=[5000])
    # Start the background task
    thread = threading.Thread(target=background_task)
    thread.start()
    Timer(1, open_browser).start()
    socketio.run(app, debug=False)
