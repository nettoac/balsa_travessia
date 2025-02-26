from flask import Blueprint, request, jsonify
from ..services.registro_service import RegistroService

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registros', methods=['GET'])
def get_registros():
    registros = RegistroService.get_all_registros()
    return jsonify([registro.to_dict() for registro in registros])

@registro_bp.route('/registros', methods=['POST'])
def create_registro():
    data = request.get_json()
    registro = RegistroService.create_registro(data)
    return jsonify(registro.to_dict()), 201