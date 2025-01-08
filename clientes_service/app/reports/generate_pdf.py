from io import BytesIO
from flask import send_file, jsonify
from reportlab.pdfgen import canvas

def generate_clientes_pdf_in_memory(clientes):
    """
    Genera un PDF en memoria con los datos de los clientes.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "Reporte de Clientes")
    for idx, cliente in enumerate(clientes, start=1):
        pdf.drawString(100, 750 - idx * 20, f"{cliente['id']} - {cliente['nombre']} - {cliente['telefono']}")
    pdf.save()
    buffer.seek(0) 
    return buffer
