from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import DadoProcessado
from app.utils import role_required, limpar_e_padronizar_dado

dados_bp = Blueprint('dados', __name__)

@dados_bp.route('/api/dados/processar', methods=['POST'])
@role_required('Admin')
def processar_dado():
    dados = request.get_json()
    dado_bruto = dados.get('dado')

    if not dado_bruto:
        return jsonify({"msg": "Campo 'dado' é obrigatório."}), 400

    # 1. Rotina de Limpeza e Padronização (Req. 1)
    dado_limpo = limpar_e_padronizar_dado(dado_bruto)

    # 2. Validação de Duplicação (Req. 2)
    if DadoProcessado.query.filter_by(dado_limpo=dado_limpo).first():
        return jsonify({"msg": f"Duplicação detectada. O dado padronizado '{dado_limpo}' já existe."}), 409 # Conflict

    # 3. Salva no Banco
    current_user_id = get_jwt_identity()
    novo_dado = DadoProcessado(
        dado_bruto=dado_bruto,
        dado_limpo=dado_limpo,
        processado_por_id=current_user_id
    )
    
    db.session.add(novo_dado)
    db.session.commit()

    return jsonify({"msg": "Dado processado e salvo com sucesso!", "dado_processado": novo_dado.to_json()}), 201

@dados_bp.route('/api/dados/processados', methods=['GET'])
@jwt_required()
def get_dados_processados():
    """
    Retorna todos os dados processados no banco.
    """
    # Busca todos os dados processados, ordenados por data de processamento
    dados = DadoProcessado.query.order_by(DadoProcessado.data_processamento.desc()).all()
    
    # Converte a lista de objetos para JSON usando o método to_json()
    return jsonify([dado.to_json() for dado in dados]), 200