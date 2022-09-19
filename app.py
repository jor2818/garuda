from flask import Flask, render_template
from member import *
from survey import *
from datetime import timedelta
from flask_bcrypt import Bcrypt
import secrets




app = Flask(__name__)
# create the secret_key_hash
secret_key = secrets.token_hex(16)
bcrypt = Bcrypt(app)
secret_key_hash = bcrypt.generate_password_hash(secret_key)
app.config['SECRET_KEY'] = secret_key_hash
app.permanent_session_lifetime = timedelta(minutes=30)

app.register_blueprint(member)
app.register_blueprint(survey)



@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)