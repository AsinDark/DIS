from flask import Blueprint, render_template, request, current_app, redirect
from datetime import date

from sql_provider import SQLProvider
from database import work_with_db, make_update
from access import group_permission_decorator

edit_app = Blueprint('edit', __name__, template_folder='templates')

provider = SQLProvider('scenario_edit/sql/')

@edit_app.route('/')
@group_permission_decorator
def get_edit_menu():
    return render_template('select_table.html')

@edit_app.route('/worker', methods=['GET', 'POST'])
@group_permission_decorator
def get_table_worker():
    if request.method == 'GET':
        sql = provider.get('worker.sql')
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        heads = ['ФИО сотрудника', 'Номер отдела', 'Дата рождения', 'Адрес', 'Образование', 'Установленный оклад',
                 'Дата приёма на работу', 'Дата увольнения', 'Название позиции штатного расписания']
        return render_template('worker.html', heads=heads, context=result)
    else:
        id_w = request.form.get('id_w_delete')
        if id_w is None:
            id_w = request.form.get('id_w_dismiss')
            dismiss_date = date.today()
            sql = provider.get('update_worker.sql', dismiss_date=dismiss_date, id_w=id_w)
        else:
            sql = provider.get('delete_worker.sql', id_w=id_w)
        make_update(current_app.config['DB_CONFIG'], sql)
        return redirect('/edit/worker')

@edit_app.route('/worker/insert_worker', methods=['GET', 'POST'])
@group_permission_decorator
def add_worker():
    if request.method == 'GET':
        sql = provider.get('position.sql')
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        heads = ['ID позиции', 'Название позиции', 'Минимальный оклад', 'Максимальный оклад']
        return render_template('insert_worker.html', heads=heads, context=result)
    else:
        name = request.form.get('name')
        departament_number = request.form.get('departament_number')
        birthday = request.form.get('birthday')
        adress = request.form.get('adress')
        education = request.form.get('education')
        Salary = request.form.get('Salary')
        recruit_date = request.form.get('recruit_date')
        w_id_p = request.form.get('w_id_p')
        sql = provider.get('insert_worker.sql', name=name, departament_number=departament_number, birthday=birthday,
                           adress=adress, education=education, Salary=Salary, recruit_date=recruit_date, w_id_p=w_id_p)
        make_update(current_app.config['DB_CONFIG'], sql)
        return redirect('/edit/worker')

@edit_app.route('/position', methods=['GET', 'POST'])
@group_permission_decorator
def get_table_position():
    if request.method == 'GET':
        sql = provider.get('position.sql')
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        heads = ['Название позиции', 'Минимальный оклад', 'Максимальный оклад']
        return render_template('position.html', heads=heads, context=result)
    else:
        id_p = request.form.get('id_p')
        sql = provider.get('delete_position.sql', id_p=id_p)
        make_update(current_app.config['DB_CONFIG'], sql)
        return redirect('/edit/position')

@edit_app.route('/position/insert_position', methods=['GET', 'POST'])
@group_permission_decorator
def add_position():
    if request.method == 'GET':
        return render_template('insert_position.html')
    else:
        title = request.form.get('title')
        min_salary = request.form.get('min_salary')
        max_salary = request.form.get('max_salary')
        sql = provider.get('insert_position.sql', title=title, min_salary=min_salary, max_salary=max_salary)
        make_update(current_app.config['DB_CONFIG'], sql)
        return redirect('/edit/position')

@edit_app.route('/vacancy', methods=['GET', 'POST'])
@group_permission_decorator
def get_table_vacancy():
    if request.method == 'GET':
        sql = provider.get('vacancy.sql')
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        heads = ['Дата открытия', 'Дата закрытия', 'Название позиции штатного расписания']
        return render_template('vacancy.html', heads=heads, context=result)
    else:
        id_v = request.form.get('id_v')
        sql = provider.get('delete_vacancy.sql', id_v=id_v)
        make_update(current_app.config['DB_CONFIG'], sql)
        return redirect('/edit/vacancy')

@edit_app.route('/vacancy/insert_vacancy', methods=['GET', 'POST'])
@group_permission_decorator
def add_vacancy():
    if request.method == 'GET':
        sql = provider.get('position.sql')
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        heads = ['ID позиции', 'Название позиции', 'Минимальный оклад', 'Максимальный оклад']
        return render_template('insert_vacancy.html', heads=heads, context=result)
    else:
        open_date = date.today()
        v_id_p = request.form.get('v_id_p')
        sql = provider.get('insert_vacancy.sql', open_date=open_date, v_id_p=v_id_p)
        make_update(current_app.config['DB_CONFIG'], sql)
        return redirect('/edit/vacancy')
