from flask import Blueprint, render_template, request, current_app

from sql_provider import SQLProvider
from database import work_with_db
from access import group_permission_decorator

query_app = Blueprint('queries', __name__, template_folder='templates')

provider = SQLProvider('scenario_query/sql/')

@query_app.route('/')
@group_permission_decorator
def get_queries():
    return render_template('queries.html')

@query_app.route('/query1')
@group_permission_decorator
def get_query1():
    return render_template('query1.html')

@query_app.route('/query2')
@group_permission_decorator
def get_query2():
    return render_template('query2.html')

@query_app.route('/query3')
@group_permission_decorator
def get_query3():
    return render_template('query3.html')

@query_app.route('/query4')
@group_permission_decorator
def get_query4():
    return render_template('query4.html')

@query_app.route('/result1')
@group_permission_decorator
def get_report_by_title():
    title = request.args.get('title')
    sql = provider.get('query1.sql', title=title)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)
    return render_template('result1.html', context=result)

@query_app.route('/result2')
@group_permission_decorator
def get_report_by_year():
    year = request.args.get('year')
    sql = provider.get('query2.sql', year=year)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)
    return render_template('result2.html', context=result)

@query_app.route('/result3')
@group_permission_decorator
def get_info_by_number():
    number = request.args.get('number')
    sql = provider.get('query3.sql', number=number)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)
    return render_template('result3.html', context=result)

@query_app.route('/result4')
@group_permission_decorator
def get_positions_by_year():
    year = request.args.get('year')
    sql = provider.get('query4.sql', year=year)
    db_config = current_app.config['DB_CONFIG']
    result = work_with_db(db_config, sql)
    return render_template('result4.html', context=result)