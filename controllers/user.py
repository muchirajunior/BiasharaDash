import random
from flask import Blueprint, render_template,request,redirect,flash
from flask_login import login_user, logout_user
from flask_mail import Message
from models.business import Business
from models.cartegory import Cartegory
from models.user import User,db
from main import bcrypt,mail

users=Blueprint("users",__name__,url_prefix="/user",template_folder="../templates/user")

@users.route("/login",methods=['POST','GET'])
def login():
    try:
        if request.method=="POST":
            username=request.form["email"]
            password=request.form["password"]
            next_page = request.args.get("next")
            user:User= User.query.filter_by(email=username).first()
            if user == None:
                flash("user does not exist")
                return render_template("login.html")
           
            if bcrypt.check_password_hash(user.password, password) :
                login_user(user)
                if(user.otp != None):
                    user.otp=None
                    db.session.commit()
                if(next_page != None): #check for next page the user wanted to access and redirect if any
                    return redirect(next_page)
                return redirect ("/")
            elif user.otp != None and str(user.otp) == password:
                user.otp=None
                db.session.commit()
                login_user(user)
                return redirect('/')
            elif user.otp != None and str(user.otp) != password:
                flash("wrong otp !!")
                return render_template("login.html")
            else:
                flash("wrong user password")
                return render_template("login.html")
    except:
        flash("login error !!")
        return render_template("login.html")

    return render_template("login.html")

@users.route('/register',methods=['POST','GET'])
def register():
    cartegories=Cartegory.query.all()
    try:
        if request.method=="POST":
            print("register user")
            #user
            name=request.form["name"]
            email=request.form["email"]
            password=request.form["password"]
            repeat_password=request.form["repeat_password"]

            if(password!=repeat_password):
                flash("password missmatch")
                return render_template('register.html',cartegories=cartegories)
            
            password=bcrypt.generate_password_hash(password,10).decode('utf-8')

            user=User(name,email,password)
            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect("/")
    except Exception as error:
        print(error)
        flash(str(error.args))
        return render_template('register.html',cartegories=cartegories)

    return render_template('register.html',cartegories=cartegories)

@users.route('/forgot-password',methods=['POST','GET'])
def forgot_password():
    try:
        if request.method=='POST':
            email = request.form.get('email')
            user:User = User.query.filter_by(email=email).first()
            if user == None:
                flash('user with such email does not exist. please check you email and try again !')
                return render_template('forgot_password.html')
            otp=random.randint(100000,999999)
            message= Message(
                    body=f"Hello {user.name}  \n\n your otp is {otp} use it to login and reset your password  \n \n Thank You",
                    subject="forgot password otp",
                    sender="non-reply@biashara.buzz",
                    recipients=[email]
                    )
            mail.send(message)
            user.otp=otp
            db.session.commit()
        
            return redirect('/user/login')
    except Exception as error:
        flash(error.args)
    return render_template('forgot_password.html')

@users.route("/restricted")
def restricted():
    return render_template("restricted.html")

@users.route('/logout')
def logout():
    logout_user()
    return redirect("/")