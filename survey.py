from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import pymysql


con = pymysql.connect("127.0.0.1","root","","garudadb")
survey = Blueprint('survey', __name__)



@survey.route('/showsurvey')
def Showdatasurvey():
    if "username" not in session:
        return redirect(url_for('member.Signin'))

    with con:
        cur = con.cursor()
        
        if session["status"] == 0:
            sql = "SELECT * FROM tb_survey WHERE srv_usrname=%s"
            cur.execute(sql, session['username'])
        else:
            sql = "SELECT * FROM tb_survey"
            cur.execute(sql)
        
        rows = cur.fetchall()
        print(rows)
        return render_template('showdatasurvey.html', headername='ข้อมูลการสำรวจ',rows=rows)

@survey.route('/editsurvey', methods=['POST'])
def Editsurvey():
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
            return redirect(url_for('member.Showdatasurvey'))
        

@survey.route('/delsurvey', methods=['POST'])   
def Delsurvey():
    if request.method == 'POST':
        
        id = request.form['id']

        with con:
            cur = con.cursor()
            sql = "DELETE FROM tb_survey WHERE srv_id=%s"
            cur.execute(sql, id)
            con.commit()
            return redirect(url_for('survey.Showdatasurvey'))


@survey.route('/addsurvey', methods=['POST'])
def Addsurvey():
    
    if request.method == 'POST':
        
        projname = request.form['projname']
        rname = request.form['rname']
        stname = request.form['stname']
        date = request.form['date']
        username = session['username']
        weather = request.form['weather']
        trippurpose = request.form['trippurpose']
        orgplc = request.form['orgplc']
        orgplcname = request.form['orgplcname']
        orgzone = request.form['orgzone']
        destplc = request.form['destplc']
        destplcname = request.form['destplcname']
        destzone = request.form['destzone']
        vehtype = request.form['vehtype']
        nbpass = request.form['nbpass']
        
        with con:
            cur = con.cursor()
            sql = "INSERT INTO tb_survey (srv_projname, srv_rname, srv_stname, srv_date, srv_usrname, srv_weather, srv_trippurpose, srv_orgplc, srv_orgplcname, srv_orgzone, srv_destplc, srv_destplcname, srv_destzone, srv_vehtype, srv_nbpass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql,(projname,rname,stname,date,username,weather,trippurpose,orgplc,orgplcname,orgzone,destplc,destplcname,destzone,vehtype,nbpass))
            con.commit()
            flash("This data has been stored already.")
            return redirect(url_for('member.Surveyform'))

        


