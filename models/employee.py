from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    """
    The Employee model represents an employee in the HRMS system.
    
    Attributes:
    - id (int): The unique identifier for the employee.
    - name (str): The name of the employee.
    - designation (str): The employee's designation or job title.
    - date_of_joining (date): The date when the employee joined the company.
    - department (str): The department to which the employee belongs.
    - attendance (relationship): A relationship that links to the attendance records of the employee.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)  # Attribute for designation
    date_of_joining = db.Column(db.Date, nullable=False)      # Attribute for date of joining
    department = db.Column(db.String(100), nullable=False)    # New attribute for department
    attendance = db.relationship('Attendance', backref='employee', lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the Employee instance.

        Example:
        '<Employee John Doe, Designation: Software Engineer, Department: IT>'
        """
        return f'<Employee {self.name}, Designation: {self.designation}, Department: {self.department}>'


class Attendance(db.Model):
    """
    The Attendance model represents attendance records for each employee.
    
    Attributes:
    - id (int): The unique identifier for the attendance record.
    - employee_id (int): The foreign key that links to an employee.
    - date (date): The date when the attendance record was created. Defaults to the current date.
    - status (str): The attendance status for the day, either 'present' or 'absent'.
    """

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(10))  # 'present' or 'absent'

    def __repr__(self):
        """
        Returns a string representation of the Attendance instance.

        Example:
        '<Attendance for Employee ID 1, Date: 2024-10-01, Status: present>'
        """
        return f'<Attendance for Employee ID {self.employee_id}, Date: {self.date}, Status: {self.status}>'
