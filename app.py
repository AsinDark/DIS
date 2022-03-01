import json

from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

from scenario_query.routes import query_app
from scenario_auth.routes import auth_app
from scenario_edit.routes import edit_app

app.register_blueprint(query_app, url_prefix='/queries')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(edit_app, url_prefix='/edit')

app.config['DB_CONFIG'] = json.load(open('configs/dbconfig.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['SECRET_KEY'] = 'my secret key'

@app.route('/')
def index():
    return render_template('mainMenu.html')

@app.route('/exit')
def index_exit():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
