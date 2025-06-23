from flask import Blueprint, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

# mysql variable global para asignar en app.py
mysql = None

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/reporte/pdf')
def reportepdf():
    global mysql

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, correo, password, id_rol FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Definir estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0a3d62"),
        spaceAfter=20,
        spaceBefore=20,
    )

    elements.append(Paragraph("Reporte de Usuarios", title_style))
    elements.append(Spacer(1, 12))

    # Datos y cabecera
    data = [["ID", "Correo", "Password", "Rol"]]
    for u in usuarios:
        rol_str = "Administrador" if u['id_rol'] == 1 else "Usuario"
        data.append([str(u['id']), u['correo'], u['password'], rol_str])

    # Tabla con diseño
    table = Table(data, colWidths=[50, 200, 150, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0a3d62")),  # header azul oscuro
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),               # texto blanco header
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#1e3799")),  # líneas azules
        ('ROWBACKGROUNDS', (1, 0), (-1, -1), [colors.HexColor("#58c0c7"), colors.HexColor("#c7ecee")]),  # filas alternadas aqua claro
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#30336b")),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        download_name="usuarios_reporte.pdf",
        mimetype='application/pdf',
        as_attachment=False
    )
