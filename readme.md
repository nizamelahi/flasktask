edit .env file with your database details <br>
db used: 
https://github.com/datacharmer/test_db 
 
endpoints: 
 
POST /employee/\<fname\>/\<lname\>/\<bdate\>/\<gender\>/\<salary\>/\<dno\>/\<title\>  <br>
response :
success/invalid dept_no
 
GET /employee_details 
response: 
json with departments.dept_no, departments.dept_name, employees.emp_no, employees.first_name, employees.last_name,from_date,to_date 
 
GET /department_details 
response: 
json with employees.emp_no, first_name, last_name, dept_emp.dept_no, departments.dept_name, title, salary 

