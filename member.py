from flask import Blueprint,render_template,request,redirect,url_for
import pymysql


con = pymysql.connect(host='localhost',port=3306,user='root',password='',db='garudadb',cursorclass=pymysql.cursors.DictCursor)
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
        
        with con:
            cur = con.cursor()
            sql = "UPDATE tb_member SET mem_fname=%s, mem_lname=%s, mem_username=%s, mem_email=%s WHERE mem_id=%s"
            cur.execute(sql,(fname,lname,username,email,id))
            con.commit()
            return redirect(url_for('member.Showdatamember'))
        
        
        