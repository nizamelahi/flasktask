from flask import Flask , jsonify,request
from datetime import date,datetime
from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker,Session,class_mapper
from sqlalchemy.sql.expression import func
from sqlalchemy import create_engine,insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Date,Enum,CHAR,ForeignKey,PrimaryKeyConstraint
import os
load_dotenv()

engine = create_engine('mysql+pymysql://'+os.getenv('username')+':'+os.getenv('pw')+'@'+os.getenv('dbhost')+'/'+os.getenv('dbname'))

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



class employees(Base):
    __tablename__ = 'employees'
    emp_no =Column(Integer, primary_key=True,nullable=False)
    birth_date=Column(Date,nullable=False)
    first_name=Column(String(14),nullable=False)
    last_name=Column(String(16),nullable=False)
    gender=Column(Enum('M','F'),nullable=False)
    hire_date=Column(Date,nullable=False)
    # chkfield=Column(String,nullable=False)

    def __repr__(self):
        return f'employee {self.first_name}'

class departments(Base):
    __tablename__ = 'departments'
    dept_no=Column(CHAR(4),primary_key=True,nullable=False)
    dept_name=Column(String(40),unique=True,nullable=False)

    def __repr__(self):
        return f'department {self.dept_name}'

class dept_manager(Base):
    __tablename__ = 'dept_manager'
    emp_no=Column(Integer,ForeignKey(employees.emp_no,ondelete="CASCADE"),nullable=False)
    dept_no=Column(CHAR(4),ForeignKey(departments.dept_no,ondelete="CASCADE"),nullable=False)
    from_date=Column(Date,nullable=False)
    to_date=Column(Date,nullable=False)
    PrimaryKeyConstraint(emp_no, dept_no)

    def __repr__(self):
        return f'dept_manager {self.emp_no}'

class dept_emp(Base):
    __tablename__ = 'dept_emp'
    emp_no =Column(Integer,ForeignKey(employees.emp_no,ondelete="CASCADE"),nullable=False)
    dept_no=Column(CHAR(4),ForeignKey(departments.dept_no,ondelete="CASCADE"),nullable=False)
    from_date=Column(Date,nullable=False)
    to_date=Column(Date,nullable=False)
    PrimaryKeyConstraint(emp_no, dept_no)
    
    def __repr__(self):
        return f'dept_emp {self.emp_no}'

class titles(Base):
    __tablename__ = 'titles'
    emp_no =Column(Integer,ForeignKey(employees.emp_no,ondelete="CASCADE"),nullable=False)
    title=Column(String(50),nullable=False)
    from_date=Column(Date,nullable=False)
    to_date=Column(Date,nullable=True)
    PrimaryKeyConstraint(emp_no, title,from_date)

    def __repr__(self):
        return f'title {self.title}'

class salaries(Base):
    __tablename__ = 'salaries'
    emp_no =Column(Integer,ForeignKey(employees.emp_no,ondelete="CASCADE"),nullable=False)
    salary=Column(Integer,nullable=False)
    from_date=Column(Date,nullable=False)
    to_date=Column(Date,nullable=True)
    PrimaryKeyConstraint(emp_no,from_date)

    def __repr__(self):
        return f'salary {self.salary}'


app = Flask(__name__)


@app.route('/')

def index():
    db_session = scoped_session(sessionmaker(bind=engine))
    items=db_session.query(employees.first_name).limit(10)
    for item in items:
        print(item)
    return("online\n")

@app.route('/create')
def crt():
    Base.metadata.create_all(engine)
    return("created\n")

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

@app.route('/add_employee/<fname>/<lname>/<bdate>/<gndr>/<sal>/<dno>/<ttl>',methods=['POST'])
def addemp(fname,lname,bdate,gndr,sal,dno,ttl):
    
    
    dept_check=session.query(departments).filter(departments.dept_no==dno).first()
    
    if not dept_check  :
        return ("invalid dept_no \n")

    else:
        emp_chk=session.query(func.max(employees.emp_no)).first()[0]
        if emp_chk:
            empid=int(str(emp_chk))+1
        else :
            empid=1
        
        # empargs=(empid,bdate,fname,lname,gndr,date.today())
        emp=employees(emp_no=int(empid),birth_date=datetime.strptime(bdate, '%Y-%m-%d'),first_name=fname,last_name=lname,gender=gndr,hire_date=date.today())
        session.add(emp)
        session.commit()
        
        # dept_emp_args=(empid,dno,date.today(),"9999-01-01")
        deptemp=dept_emp(emp_no=int(empid),dept_no=dno,from_date=date.today(),to_date=datetime.strptime("9999-01-01", '%Y-%m-%d'))
        session.add(deptemp)
        session.commit()

        # titles_args=(empid,ttl,date.today(),"9999-01-01",)
        titl=titles(emp_no=int(empid),title=ttl,from_date=date.today(),to_date=datetime.strptime("9999-01-01", '%Y-%m-%d'))
        session.add(titl)
        session.commit()

        # salaries_args=(empid,sal,date.today(),"9999-01-01",)
        slr=salaries(emp_no=int(empid),salary=sal,from_date=date.today(),to_date=datetime.strptime("9999-01-01", '%Y-%m-%d'))
        session.add(slr)
        session.commit()

        return ("success\n")

@app.route('/employee_update/<empid>',methods=['PUT'])
def updt(empid):
    employee=employee = session.query(employees).filter(employees.emp_no==empid).first()
    if not employee  :
        return ("invalid employee id \n")
    else:
        args=request.args
        if args.get('fname'):
                employee = session.query(employees).filter(employees.emp_no==empid).first()
                setattr(employee, 'first_name', args.get('fname'))
                session.commit()
        if args.get('lname'):
                employee = session.query(employees).filter(employees.emp_no==empid).first()
                setattr(employee, 'last_name', args.get('lname'))
                session.commit()
        if args.get('bdate'):
                employee = session.query(employees).filter(employees.emp_no==empid).first()
                setattr(employee, 'birth_date', datetime.strptime(args.get('bdate'), '%Y-%m-%d'))
                session.commit()
        if args.get('gndr'):
                employee = session.query(employees).filter(employees.emp_no==empid).first()
                setattr(employee, 'gender', args.get('gndr'))
                session.commit()
        if args.get('sal'):
                salary = session.query(salaries).filter(salaries.emp_no==empid).first()
                setattr(salary, 'salary', args.get('sal'))
                session.commit()
        if args.get('dno'):
                dept_check=session.query(departments).filter(departments.dept_no==args.get('dno')).first()
                if not dept_check  :
                    return ("invalid dept_no \n")
                else:
                    deptemp = session.query(dept_emp).filter(dept_emp.emp_no==empid).first()
                    setattr(deptemp, 'dept_no', args.get('dno'))
                    session.commit()
        if args.get('ttl'):
                titl = session.query(titles).filter(titles.emp_no==empid).first()
                setattr(titl, 'title', args.get('ttl'))
                session.commit()
        return ("success\n")


@app.route('/employee_delete/<empid>',methods=['DELETE'])
def delt(empid):
    employee=employee = session.query(employees).filter(employees.emp_no==empid).first()
    if not employee  :
        return ("invalid employee id \n")
    session.delete(employee)
    session.commit()
    return("success\n")