from flask import Flask, render_template,request,redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey
app = Flask(__name__)

responses = []

from surveys import satisfaction_survey

@app.route('/')
def index():
    title = "Customer Satisfaction Survey"
    instructions = "Please fill out a survey about your experience with us."
    return render_template('index.html', title=title, instructions=instructions)

@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    if request.method == 'POST':
        answer = request.form.get('answer')
        responses.append(answer)
        next_question_id = question_id + 1
        if next_question_id < len(satisfaction_survey.questions):
            return redirect(url_for('question', question_id=next_question_id))
        else:
            return redirect(url_for('thank_you'))
    else:
        if question_id < len(satisfaction_survey.questions):
            current_question = satisfaction_survey.questions[question_id]
            question_text = current_question.question
            choices = current_question.choices
            return render_template('question.html', question_text=question_text, choices=choices)
        else:
            return "Invalid question ID"

@app.route('/thank_you')
def thank_you():
    return "Thank you for completing the survey!"


