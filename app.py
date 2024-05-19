from flask import Flask, render_template,request,redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG'] = True

responses_key = "responses"
debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """Choose a survey."""
    return render_template("start_survey.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear all the responses from the session"""
    session[responses_key]= []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save the response from the taker and move them to the next question"""

    #this line of code gets the answer that the person put in 
    choice=request.form['answer']

    #this line takes responses and connects it to this users "sesion" so they could store the users answers
    responses = session[responses_key]
    #this line of code takes the users choice and adds it to respnses
    responses.append(choice)
    #this line of code updates responses of this users session
    session[responses_key]= responses

    #this if statement checks to see if after this anser that the use inputs if there are more question to the surevy or if he completed it redirects him to complete page
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route("/questions/<int:qid>")
def show_question(qid):
    responses = session.get(responses_key)

    if (responses is None):
        return redirect("/")

    # this if statement will redirect the user to the complete page of the number of responses he gave equals the number of question (i.e. - he completed the surevy)
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question= survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """this is the survey complete route - the page that will show when surevy is complete!"""

    return render_template("completion.html")