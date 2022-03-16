from flask import Flask, render_template
from member import *
from survey import *
from datetime import timedelta



app = Flask(__name__)
app.register_blueprint(member)
app.register_blueprint(survey)
app.secret_key = "jor2818"
app.permanent_session_lifetime = timedelta(minutes=30)



@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)