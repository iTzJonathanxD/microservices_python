from flask import Flask, send_file, jsonify, Blueprint
from app.models import DetalleReserva, Reserva, Menu
from app.reports.generate_pdf import generate_detalles_reserva_pdf_in_memory
import os

reporte = Blueprint("reportes", __name__)

@reporte.route('/detalles_reserva/reporte', methods=['GET'])
def generate_detalles_reserva_report():
    """
    Genera un reporte PDF de todos los detalles de reserva y lo devuelve como respuesta.
    """
    try:
        # Obtener todos los detalles de reserva de la base de datos
        detalles = DetalleReserva.query.all()
        if not detalles:
            return jsonify({"error": "No hay detalles de reserva registrados para generar el reporte"}), 404

        detalles_data = [
            {
                "id": d.id_detalle_reserva,
                "id_reserva": d.id_reserva,
                "id_menu": d.id_menu,
                "cantidad": d.cantidad,
                "menu_nombre": d.menu.nombre_menu,  
                "reserva_fecha": d.reserva.fecha_reserva.strftime("%Y-%m-%d")
            }
            for d in detalles
        ]

        pdf_buffer = generate_detalles_reserva_pdf_in_memory(detalles_data)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="detalles_reserva_report.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": f"Error al generar el reporte: {str(e)}"}), 500
