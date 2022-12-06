from flask import Flask , jsonify,request
from datetime import date
from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker,Session,class_mapper
from sqlalchemy.sql.expression import func
import os
from sqlalchemy import create_engine,insert
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://nizamelahi:1ft1kh2r@localhost/employees',)
Base = declarative_base()
Base.metadata.reflect(engine)


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

    args=request.args
    if args.get('limit'):
            limit=args.get('limit')
    else:
        limit=100
    if args.get('offset'):
            offset=args.get('offset')
    else:
        offset=0

    Session = sessionmaker(bind=engine)
    session = Session()
    data=session.query(
    employees.emp_no,employees.first_name,employees.last_name,dept_emp.dept_no,departments.dept_name,titles.title,salaries.salary
    ).join(
        dept_emp,  employees.emp_no==dept_emp.emp_no
    ).join(
        departments,  dept_emp.dept_no==departments.dept_no
    ).join(
        titles,  titles.emp_no==employees.emp_no
    ).join(
        salaries,  salaries.emp_no==employees.emp_no
    ).order_by(
        employees.emp_no
    ).limit(
        limit
    ).offset(
        offset
    )
    return jsonify([dict(r) for r in data])

@app.route('/department_details',methods=['GET'])
def dept_details():

    args=request.args
    if args.get('limit'):
            limit=args.get('limit')
    else:
        limit=100
    if args.get('offset'):
            offset=args.get('offset')
    else:
        offset=0

    Session = sessionmaker(bind=engine)
    session = Session()
    data=session.query(
    departments.dept_no, departments.dept_name, employees.emp_no, employees.first_name, employees.last_name, dept_manager.from_date, dept_manager.to_date
    ).join(
        dept_manager,  departments.dept_no==dept_manager.dept_no
    ).join(
        employees,  dept_manager.emp_no==employees.emp_no
    ).order_by(
        departments.dept_no
    ).limit(
        limit
    ).offset(
        offset
    )
    return jsonify([dict(r) for r in data])

@app.route('/employee/<fname>/<lname>/<bdate>/<gndr>/<sal>/<dno>/<ttl>',methods=['POST'])
def addemp(fname,lname,bdate,gndr,sal,dno,ttl):
    
    db_session = scoped_session(sessionmaker(bind=engine))
    dept_check=db_session.query(departments).filter(departments.dept_no==dno).first()
    
    if not dept_check  :
        return ("invalid dept_no \n")

    else:
        empid=int(str(db_session.query(func.max(employees.emp_no)).first()[0]))+1

        empargs=(empid,bdate,fname,lname,gndr,date.today())
        stmt= insert(employees).values(empargs)
        db_session.execute(stmt)
        db_session.commit()
        
        dept_emp_args=(empid,dno,date.today(),"9999-01-01",)
        stmt=insert(dept_emp).values(dept_emp_args)
        db_session.execute(stmt)
        db_session.commit()

        titles_args=(empid,ttl,date.today(),"9999-01-01",)
        stmt=insert(titles).values(titles_args)
        db_session.execute(stmt)
        db_session.commit()

        salaries_args=(empid,sal,date.today(),"9999-01-01",)
        stmt=insert(salaries).values(salaries_args)
        db_session.execute(stmt)
        db_session.commit()

        return ("success\n")
