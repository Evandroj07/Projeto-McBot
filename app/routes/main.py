from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import role_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/recurso-publico', methods=['GET'])
def recurso_publico():
    return jsonify(mensagem="Você acessou um recurso público!"), 200

@main_bp.route('/api/recurso-logado', methods=['GET'])
@jwt_required()
def recurso_logado():
    current_user_id = get_jwt_identity()
    return jsonify(mensagem=f"Recurso para usuários logados. Seu ID: {current_user_id}"), 200

@main_bp.route('/api/admin/painel', methods=['GET'])
@role_required('Admin')
def painel_admin():
    current_user_id = get_jwt_identity()
    return jsonify(mensagem=f"Bem-vindo ao Painel de Administração! Acesso exclusivo do Admin ID: {current_user_id}"), 200