from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import pymysql


con = pymysql.connect("127.0.0.1","root","","garudadb")
member = Blueprint('member', __name__)

bcrypt = Bcrypt()


@member.route('/showmember')
def Showdatamember():
    if "username" not in session:
        return redirect(url_for('member.Signin'))

    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_member"
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)
        return render_template('tables-member.html', rows=rows)

@member.route('/editmember', methods=['GET','POST'])
def Editmember():
    if request.method == 'POST':
        
        id = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        status = request.form['status']
        print(status)
        
        with con:
            cur = con.cursor()
            sql = "UPDATE tb_member SET mem_fname=%s, mem_lname=%s, mem_username=%s, mem_email=%s, mem_status=%s WHERE mem_id=%s"
            cur.execute(sql,(fname,lname,username,email,status,id))
            con.commit()
            return redirect(url_for('member.Showdatamember'))
        

@member.route('/delmember', methods=['GET','POST'])   
def Delmember():
    if request.method == 'POST':
        
        id = request.form['id']

        with con:
            cur = con.cursor()
            sql = "DELETE FROM tb_member WHERE mem_id=%s"
            cur.execute(sql, id)
            con.commit()
            return redirect(url_for('member.Showdatamember'))


@member.route('/signup')
def Signup():
    return render_template('pages-sign-up.html')

@member.route('/addmember', methods=['GET','POST'])
def Addmember():
    
    if request.method == 'POST':
        
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password_1']
        con_password = request.form['password_2']
        
        if len(fname)<2:
            flash("Firstname should be greater than 2 characters.Try again!!!")
            
        elif len(lname)<2:
            flash("Lastname should be greater than 2 characters.Try again!!!")

        elif len(username)<2:
            flash("Username should be greater than 2 characters.Try again!!!")

        elif len(email)<7:
            flash("Email should be at least 7 characters.Try again!!!")
        
        elif password != con_password:
            flash("Password are not matched.Try again!!!")
            
        else:
            # generate hash password
            password = bcrypt.generate_password_hash(password)
            with con:
                cur = con.cursor()
                sql = "INSERT INTO tb_member (mem_fname, mem_lname, mem_username, mem_email, mem_password) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(sql,(fname,lname,username,email,password))
                con.commit()
                return redirect(url_for('member.Signin'))

    return redirect(url_for('member.Signup'))

@member.route('/signin')
def Signin():
    return render_template('pages-sign-in.html')

@member.route('/surveyform')
def Surveyform():
    return render_template('forms-roadside.html')

@member.route('/checklogin', methods=['POST','GET'])
def Checklogin():
    
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']
        
        with con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_member WHERE mem_username=%s"
            cur.execute(sql,username)
            rows = cur.fetchall()
            #print(rows[0][5])
            #print(password1)
            # Check status Admin or user
            if len(rows)>0:
                if bcrypt.check_password_hash(rows[0][5], password1):# Why False!
                    if rows[0][6] == 0:
                        session['username'] = username
                        session['fname'] = rows[0][1]
                        session['status'] = rows[0][6]
                        session.permanent = True
                        return redirect(url_for('member.Surveyform'))
                    else:
                        session['username'] = username
                        session['fname'] = rows[0][1]
                        session['status'] = rows[0][6]
                        session.permanent = True
                        return redirect(url_for('member.Showdatamember'))
                else:
                    flash("Incorrect Password! Please Check your password again.")

            else:
                flash("You are not logged in. Please Check your username and password.")
            return render_template('pages-sign-in.html')
            
@member.route('/signoff')
def Signoff():
    session.clear()
    return redirect(url_for('member.Signin'))