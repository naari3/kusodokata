import os
from kuso import MarkovChainer
from flask import Flask, render_template, send_from_directory

with open("kuso.txt") as f:
    text = f.read()
    txts = text.split("\n")
mc = MarkovChainer(3, txts)
app = Flask(__name__)

@app.route('/')
def index():
    dokata = [mc.make_sentence() for i in range(3)]
    return render_template('index.html', dokata=dokata)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/x-icon')

if __name__ == '__main__':
    app.run()
