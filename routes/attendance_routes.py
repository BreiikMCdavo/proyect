from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.employee import db, Employee, Attendance
from datetime import datetime 

# Define the blueprint for attendance-related routes
attendance_blueprint = Blueprint('attendance', __name__)

@attendance_blueprint.route('/employees')
def all_employees():
    """
    Renders a page displaying all employees in the database.

    Returns:
    - HTML template rendering all employees.
    """
    employees = Employee.query.all()
    return render_template('all_employees.html', employees=employees)

@attendance_blueprint.route('/update_attendance/<int:employee_id>', methods=['POST'])
def update_attendance(employee_id):
    """
    Updates the attendance status (present or absent) for a specific employee.

    Parameters:
    - employee_id (int): The unique ID of the employee.

    Returns:
    - Redirects back to the all employees page after updating the attendance.
    """
    status = request.form.get('status')  # 'present' or 'absent'
    attendance = Attendance(employee_id=employee_id, status=status)
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for('attendance.all_employees'))

@attendance_blueprint.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    """
    Adds a new employee to the database. Supports both GET and POST requests.
    
    GET: Displays the form to add a new employee.
    POST: Processes the form submission and adds the new employee to the database.

    Returns:
    - On GET: Renders the employee addition form.
    - On POST: Redirects to the all employees page after adding the employee.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        designation = request.form.get('designation')
        date_of_joining = request.form.get('date_of_joining')
        doj = datetime.strptime(date_of_joining, '%Y-%m-%d').date()
        department = request.form.get('department')

        # Validate the form input
        if not name or not designation or not date_of_joining:
            return jsonify({
                "Enter all details": "Please fill in all required fields."
            })

        # Add new employee to the database
        new_employee = Employee(name=name, designation=designation, date_of_joining=doj, department=department)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('attendance.all_employees'))

    return render_template('add_employee.html')

@attendance_blueprint.route('/overview/<string:department>')
def overview(department):
    """
    Provides an overview of attendance for all employees in a specific department.
    
    Parameters:
    - department (str): The name of the department for which to display attendance overview.

    Returns:
    - Renders an overview page with employee attendance details, including counts of present and absent employees.
    """
    # Get all employees in the specified department
    employees = Employee.query.filter_by(department=department).all()
    attendances = []

    # Counters for present and absent statuses
    present_count = 0
    absent_count = 0
    
    # Collect attendance records for each employee in the department
    for employee in employees:
        employee_attendance = Attendance.query.filter_by(employee_id=employee.id).all()
        attendances.append({
            'employee': employee,
            'attendance': employee_attendance
        })

        # Count present and absent statuses
        for attendance in employee_attendance:
            if attendance.status == 'present':
                present_count += 1
            elif attendance.status == 'absent':
                absent_count += 1
                
    return render_template('overview.html', 
                           department=department, 
                           attendances=attendances,
                           present_count=present_count, 
                           absent_count=absent_count)

@attendance_blueprint.route("/",methods=['GET'])
def welcome():
    return render_template('welcome.html')
