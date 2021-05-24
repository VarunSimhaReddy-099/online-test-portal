from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pyrebase
import requests
import os
from dotenv import load_dotenv
load_dotenv()

config = {
    "apiKey": os.environ.get("API_KEY"),
    "authDomain": os.environ.get("AUTH_DOMAIN"),
    "databaseURL": os.environ.get("DATA_BASE_URL"),
    "storageBucket": os.environ.get("STORAGE_BUCKET"),
    "projectId": os.environ.get("PROJECT_ID"),
    "messagingSenderId": os.environ.get("MESSAGING_SENDER_ID"),
    "appId": os.environ.get("APP_ID")
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.sqlite3'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = os.environ.get("SECRET_KEY")
db = SQLAlchemy(app)


# <-------------------Creation of Db Model Questions with crct options table -------------------->

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column('q_no', db.Integer, primary_key=True)
    question = db.Column(db.Text)
    value_1 = db.Column(db.String(100))
    value_2 = db.Column(db.String(100))
    value_3 = db.Column(db.String(100))
    value_4 = db.Column(db.String(100))
    crct_option = db.Column(db.String(30))

    def __init__(self, question, value_1, value_2, value_3, value_4, crct_option):
        self.question = question
        self.value_1 = value_1
        self.value_2 = value_2
        self.value_3 = value_3
        self.value_4 = value_4
        self.crct_option = crct_option


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    score = db.Column(db.Integer)

    def __init__(self, name, score):
        self.name = name
        self.score = score


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    adminid = db.Column(db.Text)

    def __init__(self, adminid):
        self.adminid = adminid
# <--------------------------Index Route-------------------------->


@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('userDashboard'))
    elif 'email' in session and verifyAdmin(session['checkAdminId']):
        return redirect(url_for('list_questtions'))
    else:
        return render_template("index.html")


# <------------------Login Route---------------------------------------->
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if 'email' not in session:
            try:
                email = request.form['email']
                password = request.form['password']
                user = auth.sign_in_with_email_and_password(email, password)
                # print(user['email'])
                session['email'] = user['email']
                session['checkAdminId'] = user['localId']
                # print(user['localId'])
                return redirect(url_for('userDashboard'))
            except requests.HTTPError as exception:
                error = eval(exception.strerror)
                return render_template('login.html', error=error['error']['message'])
        else:
            return redirect(url_for('userDashboard'))
    if request.method == "GET" and 'email' in session:
        return redirect(url_for('list_questions'))
    return render_template('login.html')

# <-----------------------Route to Add the question ------------------>


@app.route('/add', methods=["GET", "POST"])
def add():
    try:
        if verifyAdmin(session['checkAdminId']):
            if request.method == "POST":
                formDetails = request.form.to_dict()
                # print(formDetails)
                submitted_question = Question(formDetails['question'], formDetails['value1'], formDetails['value2'],
                                              formDetails['value3'], formDetails['value4'], formDetails['crctOption'])
                db.session.add(submitted_question)
                db.session.commit()
                return redirect(url_for('add'))
            return render_template('add.html')
        else:
            return f"You are not a admin"
    except:
        return f"<h1>Please Login</h1>"

# <-------------------Display Question to the User ---------->


@app.route('/questions')
def list_questions():
    try:
        if verifyAdmin(session['checkAdminId']):
            return render_template('adminView.html', Questions=Question.query.all())
    except:
        pass
    if 'email' in session:
        Questions = Question.query.all()
        # print(session['email'])
        return render_template('view.html', Questions=Question.query.all())
    return redirect(url_for('index'))
# <----------------------------------- Validate Route to get Results------------------------->


@app.route('/validate', methods=["POST"])
def validate():
    if alreadySubmitted():
        result1 = User.query.filter_by(name=session['email']).first().score
        return render_template('userScore.html', result=result1, message="You have already submitted your answers once and scored", taketest=False)
    listOfQuestions = request.form.to_dict()
    #print("Answers received by Client ", listOfQuestions)
    # print("You have scored ", result(listOfQuestions))
    # {result(listOfQuestions)}
    return render_template('userScore.html', result=result(listOfQuestions), message="You have scored")
# <------------------------Check Already Added answers------------>


def alreadySubmitted():
    submittedStudents = User.query.filter_by(name=session['email']).first()
    if submittedStudents is not None:
        return True


@app.route('/user/dashboard')
def userDashboard():
    # print("Look at me++++++", session['checkAdminId'])
    if not verifyAdmin(session['checkAdminId']):
        return render_template('userDashboard.html', alreadySubmitted=alreadySubmitted())
    return redirect(url_for('list_questions'))
# <-----------------------------------method for Get Results------------------------->


def result(submitedByClient):
    Questions = Question.query.all()
    dic = {}
    count = 0
    for question in Questions:
        dic[str(question.id)] = question.crct_option

    # print(dic)
    # print(submitedByClient)
    try:
        for key, values in dic.items():
            if key not in submitedByClient:
                submitedByClient.update({key: '0'})
            if values == submitedByClient[key]:
                count += 1
        storeScore = User(session['email'], count)
        db.session.add(storeScore)
        db.session.commit()
        return count
    except:
        # print('Error occured !!! please enter all the answers.....')
        return f"<h1>Error occured !!! please enter all the answers.....</h1>"


# <<----------Simpler Version To Implement Admin Check-------------------------->

# def verifyAdmin(checkAdminId):
#     print(checkAdminId)
#     admin = False
#     if "WAQIm0svPRdmeBJEnLx38QxKVmM2" == checkAdminId:
#         admin = True
#     return admin
# <<<<<<<====================================================================>

# <<---------------Check Admin method via database -------------------------------------->
def verifyAdmin(checkAdminId):
    admin = False
    try:
        if Admin.query.filter_by(adminid=checkAdminId).first().adminid == checkAdminId:
            admin = True
    except:
        admin = False
    return admin


@app.route('/admin/createadmin', methods=["GET", "POST"])
def createAdmin():
    try:
        if verifyAdmin(session['checkAdminId']):
            if request.method == "POST":
                uniqueId = request.form['uniqueId']
                # print(uniqueId)
                db.session.add(Admin(uniqueId))
                db.session.commit()
                return render_template('createadmin.html', message="Admin has been created successfully")
            return render_template('createadmin.html')
        else:
            return f"You are not a admin"
    except:
        return f"<h1>Error Occured <br/> Please Login and try again</h1>"


# <------------------Admin View ------------------------------------>


@app.route('/admin/view', methods=["GET", "POST"])
def adminView():
    try:
        if verifyAdmin(session['checkAdminId']):
            if request.method == "POST":
                qNumber = int(request.form['qNumber'])
                # print(qNumber)
                question = Question.query.get(qNumber)
                db.session.delete(question)
                db.session.commit()
                return redirect(url_for('adminView'))
            return render_template('adminView.html', Questions=Question.query.all())
        else:
            return f"You are not a admin"
    except:
        return f"<h1>Please Login</h1>"


# <---------------------------Register Route ------------------------->

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'email' in session:
        return redirect(url_for('list_questions'))
    if request.method == "POST":
        try:
            email = request.form['email']
            password = request.form['password']
            success = auth.create_user_with_email_and_password(email, password)
            # print(success)
            return redirect(url_for('index'))
        except requests.HTTPError as exception:
            error = eval(exception.strerror)
            # print(error)
            return render_template('register.html', error=error['error']['message'])
    return render_template('register.html')


# <-----------------------LOGOUT Route -------------------------------->
@app.route('/logout')
def logout():
    if 'email' in session:
        session.clear()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


# <--------------------------view every one's score (admin) -------->
@app.route('/admin/view/scores')
def viewScore():
    try:
        if verifyAdmin(session['checkAdminId']):
            return render_template('viewScore.html', score=User.query.all())
    except:
        # score = User.query.all()
        # for scorer in score:
        #     print(scorer.name, scorer.score)
        pass
    return f"You are not an admin to access this page!!!"

# <----------------------Error Route ------------------------>


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html")


@app.route('/retake', methods=["POST"])
def retake():
    db.session.delete(User.query.filter_by(name=session['email']).first())
    db.session.commit()
    return redirect(url_for('list_questions'))


@app.route('/forgotpassword', methods=["GET", "POST"])
def forgotpassword():
    try:
        if request.method == "POST":
            email = request.form['email']
            user = auth.send_password_reset_email(email)
            print("success")
            return render_template('reset.html', error="Please check your email inbox/spam folder and follow the setps to reset password ")
    except requests.HTTPError as exception:
        error = eval(exception.strerror)
        return render_template('reset.html', error=error['error']['message'])
    return render_template('reset.html')


# <--------------Run App -------------------------------------------->
if __name__ == "__main__":
    app.run()
