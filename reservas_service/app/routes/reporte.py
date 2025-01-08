from flask import Flask, send_file, jsonify, Blueprint
from app.models import Reserva
from app.reports.generate_pdf import generate_reservas_pdf_in_memory

reporte_reservas = Blueprint("reportes_reservas", __name__)

@reporte_reservas.route('/reservas/reporte', methods=['GET'])
def generate_reservas_report():
    """
    Genera un reporte PDF de todas las reservas y lo devuelve como respuesta.
    """
    try:
        # Obtener todas las reservas de la base de datos
        reservas = Reserva.query.all()
        if not reservas:
            return jsonify({"error": "No hay reservas registradas para generar el reporte"}), 404

        reservas_data = [
            {
                "id": r.id_reserva,
                "fecha": r.fecha_reserva.strftime("%Y-%m-%d"),
                "cliente": {
                    "id": r.cliente.id_cliente,
                    "nombre": r.cliente.nombre_cliente,
                    "telefono": r.cliente.telefono_cliente
                }
            } for r in reservas
        ]

        # Generar el PDF en memoria
        pdf_buffer = generate_reservas_pdf_in_memory(reservas_data)

        # Enviar el archivo directamente como descarga
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="reservas_report.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": f"Error al generar el reporte: {str(e)}"}), 500
