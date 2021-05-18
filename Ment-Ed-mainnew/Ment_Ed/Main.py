import time
import os
import smtplib, ssl
from itsdangerous import URLSafeTimedSerializer
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'the random string'
app.config['MAIL_DEFAULT_SENDER'] = 'mentedsupp@gmail.com'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_SSL']= False
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME'] = 'mentedsupp@gmail.com'
app.config['MAIL_PASSWORD'] = 'NPt-Lp}h=JKzW5J}'

db = SQLAlchemy(app)
mail= Mail(app)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])



#################### All the databases ################################
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    typeOfAccount = db.Column(db.String(10))
    credentials = db.Column(db.String(50))
    image = db.Column(db.String(50))
    about = db.Column(db.String(50))
    skills = db.Column(db.String(50))
    institute = db.Column(db.String(50))
    verifiedskills = db.Column(db.String(50))
    github = db.Column(db.String(50))
    linkedin = db.Column(db.String(50))
    score = db.Column(db.Integer, default=100)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(50))
    shortdescription = db.Column(db.String(200))
    detaileddescription = db.Column(db.String(200))
    pay = db.Column(db.Integer)
    tags=db.Column(db.String(50))
    status = db.Column(db.Integer, default='Pending')
    askedby_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    askedby_name = db.Column(db.String(200))
    askedby_img = db.Column(db.String(200))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(50))
    shortdescription = db.Column(db.String(200))
    detaileddescription = db.Column(db.String(200))
    pay = db.Column(db.Integer)
    tags=db.Column(db.String(50))
    status = db.Column(db.Integer, default='Pending')
    askedby_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    askedby_name = db.Column(db.String(200))
    askedby_img = db.Column(db.String(200))


class Certify(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate = db.Column(db.String(50))
    link = db.Column(db.String(200))
    askedby_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    askedby_name = db.Column(db.String(200))
    askedby_img = db.Column(db.String(200))

class SCertify(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate = db.Column(db.String(50))
    link = db.Column(db.String(200))
    askedby_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    askedby_name = db.Column(db.String(200))
    askedby_img = db.Column(db.String(200))


class Allresume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(200))
    
class ProfProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(50))
    shortdescription = db.Column(db.String(200))
    link = db.Column(db.String(200))
    pay = db.Column(db.Integer)
    tags=db.Column(db.String(50))
    askedby_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    askedby_name = db.Column(db.String(200))
    askedby_img = db.Column(db.String(200))

class SProfProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(50))
    shortdescription = db.Column(db.String(200))
    link = db.Column(db.String(200))
    pay = db.Column(db.Integer)
    tags=db.Column(db.String(50))
    askedby_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    askedby_name = db.Column(db.String(200))
    askedby_img = db.Column(db.String(200))


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    image = db.Column(db.String(50))
    description = db.Column(db.String(200))
    pay = db.Column(db.Integer)
    questionID = db.Column(db.Integer, db.ForeignKey('question.id'))


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    image = db.Column(db.String(50))
    description = db.Column(db.String(200))
    pay = db.Column(db.Integer)
    projectID = db.Column(db.Integer, db.ForeignKey('project.id'))

class Assigned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdbyId = db.Column(db.Integer, db.ForeignKey('user.id'))
    questionID = db.Column(db.Integer, db.ForeignKey('question.id'))
    assignedto_ID = db.Column(db.Integer, db.ForeignKey('user.id'))
    # To display the name of user and question in history section
    questionName = db.Column(db.String(200))
    assignedName = db.Column(db.String(200))

class Massigned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdbyId = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    projectID = db.Column(db.Integer, db.ForeignKey('project.id'))
    assignedto_ID = db.Column(db.Integer, db.ForeignKey('user.id'))
    # To display the name of user and question in history section
    projectName = db.Column(db.String(200))
    assignedName = db.Column(db.String(200))

class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    company = db.Column(db.String(200))
    credentials = db.Column(db.String(50))
    image = db.Column(db.String(50))
    roles = db.Column(db.String(50))

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    company = db.Column(db.String(200))
    credentials = db.Column(db.String(50))
    image = db.Column(db.String(50))
    roles = db.Column(db.String(50))
    score = db.Column(db.Integer, default=100)

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='Pending')
    date = db.Column(db.Integer)
    time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))
    # To display the name of user and question in history section
    username = db.Column(db.String(50))
    userabout = db.Column(db.String(50))
    recruitername = db.Column(db.String(50))

class Minterview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='Pending')
    date = db.Column(db.Integer)
    time = db.Column(db.Integer)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))
    # To display the name of user and question in history section
    username = db.Column(db.String(50))
    usercompany = db.Column(db.String(50))
    recruitername = db.Column(db.String(50))
################################  REGISTER  LOGIN  LOGOUT ROUTES ###################################

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('homepage.html')
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        data = User.query.filter_by(username=username,
                                    password=password).first()

        if data is not None:
            session['user'] = data.id
            print(session['user'])
            return redirect(url_for('index'))

        return render_template('incorrectLogin.html')

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

@app.route('/ConfirmEmail', methods=['GET', 'POST'])
def ConfirmEmail():
    if request.method == 'GET':
        return render_template('ConfirmEmail.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(username=request.form['username'],
                        password=request.form['password'], email=request.form['email'],
                         typeOfAccount=request.form['typeOfAccount'],
                        credentials=request.form['credentials'], institute=request.form['institute'],
                        skills=request.form['skills'], image=request.form['image'], 
                        about=request.form['about'],
                        github=request.form['github'], linkedin=request.form['linkedin'])

        db.session.add(new_user)
        db.session.commit()
        subject = "Confirm your email"
        token = ts.dumps(request.form['email'], salt='email-confirm-key')
        confirm_url = url_for('confirm_email',token=token,_external=True)
        template = render_template('/activate.html',confirm_url=confirm_url)
        send_email(request.form['email'], subject, template)
        return redirect(url_for('ConfirmEmail'))
    return render_template('register.html')

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return render_template('homepage.html')



###########Recruiter##################

@app.route('/Rlogin', methods=['GET', 'POST'])
def Rlogin():
    if request.method == 'GET':
        return render_template('Rlogin.html')
    else:
        username = request.form['username']
        password = request.form['password']
        data = Recruiter.query.filter_by(username=username,
                                         password=password).first()
        if data is not None:
            session['user'] = data.id
            print(session['user'])
            return redirect(url_for('Rindex'))

        return render_template('incorrectLogin.html')


@app.route('/Rregister/', methods=['GET', 'POST'])
def Rregister():
    if request.method == 'POST':
        new_recruiter = Recruiter(username=request.form['username'],email=request.form['email'],
                                  password=request.form['password'], company=request.form['company'],
                                  credentials=request.form['credentials'], image=request.form['image'],
                                  roles=request.form['roles'])

        db.session.add(new_recruiter)
        db.session.commit()
        subject = "Confirm your email"
        token = ts.dumps(request.form['email'], salt='email-confirm-key')
        confirm_url = url_for('confirm_email',token=token,_external=True)
        template = render_template('/activate.html',confirm_url=confirm_url)
        send_email(request.form['email'], subject, template)
        return redirect(url_for('ConfirmEmail'))
    return render_template('Rregister.html')


@app.route('/confirm/<token>')
def r_confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = Recruiter.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('Rlogin'))

@app.route('/Rlogout', methods=['GET', 'POST'])
def Rlogout():
    session.pop('username', None)
    print("session closed")
    return render_template('homepage.html')

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('homepage.html')

################################ Mentor ###############################
@app.route('/Mlogin', methods=['GET', 'POST'])
def Mlogin():
    if request.method == 'GET':
        return render_template('Mlogin.html')
    else:
        username = request.form['username']
        password = request.form['password']
        data = Mentor.query.filter_by(username=username,
                                         password=password).first()
        if data is not None:
            session['user'] = data.id
            print(session['user'])
            return redirect(url_for('Mindex'))

        return render_template('incorrectLogin.html')

@app.route('/Mregister/', methods=['GET', 'POST'])
def Mregister():
    if request.method == 'POST':
        new_mentor = Mentor(username=request.form['username'],email=request.form['email'],
                                  password=request.form['password'], company=request.form['company'],
                                  credentials=request.form['credentials'], image=request.form['image'],
                                  roles=request.form['roles'])

        db.session.add(new_mentor)
        db.session.commit()
        subject = "Confirm your email"
        token = ts.dumps(request.form['email'], salt='email-confirm-key')
        confirm_url = url_for('confirm_email',token=token,_external=True)
        template = render_template('/activate.html',confirm_url=confirm_url)
        send_email(request.form['email'], subject, template)
        return redirect(url_for('ConfirmEmail'))
    return render_template('Mregister.html')

@app.route('/confirm/<token>')
def m_confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = Mentor.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('Mlogin'))

@app.route('/Mlogout', methods=['GET', 'POST'])
def Mlogout():
    session.pop('username', None)
    return render_template('homepage.html')

######################################### CRUD Model ####################################

@app.route('/index')
def index():
    user_id = session['user']
    username = User.query.get(session['user']).username
    print('*' * 30)
    print('YOU ARE LOGGINED IN AS', username)  # All those print statments are for testing purpose. Ignore them
    print('*' * 30)
    flash("welcome {}".format(username))
    today = time.strftime("%m/%d/%Y")
    showQuestion = Question.query.order_by(desc(Question.id))
    rank_user = User.query.order_by(desc(User.score))
    interview = Interview.query.filter_by(user_id=user_id).filter_by(status='Confirmed').order_by(Interview.date).all()
    return render_template('index.html', showQuestion=showQuestion, rank_user=rank_user, interview=interview,
                           today=today)


# Route to add a new question
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = session['user']
        getTagsArrays=request.form.getlist('tags')
        t=''
        for eachTag in getTagsArrays:
            t += "      "
            t += eachTag
            t += "   |   "
        print('getTagsArrays',getTagsArrays, 'eachTag',t)
        print(user_id)
        new_question = Question(question=request.form['question'],
                                shortdescription=request.form['shortdescription'],
                                detaileddescription=request.form['detaileddescription'],
                                pay=request.form['pay'], tags=t, askedby_id=user_id,
                                askedby_name=User.query.get(user_id).username,
                                askedby_img=User.query.get(user_id).image)
        flash("New question has been succesfully added")
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('index'))

    else:
        return render_template('AddQuestion.html')


# In the index.html file, the entire question db will be displayed
# When the user clicks on view more btn, they would be redirected to the ParticularQuestion url
@app.route('/ParticularQuestion', methods=['GET', 'POST'])
def ParticularQuestion():
    if request.method == 'POST':
        id = request.args['questionid']
        username = User.query.get(session['user']).username
        image=User.query.get(session['user']).image
        
        new_response = Response(username=username,
                                description=request.form['description'],
                                pay=request.form['pay'], questionID=id, image=image)
        db.session.add(new_response)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        args = request.args
        print('args in q url is', args)
        questionid = Question.query.get(args['questionid'])
        # To check whether the user view the q is same as the user who raised that question. If True, then display assign tag
        isSamePerson = args['user']
        print(isSamePerson)
        user = questionid.askedby_id
        img = User.query.get(user).image
        username = User.query.get(user).username
        response = Response.query.filter_by(questionID=questionid.id).all()
        
        print("response is", response)
        return render_template('ParticularQuestion.html', question=questionid, username=username, img=img,
                               response=response,
                               isSamePerson=isSamePerson)


################################ My Questions Section ###################################

@app.route('/DoubtSolved')
def DoubtSolved():
    id = request.args
    print(id)
    q = Question.query.get(id)
    print(q.status)
    q.status = 'Solved'
    print(q.status)
    db.session.commit()
    return render_template('DoubtSolved.html', q=q)


@app.route('/Delete')
def Delete():
    id = int(request.args['id'])
    print('to be deleted ', id)
    obj = Question.query.filter_by(id=id).one()
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/assign')
def assign():
    qid = int(request.args['qid'])
    assignedto_ID = int(request.args['userid'])
    createdbyId = session['user']
    print('to be assign ', id)
    obj = Question.query.filter_by(id=qid).one()
    print('obj is', obj)
    print(obj.question)
    obj.status = 'Assigned'
    assign = Assigned(createdbyId=createdbyId, questionID=qid, assignedto_ID=assignedto_ID,
                      assignedName=request.args['assignedName'], questionName=request.args['questionName'])
    db.session.add(assign)
    db.session.commit()
    print('************* STATUS CHANGED TO ASSIGNED **************')
    return redirect(url_for('index'))


####################################  OTHER ROUTES  #########################################


@app.route('/payment')
def payment():
    details = request.args
    print(details)
    mentor = str(details['doubt'])
    print('m is', mentor)
    amt = details['amount']
    user_id = session['user']
    u = User.query.get(user_id)
    mentor = User.query.filter_by(username=mentor).first()
    topay = User.query.get(mentor.id)
    print('mentor is  ', topay)
    if u.score > 0:
        flash("Payment successully made")
        print(u.score)
        u.score = u.score - int(amt)
        topay.score += int(amt)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('4o4.html', display_content="Transcation unsuccessul due to lack of credits")


@app.route('/verifiedskills', methods=['POST', 'GET'])
def verifiedskills():
    if request.method == 'POST':
        points = 0
        result = request.form
        r1 = result['q1']
        r2 = result['q2']
        r3 = result['q3']
        r4 = result['q4']
        r5 = result['q5']

        if r1 == 'C':
            points += 20
        if r2 == 'A':
            points += 20
        if r3 == 'C':
            points += 20
        if r4 == 'B':
            points += 20
        if r5 == 'B':
            points += 20

        if points >= 60:
            userid = session['user']
            user = User.query.filter_by(id=userid).one()
            user.verifiedskills = 'javascript'
            db.session.add(user)
            db.session.commit()
        return render_template('quizResult.html', points=points)

    return render_template('quiz.html')


######################################### Routes to display ####################################

@app.route('/scoreBoard')
def scoreBoard():
    rank_user = User.query.order_by(desc(User.score))
    return render_template('scoreBoard.html', rank_user=rank_user)


# Shows the user profile of the user who is currently logged in
@app.route('/profile')
def profile():
    userid = session['user']
    print('userid is', userid)
    Profile = User.query.filter_by(id=userid).one()
    Sprofile_project = SProfProject.query.filter_by(askedby_id=userid).all()
    Scertificate = SCertify.query.filter_by(askedby_id=userid).all()
    s_resume = Allresume.query.order_by(desc(Allresume.id))
    return render_template('profile.html', i=Profile, Sprofile_project=Sprofile_project, Scertificate=Scertificate, s_resume = s_resume)

# Route to add a new project
@app.route('/SProfileProject', methods=['GET', 'POST'])
def SProfileProject():
    if request.method == 'POST':
        user_id = session['user']
        getTagsArrays=request.form.getlist('tags')
        t=''
        for eachTag in getTagsArrays:
            t += "      "
            t += eachTag
            t += "   |   "
       
        Sprofile_project = SProfProject( project=request.form['project'],
                                shortdescription=request.form['shortdescription'],
                                link=request.form['link'],
                                tags=t, askedby_id=user_id,
                                askedby_name=User.query.get(user_id).username,
                                askedby_img=User.query.get(user_id).image)
        
        db.session.add(Sprofile_project)
        db.session.commit()
        return redirect(url_for('profile'))

    else:
        return render_template('SProfileProject.html')

# Route to add certificates
@app.route('/Scertificates', methods=['GET', 'POST'])
def Scertificates():
    if request.method == 'POST':
        user_id = session['user']
        Scertificate = SCertify( certificate=request.form['certificate'],
                                link=request.form['link'],
                                askedby_id=user_id)
        
        db.session.add(Scertificate)
        db.session.commit()
        return redirect(url_for('profile'))

    else:
        return render_template('Scertificates.html')

# Route to upload resume
@app.route('/Sresume', methods=['GET', 'POST'])
def Sresume():
    if request.method == 'POST':
        user_id = session['user']
        resume = Allresume(link=request.form['link'])       
        db.session.add(resume)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return render_template('Sresume.html')


# Shows the list of tasks assigned to and by a particular user
@app.route('/history')
def history():
    user_id = session['user']
    askedByme = Assigned.query.filter_by(createdbyId=user_id).all()
    toBeDoneByMe = Assigned.query.filter_by(assignedto_ID=user_id).all()
    myQuestion = Question.query.filter_by(askedby_id=user_id).all()
    print(myQuestion)
    return render_template('history.html', askedByme=askedByme, toBeDoneByMe=toBeDoneByMe, myQuestion=myQuestion,
                           user_id=user_id)


# To display all the questions asked by the particular user
'''
@app.route('/myQuestion')
def myQuestion():
    user_id = session['user']
    myQuestion = Question.query.filter_by(askedby_id=user_id).all()
    print(myQuestion)
    return render_template('myQuestion.html', myQuestion=myQuestion, user_id=user_id)
'''


@app.route('/scratchcard')
def scratchcard():
    return render_template('scratchcard.html')


@app.route('/jobs', methods=['POST', 'GET'])
def jobs():
    userid = session['user']
    user = User.query.filter_by(id=userid).one()
    recruiter = Recruiter.query.all()
    print(recruiter)
    if request.method == 'POST':
        

        return redirect(url_for('index'))
    return render_template('jobs.html', user=user, recruiter=recruiter)


@app.route('/submitinterview')
def submitinterview():
    new_item = Interview(user_id=request.args['uid'], username=User.query.get(session['user']).username,
                         recruiter_id=request.args['rid'], recruitername=request.args['recruitername'],
                         userabout=User.query.get(session['user']).about)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))


########################Recruiter ################################

@app.route('/Rindex')
def Rindex():
    rid = session['user']
    username = Recruiter.query.get(session['user']).username
    print('*' * 30)
    print('Recruiter, u ARE LOGGINED IN AS', username)  # All those print statments are for testing purpose. Ignore them
    print('*' * 30)
    flash("welcome {}".format(username))
    today = time.strftime("%m/%d/%Y")
    interview = Interview.query.filter_by(recruiter_id=rid).filter_by(status='Confirmed').order_by(Interview.date).all()

    return render_template('Rindex.html', interview=interview, today=today)


@app.route('/Rnotifications', methods=['POST', 'GET'])
def Rnotifications():
    rid = session['user']
    print(Interview.query.all())
    
    allInterview = Interview.query.filter_by(recruiter_id=rid).filter_by(status='Pending').all()
    print(allInterview)
    if request.method == 'POST':
        id = request.form['id']
        confirm_appointment = Interview.query.filter_by(id=id).one()
        confirm_appointment.status = 'Confirmed'
        confirm_appointment.date = request.form['date']
        confirm_appointment.time = request.form['time']
        db.session.commit()
        return redirect(url_for('Rindex'))
    return render_template('Rnotifications.html', allInterview=allInterview)


@app.route('/CancelInterview')
def CancelInterview():
    id = int(request.args['id'])
    print('to be cancelled ', id)
    CancelAppointment = Interview.query.filter_by(id=id).one()
    print(CancelAppointment)
    CancelAppointment.status = 'Denied'
    db.session.commit()
    return redirect(url_for('Rindex'))


@app.route('/hire')
def hire():
    rid = session['user']
    username = Recruiter.query.get(session['user']).username
    flash("welcome {}".format(username))
    today = time.strftime("%m/%d/%Y")
    mentor_interview = Minterview.query.filter_by(recruiter_id=rid).filter_by(status='Confirmed').order_by(Minterview.date).all()

    return render_template('hire.html', mentor_interview=mentor_interview, today=today)

@app.route('/McancelInterview')
def McancelInterview():
    id = int(request.args['id'])
    
    CancelAppointment = Minterview.query.filter_by(id=id).one()
    CancelAppointment.status = 'Denied'
    db.session.commit()
    return redirect(url_for('Mentors'))
######################################### MENTOR ####################################


@app.route('/Mindex')
def Mindex():
    user_id = session['user']
    username = Mentor.query.get(session['user']).username
    today = time.strftime("%m/%d/%Y")
    showQuestion = Question.query.order_by(desc(Question.id))
    showProject = Project.query.order_by(desc(Project.id))
    rank_user = Mentor.query.order_by(desc(Mentor.score))
    interview = Interview.query.filter_by(user_id=user_id).filter_by(status='Confirmed').order_by(Interview.date).all()
    return render_template('Mindex.html',showQuestion=showQuestion, showProject=showProject, rank_user=rank_user, interview=interview,
                           today=today)

# Route to add a new project
@app.route('/Madd', methods=['GET', 'POST'])
def Madd():
    if request.method == 'POST':
        user_id = session['user']
        getTagsArrays=request.form.getlist('tags')
        t=''
        for eachTag in getTagsArrays:
            t += "      "
            t += eachTag
            t += "   |   "
        print('getTagsArrays',getTagsArrays, 'eachTag',t)
        print(user_id)
        new_project = Project( project=request.form['project'],
                                shortdescription=request.form['shortdescription'],
                                detaileddescription=request.form['detaileddescription'],
                                pay=request.form['pay'], tags=t, askedby_id=user_id,
                                askedby_name=Mentor.query.get(user_id).username,
                                askedby_img=Mentor.query.get(user_id).image)
        flash("New question has been succesfully added")
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('Mindex'))

    else:
        return render_template('AddProject.html')
# In the Mindex.html file, the entire project db will be displayed
# When the mentor clicks on view more btn, they would be redirected to the ParticularProject url
@app.route('/ParticularProject', methods=['GET', 'POST'])
def ParticularProject():
    if request.method == 'POST':
        pid = int(request.args['pid'])
        username = Mentor.query.get(session['user']).username
        image=Mentor.query.get(session['user']).image
        print('question id is', pid)
        new_request = Mresponse(username=username,
                                description=request.form['description'],
                                pay=request.form['pay'], questionID=pid, image=image)
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('Mindex'))
    else:
        args = request.args
        print('args in q url is', args)
        pid = Project.query.get(args['pid'])
        # To check whether the user view the q is same as the user who raised that question. If True, then display assign tag
        isSamePerson = args['user']
        print(isSamePerson)
        user = pid.askedby_id
        img = Mentor.query.get(user).image
        username = Mentor.query.get(user).username
        request = Mresponse.query.filter_by(projectID=pid.id).all()
        print("response is", response)
        return render_template('ParticularProject.html', project=pid, username=username, img=img,
                               request=request,
                               isSamePerson=isSamePerson)


# Shows the list of tasks assigned to and by a particular user
@app.route('/Mhistory')
def Mhistory():
    mentor_id = session['user']
    askedByme = Massigned.query.filter_by(createdbyId=mentor_id).all()
    toBeDoneByMe = Massigned.query.filter_by(assignedto_ID=mentor_id).all()
    myProject = Project.query.filter_by(askedby_id=mentor_id).all()
    print(myProject)
    return render_template('Mhistory.html', askedByme=askedByme, toBeDoneByMe=toBeDoneByMe, myProject=myProject,
                           mentor_id=mentor_id)

@app.route('/Mjobs', methods=['POST', 'GET'])
def Mjobs():
    mentorid = session['user']
    mentor = Mentor.query.filter_by(id=mentorid).one()
    recruiter = Recruiter.query.all()
    print(recruiter)
    student = User.query.all()
    print(student)
    if request.method == 'POST':
        print('post')

        return redirect(url_for('Mindex'))
    return render_template('Mjobs.html', mentor=mentor, recruiter=recruiter, student=student)

@app.route('/Msubmitinterview')
def Msubmitinterview():
    new_interview = Minterview(mentor_id=request.args['uid'], username=Mentor.query.get(session['user']).username,
                         recruiter_id=request.args['rid'], recruitername=request.args['recruitername'],
                         usercompany=Mentor.query.get(session['user']).company)
    db.session.add(new_interview)
    db.session.commit()
    return redirect(url_for('Mindex'))

@app.route('/Mentors', methods=['POST', 'GET'])
def Mentors():
    rid = session['user']
    allMinterview = Minterview.query.filter_by(recruiter_id=rid).filter_by(status='Pending').all()
    if request.method == 'POST':
        id = request.form['id']
        confirm_appointment = Minterview.query.filter_by(id=id).one()
        confirm_appointment.status = 'Confirmed'
        confirm_appointment.date = request.form['date']
        confirm_appointment.time = request.form['time']
        db.session.commit()
        return redirect(url_for('Rindex'))
    return render_template('Mentors.html', allMinterview=allMinterview)

@app.route('/MscoreBoard')
def MscoreBoard():
    rank_mentor = Mentor.query.order_by(desc(Mentor.score))
    return render_template('MscoreBoard.html', rank_mentor=rank_mentor)


# Shows the profile of the mentor who is currently logged in
@app.route('/Mprofile')
def Mprofile():
    mentorid = session['user']
    print('mentorid is', mentorid)
    Mprofile = Mentor.query.filter_by(id=mentorid).one()
    profile_project = ProfProject.query.order_by(desc(ProfProject.id))
    certificate = Certify.query.order_by(desc(Certify.id))
    return render_template('Mprofile.html', i=Mprofile, profile_project=profile_project, certificate=certificate)

# Route to add a new project
@app.route('/ProfileProject', methods=['GET', 'POST'])
def ProfileProject():
    if request.method == 'POST':
        user_id = session['user']
        getTagsArrays=request.form.getlist('tags')
        t=''
        for eachTag in getTagsArrays:
            t += "      "
            t += eachTag
            t += "   |   "
        print('getTagsArrays',getTagsArrays, 'eachTag',t)
        print(user_id)
        profile_project = ProfProject( project=request.form['project'],
                                shortdescription=request.form['shortdescription'],
                                link=request.form['link'],
                                tags=t, askedby_id=user_id,
                                askedby_name=Mentor.query.get(user_id).username,
                                askedby_img=Mentor.query.get(user_id).image)
        flash("New question has been succesfully added")
        db.session.add(profile_project)
        db.session.commit()
        return redirect(url_for('Mprofile'))

    else:
        return render_template('ProfileProject.html')

# Route to add certificates
@app.route('/certificates', methods=['GET', 'POST'])
def certificates():
    if request.method == 'POST':
        user_id = session['user']
        certificate = Certify( certificate=request.form['certificate'],
                                link=request.form['link'],
                                askedby_id=user_id,
                                askedby_name=Mentor.query.get(user_id).username,
                                askedby_img=Mentor.query.get(user_id).image)
        
        db.session.add(certificate)
        db.session.commit()
        return redirect(url_for('Mprofile'))

    else:
        return render_template('certificates.html')


######################################### MAIN ####################################


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



                           
