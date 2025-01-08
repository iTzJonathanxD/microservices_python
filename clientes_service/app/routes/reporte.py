from flask import Flask, send_file, jsonify,Blueprint
from app.models import Cliente
from app.reports.generate_pdf import generate_clientes_pdf_in_memory
import os

reporte = Blueprint("reportes",__name__)

@reporte.route('/clientes/reporte', methods=['GET'])
def generate_clientes_report():
    """
    Genera un reporte PDF de todos los clientes y lo devuelve como respuesta.
    """
    try:
        # Obtener todos los clientes de la base de datos
        clientes = Cliente.query.all()
        if not clientes:
            return jsonify({"error": "No hay clientes registrados para generar el reporte"}), 404

        clientes_data = [{"id": c.id_cliente, "nombre": c.nombre_cliente, "telefono": c.telefono_cliente} for c in clientes]

        # Generar el PDF en memoria
        pdf_buffer = generate_clientes_pdf_in_memory(clientes_data)

        # Enviar el archivo directamente como descarga
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="clientes_report.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": f"Error al generar el reporte: {str(e)}"}), 500
