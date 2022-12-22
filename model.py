from sqlalchemy.orm import relationship,backref
from sqlalchemy import create_engine,insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Date,Enum,CHAR,ForeignKey,PrimaryKeyConstraint
from sqlalchemy import create_engine,insert
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata=Base.metadata

class employees(Base):
    __tablename__ = 'employees'
    emp_no =Column(Integer, primary_key=True,nullable=False)
    birth_date=Column(Date,nullable=False)
    first_name=Column(String(14),nullable=False)
    last_name=Column(String(16),nullable=False)
    gender=Column(Enum('M','F'),nullable=False)
    hire_date=Column(Date,nullable=False)
    dept_emps= relationship("dept_emp",cascade='all, delete-orphan')
    salary= relationship("salaries",cascade='all, delete-orphan')

    # chkfield=Column(String,nullable=False)

    def __repr__(self):
        return f'employee {self.first_name}'

class departments(Base):
    __tablename__ = 'departments'
    dept_no=Column(CHAR(4),primary_key=True,nullable=False)
    dept_name=Column(String(40),unique=True,nullable=False)
    dept_emps= relationship("dept_emp",cascade='all, delete-orphan')
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
    departmentss = relationship("departments", back_populates="dept_emps")
    employee = relationship("employees", back_populates="dept_emps")
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
    # employee = relationship("employees", back_populates="salary")

    def __repr__(self):
        return f'salary {self.salary}'

