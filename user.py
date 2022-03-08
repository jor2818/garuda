from flask import Blueprint,render_template,request,redirect,url_for
import pymysql


con = pymysql.connect("127.0.0.1","root","","garudadb")
user = Blueprint('user', __name__)

@user.route('/signin')
def Signin():
    return render_template('signin.html')