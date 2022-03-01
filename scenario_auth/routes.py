from flask import Blueprint, session, request, render_template, current_app

from sql_provider import SQLProvider
from database import work_with_db
from access import group_permission_decorator

auth_app = Blueprint('auth', __name__, template_folder='templates')

provider = SQLProvider('scenario_auth/sql')

@auth_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')

        sql = provider.get('auth.sql')

        result = work_with_db(current_app.config['DB_CONFIG'], sql)

        for dictionary in result:
            if login == dictionary['login'] and password == dictionary['password']:
                session['group_name'] = dictionary['group_name']
                return render_template('valid.html')

    return render_template('invalid.html')
