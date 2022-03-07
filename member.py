from flask import Blueprint,render_template,request,redirect,url_for
import pymysql


con = pymysql.connect("127.0.0.1","root","","garudadb")
member = Blueprint('member', __name__)



@member.route('/showmember')
def Showdatamember():
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


    