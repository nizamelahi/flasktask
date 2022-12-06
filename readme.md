edit .env file with your database details <br>
db generated via sqlalchemy <br>
use instructions on the page for installation<br><br>
Endpoints: 
 
POST /add_employee/\<fname\>/\<lname\>/\<bdate\>/\<gender\>/\<salary\>/\<dno\>/\<title\><br>
response :
success/invalid dept_no
 
GET /employee_details?limit=_lmt_&offset=_offset_<br> 
limit and offset parameters deafult to 100 and 0 respectively if not provided. 
response: 
json with departments.dept_no, departments.dept_name, employees.emp_no, employees.first_name, employees.last_name,from_date,to_date 
 
GET /department_details?limit=_lmt_&offset=_offset_<br> 
limit and offset parameters deafult to 100 and 0 respectively if not provided. 
response: 
json with employees.emp_no, first_name, last_name, dept_emp.dept_no, departments.dept_name, title, salary 
 
PUT /employee_update/\<empid\> <br>
available arguments: 
fname,lname,bdate,gndr,sal,dno,ttl 
response :
success/invalid dept_no/invalid employee id
 
DELETE /employee_delete/<empid> <br>
response :
success/invalid employee id
