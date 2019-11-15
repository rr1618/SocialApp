from flask import Flask, render_template,request,session,flash,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
import math
import json
from time import time,ctime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,login_required,logout_user,current_user,LoginManager
from sqlalchemy.sql.functions import session_user
# Open json file
with open("config.json" , "r") as c:
    home = json.load(c)["home"]
app = Flask(__name__)
app.secret_key = 'the random string'
local_server=1
t=time()
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = home["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = home["prod_uri"]
# Create DataBase object
db=SQLAlchemy(app)
# LoginManager Object
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message="Login first"
# Post Table
class posters(db.Model):
    __tablename__ = "post"
    sno = db.Column(db.Integer, primary_key=True)
    post_title=db.Column(db.String(50), nullable=False)
    post = db.Column(db.String(200), nullable=False)
    username= db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(40), nullable=True)
# Contactus table
class contactus(db.Model):
    __tablename__="contactus"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message=db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(40), nullable=True)
# Registration table
class registration(UserMixin,db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(15),nullable=False)
    lname = db.Column(db.String(15), nullable=False)
    password= db.Column(db.String(20), nullable=False)
    username= db.Column(db.String(20), nullable=False)
    email= db.Column(db.String(30), nullable=False)
    contact = db.Column(db.String(12), nullable=False)
    date=db.Column(db.String(40),nullable=True)
# decorator to load user
@login_manager.user_loader
def load_user(user_id):
    return registration.query.get(int(user_id))
@app.route('/register',methods=['POST'])
# username availaibility check
def username():
    uname=request.form['username']
    check_username=registration.query.filter_by(username=uname).first()
    if check_username:
        return jsonify({'error':'username not available'})
    return jsonify({"success":"available"})
@app.route('/<int:page_num>')
# home page
def index(page_num):
    home["caption1"]
    posts  =posters.query.order_by(posters.date.desc()).paginate(per_page=5,page=page_num,error_out=True)
    return render_template("home.html",posts=posts,home=home,session=session)
# edit post
@app.route('/dashboard/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if (request.method == 'POST'):
        sno = request.form['input3']
        chck=request.form['input4']
        print (sno,chck)
        obj = posters.query.filter_by(sno=sno).first()
        if(chck=='true'):
            print("yes")
            obj.post_title=request.form['post_title']
            obj.post=request.form['post']
            print (obj.post_title,obj.post)
            obj.date=ctime(t)
            db.session.commit()
            return jsonify({"msg":"success"})
        return jsonify({"post_title":obj.post_title,"post":obj.post})
    return "There was some error"
# delete post
@app.route('/dashboard/delete',methods=['GET','POST'])
@login_required
def delete():
    if(request.method=='POST'):
        sno=request.form['input2']
        obj=posters.query.filter_by(sno=sno).first()
        db.session.delete(obj)
        db.session.commit()
        return jsonify({"msg":"post deleted"})
    return jsonify({"msg":"post deleted"})
@app.route('/contact',methods=['GET','POST'])
# submit contact us details
def contact():
    if(request.method=="POST"):
        fname = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message=request.form.get('message')
        entry=contactus(fname=fname,email=email,phone=phone,message=message,date=ctime(t))
        db.session.add(entry)
        db.session.commit()
        return redirect('/1')
    return render_template("contact.html",session=session)
@app.route('/registration',methods=['GET','POST'])
def reg():
    if (request.method == "POST"):
        fname = request.form.get('f_name')
        lname = request.form.get('l_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        username = request.form.get('u_name')
        password = request.form.get("npass")
        # print(fname,lname,email)
        entry = registration(fname=fname,date=ctime(t), lname=lname, email=email, password=password, username=username,contact=phone)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    return render_template("registration.html")
@app.route('/dashboard/<int:page_num>')
@login_required
def dashboard(page_num):
    posts = posters.query.filter_by(username=current_user.username).order_by(posters.date.desc())
    thread=posts.paginate(per_page=5,page=page_num,error_out=True)
    return render_template('dashboard.html',cur_usr=current_user.username,posts=thread,session=session)
# Check login creditnials
@app.route('/dashboard/submit',methods=['GET','POST'])
@login_required
def submitPost():
    if (request.method == "POST"):
        post_title = request.form.get('post_title')
        post = request.form.get('post')
        post_image =request.form.get('image')
        print (ctime())
        entry = posters(username=current_user.username, post=post, post_title=post_title, date=ctime(t))
        db.session.add(entry)
        db.session.commit()
        return redirect('/dashboard/1')
    return "something went wrong"
@app.route('/login', methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        username=request.form.get('username')
        password=request.form.get('password')
        # print(username,password)
        uname=registration.query.filter_by(username=username).first()
        if(uname.password==password):
            # print("logged")
            session['user']=username
            # print (session,session['user'])
            login_user(uname)
            return jsonify({"success":"logged"})
        return jsonify({"error":"wrong pass"})
    return redirect('/')
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    session['user']=""
    logout_user()
    return redirect('/1')
if __name__ == '__main__':
	app.run(debug=True)