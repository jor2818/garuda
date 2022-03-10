from flask import Blueprint, render_template, request, redirect, url_for, session
import pymysql


con = pymysql.connect("127.0.0.1","root","","garudadb")
member = Blueprint('member', __name__)



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
        return render_template('showdatamember.html', headername='ข้อมูลสมาชิก',rows=rows)

@member.route('/editmember', methods=['POST'])
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
        

@member.route('/delmember', methods=['POST'])   
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
    return render_template('signup.html')

@member.route('/addmember', methods=['POST'])
def Addmember():
    
    if request.method == 'POST':
        
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password_1']
        con_password = request.form['password_2']
        
        if password == con_password:
            with con:
                cur = con.cursor()
                sql = "INSERT INTO tb_member (mem_fname, mem_lname, mem_username, mem_email, mem_password) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(sql,(fname,lname,username,email,password))
                con.commit()
                return redirect(url_for('member.Signin'))
        else:
            return redirect(url_for('member.Signup'))

@member.route('/signin')
def Signin():
    return render_template('signin.html')

@member.route('/surveyform')
def Surveyform():
    return render_template('surveyform.html')

@member.route('/checklogin', methods=['POST'])
def Checklogin():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_member WHERE mem_username=%s AND mem_password=%s"
            cur.execute(sql,(username,password))
            rows = cur.fetchall()
            print(rows)
            
            if len(rows)>0:
                if rows[0][6] == 0:
                    session['username'] = username
                    session['fname'] = rows[0][1]
                    session.permanent = True
                    return redirect(url_for('member.Surveyform'))
                else:
                    session['username'] = username
                    session['fname'] = rows[0][1]
                    session.permanent = True
                    return redirect(url_for('member.Showdatamember'))
            else:
                return redirect(url_for('member.login'))