from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

responses = []

@app.route('/')
def index():
    title = "Customer Satisfaction Survey"
    instructions = "Please fill out a survey about your experience with us."
    return render_template('index.html', title=title, instructions=instructions)

