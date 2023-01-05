from flask import *
from database import *

public=Blueprint('public',__name__)

@public.route('/')
def home():

    return render_template("index.html")

@public.route('/login',methods=['get','post'])
def login():
    data={}
    if 'login' in request.form:
        uname=request.form['uname']
        passw=request.form['passw']
        q="select * from login where username='%s' and password='%s' and login_status='active'"%(uname,passw)
        res=select(q)
        if res:
            session['logid']=res[0]['username']
            utype=res[0]['user_type']
            if utype=='admin':
                flash("welcome Admin")
                return redirect(url_for('admin.adhome'))
            elif utype=='user':
                flash("welcome User")
                q="select * from user where username='%s'"%(session['logid'])
                res=select(q)
                session['uid']=res[0]['user_id']
                return redirect(url_for('user.uhome'))
            elif utype=='courier':
                flash("welcome courier")
                q="select * from courier where username='%s'"%(session['logid'])
                res=select(q)
                session['cid']=res[0]['courier_id']
                return redirect(url_for('courier.chome'))
            else:
                flash("please enter a valid username or password")
                return redirect(url_for('public.login'))
        else:
            flash("The entered Username or password is incorrect please check and try again")
            return redirect(url_for('public.login'))
    return render_template('login.html')

@public.route("/reg",methods=['get','post'])
def reg():
    data={}
    if 'reg' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        gen=request.form['gen']
        dob=request.form['dob']
        phone=request.form['phone']
        hno=request.form['hno']
        street=request.form['street']
        dist=request.form['dist']
        state=request.form['state']
        pin=request.form['pin']
        uname=request.form['uname']
        passw=request.form['passw']
        q="select * from login where username='%s'"%(uname)
        res=select(q)
        if res:
           data['warning']="Username Already Exist"
        else:

            q="insert into login values('%s','%s','user','active')"%(uname,passw)
            id=insert(q)
            q="insert into user values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',curdate(),'active')"%(uname,fname,lname,gen,dob,phone,hno,street,dist,state,pin)
            insert(q)
            flash("Registration Successfull")
            return redirect(url_for('public.login'))
    return render_template('user_reg.html')