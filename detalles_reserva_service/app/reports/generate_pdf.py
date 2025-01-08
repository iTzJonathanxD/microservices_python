from reportlab.pdfgen import canvas
from io import BytesIO

def generate_detalles_reserva_pdf_in_memory(detalles):
    """
    Genera un archivo PDF en memoria con los detalles de reserva proporcionados.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 800, "Reporte de Detalles de Reserva")
    y_position = 750

    for detalle in detalles:
        pdf.drawString(100, y_position, f"ID: {detalle['id']}, Reserva: {detalle['id_reserva']} ({detalle['reserva_fecha']}), "
                                        f"Menú: {detalle['menu_nombre']} (ID: {detalle['id_menu']}), Cantidad: {detalle['cantidad']}")
        y_position -= 20

    pdf.save()
    buffer.seek(0)
    return buffer
