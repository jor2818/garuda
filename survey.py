from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import pymysql
import sqlalchemy as db
import pandas as pd

#pymysql connection setting
con = pymysql.connect("127.0.0.1","root","","garudadb")
#sqlalchemy connection setting
engine = db.create_engine('mysql+pymysql://root:@127.0.0.1/garudadb')
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
            # SQL Database to DataFrame
            df = pd.read_sql(sql,engine,params=[session['username']])

        else:
            sql = "SELECT * FROM tb_survey"
            cur.execute(sql)
            # SQL Database to DataFrame
            df = pd.read_sql(sql,engine)


        
        rows = cur.fetchall()
        #print(rows)
        print(df)
        return render_template('tables-roadside.html',rows=rows,df=df)

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
        direction = request.form['direction']
        username = session['username']
        weather = request.form['weather']
        trippurpose = request.form['trippurpose']
        orgprovince = request.form['orgprovince']
        orgamphoe = request.form['orgamphoe']
        orgtambon = request.form['orgtambon']
        orgplcname = request.form['orgplcname']
        orgzone = request.form['orgzone']
        destprovince = request.form['destprovince']
        destamphoe = request.form['destamphoe']
        desttambon = request.form['desttambon']
        destplcname = request.form['destplcname']
        destzone = request.form['destzone']
        license = request.form['license']
        vehtype = request.form['vehtype']
        nbpass = request.form['nbpass']
        nbpassbus = request.form['nbpassbus']
        goodstype = request.form['goodstype']
        goodsweight = request.form['goodsweight']
        income = request.form['income']
        
        
        
        with con:
            cur = con.cursor()
            sql = "INSERT INTO tb_survey (srv_projname, srv_rname, srv_stname, srv_date, srv_direct, srv_usrname, srv_weather, srv_trippurpose, srv_orgprovince, srv_orgamphoe, srv_orgtambon,  srv_orgplcname, srv_orgzone, srv_destprovince, srv_destamphoe, srv_desttambon, srv_destplcname, srv_destzone, srv_license, srv_vehtype, srv_nbpass, srv_nbpass_bus, srv_goodstype, srv_goodsweight, srv_income) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql,(projname,rname,stname,date,direction,username,weather,trippurpose,orgprovince,orgamphoe,orgtambon,orgplcname,orgzone,destprovince,destamphoe,desttambon,destplcname,destzone,license,vehtype,nbpass,nbpassbus,goodstype,goodsweight,income))
            con.commit()
            flash("This data has been stored already.")
            return redirect(url_for('member.Surveyform'))

        
@survey.route('/rsanalysis')
def Rsanalysis():
    
    if "username" not in session:
        return redirect(url_for('member.Signin'))

    with con:
        cur = con.cursor()
        
        if session["status"] == 0:
            sql = "SELECT * FROM tb_survey WHERE srv_usrname=%s"
            cur.execute(sql, session['username'])
            # SQL Database to DataFrame
            df = pd.read_sql(sql,engine,params=[session['username']])

        else:
            sql = "SELECT * FROM tb_survey"
            cur.execute(sql)
            # SQL Database to DataFrame
            df = pd.read_sql(sql,engine)


        
        rows = cur.fetchall()
        #print(rows)
        #print(df)
        triptype = df.groupby('srv_trippurpose')['srv_trippurpose'].count()
        vehicletype = df.groupby('srv_vehtype')['srv_vehtype'].count()
        income = df.groupby('srv_income')['srv_income'].count()
        buspassenger = df.groupby('srv_nbpass_bus')['srv_nbpass_bus'].count()
        goodstype = df.groupby('srv_goodstype')['srv_goodstype'].count()
        
        return render_template('dashboard-rs.html', df=df, triptype=triptype, vehicletype=vehicletype, income=income, buspassenger=buspassenger, goodstype=goodstype)


    