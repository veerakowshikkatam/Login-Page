from flask import Flask, render_template, redirect, request, url_for
from database import session, engine, Person, Base
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form["password"]

        existing_user = session.query(Person).filter_by(username = username).first()
        if existing_user:
            return "username already exist"
        new_user = Person(username = username, password = password)

        try:
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            return f'Something went wrong while registering user: {str(e)}'

    return render_template("register.html")


@app.route("/grade")
def grade():
    return render_template("marks.html")


#@app.route('/submit',methods=['POST','GET'])
#def submit():
#   total_score=0
 #   if request.method=='POST':
  #      am1100 =float(request.form['am1100'])
   #     am1100cred = float(request.form['am1100cred'])
    #    ch1020=float(request.form['ch1020'])
    #    ch1020cred=float(request.form['ch1020cred'])
     #   cs1100=float(request.form['cs1100'])
     #   cs1100cred=float(request.form['cs1100cred'])
      #  cy1001=float(request.form['cy1001'])
       # cy1001cred=float(request.form['cy1001cred'])
        #total_score=(am1100*am1100cred+ch1020*ch1020cred+cs1100*cs1100cred+cy1001*cy1001cred)/(am1100cred + ch1020cred + cs1100cred + cy1001cred)
   # return "Your Final Grade is " + " "  + str(total_score) + " which will show in your grade card as " + str(round(total_score, 2))


app.run(debug = True)




