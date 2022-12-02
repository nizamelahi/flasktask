import sqlite3
from flask import Flask, render_template
from flask import Flask, render_template, jsonify
from werkzeug.exceptions import abort
from flaskext.mysql import MySQL
from datetime import date

app = Flask(__name__)


app.config['MYSQL_DATABASE_USER'] = 'nizamelahi'
app.config['MYSQL_DATABASE_PASSWORD'] = '1ft1kh2r'
app.config['MYSQL_DATABASE_DB'] = 'employees'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

def get_db_connection():
    conn = mysql.connect()
    cursor =conn.cursor()
    return cursor

@app.route('/')

def index():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('SELECT * FROM employees ORDER BY first_name LIMIT 100')
    employees=cursor.fetchall()
    for employee in employees:
        print(employee)
    return render_template('index.html',employees=employees)

@app.route('/employee_details',methods=['GET'])
def emp_details():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('SELECT employees.emp_no, first_name, last_name, dept_emp.dept_no, departments.dept_name, title, salary\
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
    employees=cursor.fetchall()
    return jsonify(employees)

@app.route('/department_details',methods=['GET'])
def dept_details():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('SELECT departments.dept_no, departments.dept_name, employees.emp_no, employees.first_name, employees.last_name, from_date, to_date\
                    FROM departments\
                    INNER JOIN dept_manager\
                    ON departments.dept_no = dept_manager.dept_no\
                    INNER JOIN employees\
                    ON dept_manager.emp_no = employees.emp_no\
                    ORDER BY first_name LIMIT 100')
    employees=cursor.fetchall()
    return jsonify(employees)

@app.route('/employee/<fname>/<lname>/<bdate>/<gender>/<salary>/<dno>/<title>',methods=['POST'])
def addemp(fname,lname,bdate,gender,salary,dno,title):
    conn = mysql.connect()
    cursor =conn.cursor()
    
    cursor.execute('select dept_no\
                    from departments\
                    where dept_no like %s',dno)
    if not cursor.fetchall() :
        return ("invalid dept_no \n")
    else:
        cursor.execute('select MAX(emp_no)\
                        from employees ')
        empid=cursor.fetchone()[0] +1
        empargs=(empid,bdate,fname,lname,gender,date.today())
        cursor.execute('insert into employees (emp_no,birth_date,first_name,last_name,gender,hire_date)\
            values(%s,%s,%s,%s,%s,%s)',empargs)
        conn.commit()
        dept_emp_args=(empid,dno,date.today(),"9999-01-01",)
        cursor.execute('insert into dept_emp (emp_no,dept_no,from_date,to_date)\
            values(%s,%s,%s,%s)',dept_emp_args)
        conn.commit()
        titles_args=(empid,title,date.today(),"9999-01-01",)
        cursor.execute('insert into titles (emp_no,title,from_date,to_date)\
            values(%s,%s,%s,%s)',titles_args)
        conn.commit()
        salaries_args=(empid,salary,date.today(),"9999-01-01",)
        cursor.execute('insert into salaries (emp_no,salary,from_date,to_date)\
            values(%s,%s,%s,%s)',salaries_args)
        conn.commit()

        
        
        return ("success\n")
