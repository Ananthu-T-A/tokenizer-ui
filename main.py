from flask import *
from database import *
from public import public
from admin import admin
from user import user
from courier import courier

app=Flask(__name__)
app.secret_key="hai"
app.register_blueprint(public)
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(courier,url_prefix='/courier')


app.run(debug=True,port=5745)
