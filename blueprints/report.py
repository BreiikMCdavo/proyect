from flask import Blueprint, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from models.employee import Employee, Attendance
from app import db
from sqlalchemy import func

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/employees_attendance_pdf')
def employees_attendance_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0a3d62"),
        spaceAfter=20,
    )

    elements.append(Paragraph("Reporte de Empleados y Asistencia", title_style))
    elements.append(Spacer(1, 12))

    # Construir datos para la tabla
    data = [["ID", "Nombre", "Designación", "Departamento", "Fecha Ingreso", "Días Presentes", "Días Ausentes"]]

    # Consulta para obtener resumen de asistencia por empleado
    empleados = db.session.query(Employee).all()
    for emp in empleados:
        presentes = db.session.query(func.count(Attendance.id)).filter(
            Attendance.employee_id == emp.id, Attendance.status == 'present').scalar() or 0
        ausentes = db.session.query(func.count(Attendance.id)).filter(
            Attendance.employee_id == emp.id, Attendance.status == 'absent').scalar() or 0

        data.append([
            str(emp.id),
            emp.name,
            emp.designation,
            emp.department,
            emp.date_of_joining.strftime('%Y-%m-%d'),
            str(presentes),
            str(ausentes)
        ])

    # Crear tabla con estilos
    table = Table(data, colWidths=[30, 110, 110, 90, 75, 65, 65])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0a3d62")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor("#1e3799")),
        ('ROWBACKGROUNDS', (1, 0), (-1, -1), [colors.HexColor("#dff9fb"), colors.HexColor("#c7ecee")]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#30336b")),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        download_name="reporte_empleados_asistencia.pdf",
        mimetype='application/pdf',
        as_attachment=False
    )
@report_bp.route('/employee_attendance/<int:employee_id>')
def employee_attendance(employee_id):   
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0a3d62"),
        spaceAfter=20,
    )

    elements.append(Paragraph(f"Reporte de Asistencia del Empleado ID {employee_id}", title_style))
    elements.append(Spacer(1, 12))

    # Datos del empleado
    empleado = Employee.query.get(employee_id)
    if not empleado:
        return "Empleado no encontrado", 404

    data = [
        ["ID", "Nombre", "Designación", "Departamento", "Fecha Ingreso"],
        [str(empleado.id), empleado.name, empleado.designation, empleado.department, empleado.date_of_joining.strftime('%Y-%m-%d')]
    ]

    # Asistencia del empleado
    asistencias = Attendance.query.filter_by(employee_id=employee_id).all()
    if not asistencias:
        data.append(["No hay registros de asistencia para este empleado."])
    else:
        data.append(["Fecha", "Estado"])
        for asistencia in asistencias:
            data.append([asistencia.date.strftime('%Y-%m-%d'), asistencia.status])

    # Crear tabla con estilos
    table = Table(data, colWidths=[30, 110, 110, 90, 75])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0a3d62")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor("#1e3799")),
        ('ROWBACKGROUNDS', (1, 0), (-1, -1  ), [colors.HexColor("#dff9fb"), colors.HexColor("#c7ecee")]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#30336b")),
    ]))