from kuso import MarkovChainer

with open("kuso.txt") as f:
    text = f.read()
    txts = text.split("\n")

mc = MarkovChainer(3, txts)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return mc.make_sentence()

if __name__ == '__main__':
    app.run()
