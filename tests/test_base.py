
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker,Session,close_all_sessions
from sqlalchemy import create_engine
import os
from model import *
from unittest import mock
import model
import json
os.environ['env'] = 'test'
from app import app # Flask instance of the API
app.testing = True
from datetime import datetime

@pytest.fixture(scope="session")
def connection():
    engine = create_engine(
        "mysql+pymysql://{}:{}@{}/{}".format(
            os.environ.get('testusr'),
            os.environ.get('testpw'),
            os.environ.get('dbhost'),
            os.environ.get('testdb'),
        )
    )
    engine.connect()
    return engine

@pytest.fixture(scope="session")
def setup_database(connection):
    model.Base.metadata.bind = connection
    model.Base.metadata.create_all()
    print("created")
    yield
    print("dropped")
    model.Base.metadata.drop_all()

    

@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    close_all_sessions()
    
    
def rnd_entry(db_session):
    dpt=[
        {   
            "dept_no":"0001",
            "dept_name":"CS"
            
        },
    ]
    employee = [
        {
            "emp_no":"1",
            "birth_date":"1999,12,12",
            "first_name":"nizam",
            "last_name":"elahi",
            "gender":"M",
            "hire_date":"2000,12,12",
        },  
    ]

    dptemp=[
        {

            "emp_no":"1",
            "dept_no":"0001",
            "from_date":"1233,11,12",
            "to_date":"1111,12,12",

        },
    ]   
    mgr=[
        {

            "emp_no":"1",
            "dept_no":"0001",
            "from_date":"1122,12,12",
            "to_date":"3221,12,12",

        },
    ] 
    ttls=[
        {
            "emp_no":"1",
            "title":"nottl",
            "from_date":"1232,12,12",
            "to_date":"2113,12,12",
        },
    ]

    slr=[{
            "emp_no":"1",
            "salary":"3231",
            "from_date":"1111,12,12",
            "to_date":"4321,12,12",

    },
    ]
    for d in dpt:
        dptt=departments(**d)
        db_session.add(dptt)
    db_session.commit()

    for e in employee:
        emp = employees(**e)
        db_session.add(emp)
    db_session.commit()

    for e in mgr:
        mngr = dept_manager(**e)
        db_session.add(mngr)
    db_session.commit()
    
    for e in dptemp:
        demp = dept_emp(**e)
        db_session.add(demp)
    db_session.commit()

    for e in ttls:
        tl = titles(**e)
        db_session.add(tl)
    db_session.commit()
    
    for e in slr:
        sl = salaries(**e)
        db_session.add(sl)
    db_session.commit()



def test_getemp(db_session):
    
    rnd_entry(db_session)
    response = app.test_client().get('/employee_details')
    assert response.status_code==200
    rspns=json.loads(response.data.decode('utf-8'))
    for resp in rspns:
        assert resp['dept_name']== "CS"
        assert resp['dept_no']=="0001"
        assert resp["emp_no"]==1
        assert resp["first_name"]=="nizam"
        assert resp["last_name"]=="elahi"
        assert resp["salary"]==3231
        assert resp["title"]=="nottl"

def test_getdeptemp(db_session):
    
    response = app.test_client().get('/department_details')
    assert response.status_code==200
    rspns=json.loads(response.data.decode('utf-8'))
    for resp in rspns:
        assert resp['dept_name']== "CS"
        assert resp['dept_no']=="0001"
        assert resp["emp_no"]==1
        assert resp["first_name"]=="nizam"
        assert resp["last_name"]=="elahi"
        assert datetime.strptime(resp["from_date"], "%a, %d %b %Y %H:%M:%S %Z").date()==datetime.strptime("1122,12,12", "%Y,%m,%d").date()
        assert datetime.strptime(resp["to_date"], "%a, %d %b %Y %H:%M:%S %Z").date()==datetime.strptime("3221,12,12", "%Y,%m,%d").date()

    
def test_addemp(db_session):
    response = app.test_client().post('/add_employee/nizam/elahi/1997-01-01/M/1234/0001/notitle')
    assert response.status_code==200
    emp=db_session.query(employees).filter(employees.emp_no==2).first()
    assert emp.first_name=="nizam"
    assert emp.last_name=="elahi"
    assert emp.birth_date==datetime.strptime("1997-01-01", "%Y-%m-%d").date()
    assert emp.gender=="M"
    slr=db_session.query(salaries).filter(salaries.emp_no==2).first()
    assert slr.salary==1234
    dpt=db_session.query(dept_emp).filter(dept_emp.emp_no==2).first()
    assert dpt.dept_no=="0001"
    ttl=db_session.query(titles).filter(titles.emp_no==2).first()
    assert ttl.title=="notitle"


def test_updateemp(db_session):
    response = app.test_client().put('/employee_update/2?fname=nzm&lname=elh&bdate=1999-02-02&gndr=F&sal=1111&dno=0001&ttl=yestitle')
    assert response.status_code==200
    emp=db_session.query(employees).filter(employees.emp_no==2).first()
    assert emp.first_name=="nzm"
    assert emp.last_name=="elh"
    assert emp.birth_date==datetime.strptime("1999-02-02", "%Y-%m-%d").date()
    assert emp.gender=="F"
    slr=db_session.query(salaries).filter(salaries.emp_no==2).first()
    assert slr.salary==1111
    dpt=db_session.query(dept_emp).filter(dept_emp.emp_no==2).first()
    assert dpt.dept_no=="0001"
    ttl=db_session.query(titles).filter(titles.emp_no==2).first()
    assert ttl.title=="yestitle"


def test_relationship(db_session):
    response = app.test_client().get('/deptemps/CS')
    assert response.status_code==200
    rspns=json.loads(response.data.decode('utf-8'))
    
    resplist=rspns[1]
    resp={}
    for a in resplist:
        resp.update(a)
    assert resp["emp_no"]==2
    assert resp["fname"]=="nzm"
    assert resp["lname"]=="elh"

def test_del(db_session):
    response = app.test_client().delete('/employee_delete/2')
    assert response .status_code==200
    chk=db_session.query(employees).filter(employees.emp_no==2).first()
    assert not(chk)





















