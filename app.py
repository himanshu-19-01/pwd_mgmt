from flask import Flask, render_template,request,redirect,url_for,session
import sqlite3
import smtplib
import random
import threading
import pandas as pd
from gen import random_pass

def connect_db():
    conn = sqlite3.connect('Database.db', check_same_thread=False)
    return conn 

def mail(username,to,otp):
    
    ob=smtplib.SMTP("smtp.gmail.com",587)
    ob.starttls()
    ob.login("your mail id","your password")   # please mention you email and password here
    subject="One Time Password"
    body=f"Dear {username} \n Your one time password for email varification is : {otp} \n\n Don't share this otp to anyone !"
    mes="subject:{}\n\n{}".format(subject,body)
    print(mes)
    listofadd=[to]
    ob.sendmail("himanshumanral2003@gmail.com",listofadd,mes)
    ob.quit()

name=None
password=None
email=None
verify_email=None
portfolio=False
app = Flask(__name__)
app.secret_key = 'my_secret_12key'
@app.route("/")
def home():
    
    return render_template('base.html')
@app.route("/login",methods=['GET','POST'])
def login():
    global name,verify_email 
    if request.method=="POST":
        email=request.form['email']
        passw=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("SELECT username,email FROM login WHERE email=? AND password=?",(email,passw))
        result=cursor.fetchone()
        name=result[0]
        verify_email=result[1]
        print(result)
        if result:
            return render_template("portfolio.html")
        else:
            return render_template("base.html",msg="Invalid Credentials!")
    return render_template("portfolio.html")

@app.route("/newuser", methods=["GET", "POST"])
def new_user():
    global name,password,verify_email
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        passw = request.form['password']
        
        # Generate OTP
        otp = random.randint(1000, 9999)  # Generate a random 4-digit OTP
        thread = threading.Thread(target=mail, args=(username,email,otp))
        name=username
        password=passw
        verify_email=email
        # Send OTP to the user's email (implementation of sending email is not provided here)
        thread.start()
        # Store the generated OTP in session
        session['otp'] = otp
        
        return redirect(url_for('verify_email'))

    return render_template("newuser.html")
@app.route("/verify_email", methods=["GET", "POST"])
def verify_email():
    global name,password,verify_email
    if request.method == "POST":
        entered_otp = request.form['otp']
        stored_otp = session.get('otp')

        if entered_otp == str(stored_otp):
            
            
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO login (username, email, password) VALUES (?, ?, ?)", (name, verify_email,password))
            conn.commit()
            
            return render_template("newuser.html", msg="Account Created Successfully!")
        else:
            # OTP is incorrect, show error message
            return render_template("verify.html", error_msg="Incorrect OTP. Please try again.")
    
    return render_template("verify.html")
@app.route("/Add_new",methods=['GET','POST'])
def Add():
    global name,verify_email
    if request.method=="POST":
        print(name)
        web_name=request.form['web']
        email2=request.form['email']
        passw=request.form['password']
        conn=connect_db()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO passwords (username,email,website_name,email2,password)VALUES(?,?,?,?,?)",(name,verify_email,web_name,email2,passw))
        conn.commit()
        return render_template("add.html",msg="Sucessfully Added to Password Manager !")
    return render_template("add.html")
@app.route("/gen")
def gen():
    passw=random_pass()
    return render_template("add.html",passw=passw)
@app.route("/my_passw")
def myPassw():
    global name,verify_email
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT website_name,email2,password FROM passwords WHERE email=?",(verify_email,))
    results=cursor.fetchall()
    if results:
        df = pd.DataFrame(results, columns=['website_name','email2','password'])
        web=df['website_name'].tolist()
        email=df['email2'].tolist()
        password=df['password'].tolist()
        return render_template("show.html",web=web,email=email,password=password)
    else :
        return render_template("show.html",msg="No Password saveed Yet !")
@app.route("/manage")
def Manage():
    global verify_email
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT website_name,email2,password FROM passwords WHERE email=?",(verify_email,))
    results=cursor.fetchall()
    if results:
        df = pd.DataFrame(results, columns=['website_name','email2','password'])
        web=df['website_name'].tolist()
        email=df['email2'].tolist()
        password=df['password'].tolist()
        return render_template("manage.html",web=web,email=email,password=password)
@app.route("/del/<string:password>")
def delete(password):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE password=?",(password,))  
    conn.commit()
    return redirect(url_for('login'))
@app.route("/portfolio")
def port():
    return render_template("portfolio.html")   
if __name__=='__main__':
    app.run(debug=True)