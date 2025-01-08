from io import BytesIO
from reportlab.pdfgen import canvas

def generate_reservas_pdf_in_memory(reservas):
    """
    Genera un PDF en memoria con los datos de las reservas.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, "Reporte de Reservas")

    # Agregar cada reserva al PDF
    for idx, reserva in enumerate(reservas, start=1):
        cliente_info = f"{reserva['cliente']['id']} - {reserva['cliente']['nombre']} ({reserva['cliente']['telefono']})"
        pdf.drawString(100, 750 - idx * 20, f"Reserva {reserva['id']} - Fecha: {reserva['fecha']} - Cliente: {cliente_info}")
    
    pdf.save()
    buffer.seek(0)  # Posicionar el puntero al inicio del buffer
    return buffer
