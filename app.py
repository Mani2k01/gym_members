from flask import Flask,render_template,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
import os


app=Flask(__name__)
app.config['SECRET_KEY']=os.environ.get("SECRET_KEY")

account_sid =os.environ.get('ACCOUNT_SID')
auth_token=os.environ.get('AUTH_TOKEN')
client = Client(account_sid, auth_token)
sender_id='Bullet Gym'

### for database ###
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    number=db.Column(db.Integer,nullable=False)

with app.app_context():
    db.create_all()


@app.route('/',methods=["GET","POST"])
def home():
    if request.method == "POST":
        name=request.form['name']
        age=request.form['age']
        number=request.form['number']
        with app.app_context():
            if User.query.filter_by(name=name).first() and User.query.filter_by(number=number).first():
                flash("User already Registered ", "danger")
                return redirect(url_for('home'))

            with app.app_context():
                new_user=User(name=name,age=age,number=number)
                db.session.add(new_user)
                db.session.commit()
                flash("User Registered Successfully","success")
                send_message()
                return redirect(url_for('home'))

    return render_template("index.html")


@app.route('/users')
def users():
    with app.app_context():
        users=User.query.all()

    return render_template("users.html",users=users)
def send_message():
    number = '+91' + request.form['number']
    message = client.messages.create(
        body="You are successfully registered to Bullet Gym Membership ",
        messaging_service_sid=os.environ.get('SERVICE_SID'),
        to=number,
    )
    print(message.status)

if __name__ == "__main__":
    app.run(debug=True)
