from flask import Flask, render_template
from flask import Flask, render_template, jsonify
from werkzeug.exceptions import abort
from flaskext.mysql import MySQL
from datetime import date,datetime
import decimal
from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://nizamelahi:1ft1kh2r@localhost/employees',)
Base = declarative_base()
Base.metadata.reflect(engine)


from sqlalchemy.orm import relationship, backref


class employees(Base):
    __table__ = Base.metadata.tables['employees']
class dept_emp(Base):
    __table__ = Base.metadata.tables['dept_emp']
class dept_manager(Base):
    __table__ = Base.metadata.tables['dept_manager']
class salaries(Base):
    __table__ = Base.metadata.tables['salaries']
class departments(Base):
    __table__ = Base.metadata.tables['departments']
class titles(Base):
    __table__ = Base.metadata.tables['titles']


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

load_dotenv()

app = Flask(__name__)


@app.route('/')

def index():
    db_session = scoped_session(sessionmaker(bind=engine))
    items=db_session.query(employees.first_name).limit(10)
    for item in items:
        print(item)
    return("online")

@app.route('/employee_details',methods=['GET'])
def emp_details():
    con=engine.connect()
    data=con.execute('SELECT employees.emp_no, first_name, last_name, dept_emp.dept_no, departments.dept_name, title, salary\
                    FROM employees\
                    INNER JOIN dept_emp\
                    ON employees.emp_no = dept_emp.emp_no\
                    INNER JOIN departments\
                    ON dept_emp.dept_no = departments.dept_no\
                    INNER JOIN titles\
                    ON employees.emp_no = titles.emp_no\
                    INNER JOIN salaries\
                    ON employees.emp_no = salaries.emp_no\
                    ORDER BY first_name LIMIT 100')
    
    return jsonify([dict(r) for r in data])

@app.route('/department_details',methods=['GET'])
def dept_details():
    con=engine.connect()
    data=con.execute('SELECT departments.dept_no, departments.dept_name, employees.emp_no, employees.first_name, employees.last_name, from_date, to_date\
                    FROM departments\
                    INNER JOIN dept_manager\
                    ON departments.dept_no = dept_manager.dept_no\
                    INNER JOIN employees\
                    ON dept_manager.emp_no = employees.emp_no\
                    ORDER BY first_name LIMIT 100')
    
    return jsonify([dict(r) for r in data])

@app.route('/employee/<fname>/<lname>/<bdate>/<gender>/<salary>/<dno>/<title>',methods=['POST'])
def addemp(fname,lname,bdate,gender,salary,dno,title):
    with engine.connect() as cursor:
        data=cursor.execute('select dept_no\
                        from departments\
                        where dept_no like %s',dno)
        if not ([dict(r) for r in data]) :
            return ("invalid dept_no \n")

        else:
            data=cursor.execute('select MAX(emp_no)\
                            from employees ')
            empid=data.fetchone()[0] +1
            empargs=(empid,bdate,fname,lname,gender,date.today())
            cursor.execute('insert into employees (emp_no,birth_date,first_name,last_name,gender,hire_date)\
                values(%s,%s,%s,%s,%s,%s)',empargs)
            # cursor.commit()
            dept_emp_args=(empid,dno,date.today(),"9999-01-01",)
            cursor.execute('insert into dept_emp (emp_no,dept_no,from_date,to_date)\
                values(%s,%s,%s,%s)',dept_emp_args)
            # cursor.commit()
            titles_args=(empid,title,date.today(),"9999-01-01",)
            cursor.execute('insert into titles (emp_no,title,from_date,to_date)\
                values(%s,%s,%s,%s)',titles_args)
            # cursor.commit()
            salaries_args=(empid,salary,date.today(),"9999-01-01",)
            cursor.execute('insert into salaries (emp_no,salary,from_date,to_date)\
                values(%s,%s,%s,%s)',salaries_args)
            # cursor.commit()

            
            
            return ("success\n")
