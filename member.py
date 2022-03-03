from flask import Blueprint,render_template
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