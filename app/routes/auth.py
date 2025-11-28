from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.extensions import db, bcrypt
from app.models import Usuario, Funcao, UsuarioFuncao

# Criamos o Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    # 1. Pega o email e a senha do JSON enviado na requisição
    dados = request.get_json()
    email = dados.get('email', None)
    senha = dados.get('senha', None)

    # 2. Busca o usuário no banco pelo email
    usuario = Usuario.query.filter_by(email=email).first()

    # 3. Verifica se o usuário existe E se a senha está correta
    if usuario and bcrypt.check_password_hash(usuario.senha_hash, senha):
        # 4. Se deu certo, busca a função (role) do usuário
        usuario_funcao = UsuarioFuncao.query.filter_by(usuario_id=usuario.id).first()
        funcao = Funcao.query.get(usuario_funcao.funcao_id)
        role = funcao.nome_funcao if funcao else 'Desconhecido'

        # 5. Cria o Token JWT adicionando a 'role' dentro dele
        claims = {'role': role}
        access_token = create_access_token(identity=str(usuario.id), additional_claims=claims)

        
        return jsonify(access_token=access_token, user_role=role), 200

    # 6. Se o usuário ou senha estiverem errados
    return jsonify({"msg": "Email ou senha inválidos"}), 401

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    # 1. Pega os dados da requisição
    dados = request.get_json()
    email = dados.get('email')
    nome = dados.get('nome')
    senha = dados.get('senha')
    # ALTERADO: Se 'nome_funcao' não for enviado, assume 'User' como padrão
    nome_funcao = dados.get('nome_funcao', 'User') 

    # 2. Verifica se o usuário já existe
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"msg": "Este email já está cadastrado"}), 400

    # 3. Busca a função no banco. Se não existir, não permite o registro.
    funcao = Funcao.query.filter_by(nome_funcao=nome_funcao).first()
    if not funcao:
        return jsonify({"msg": f"Erro interno: Função '{nome_funcao}' não encontrada no banco. Verifique o seeding."}), 500

    # 4. Gera o hash da senha
    hash_da_senha = bcrypt.generate_password_hash(senha).decode('utf-8')

    # 5. Cria o novo usuário
    novo_usuario = Usuario(nome=nome, email=email, senha_hash=hash_da_senha)
    
    # 6. Salva o usuário no banco (1ª parte)
    db.session.add(novo_usuario)
    db.session.commit() # Commit para que o 'novo_usuario' receba um 'id'

    # 7. Cria a ligação na tabela usuarios_funcoes
    nova_ligacao = UsuarioFuncao(usuario_id=novo_usuario.id, funcao_id=funcao.id)
    db.session.add(nova_ligacao)
    db.session.commit() # Commit final

    return jsonify({"msg": "Usuário registrado com sucesso!"}), 201

@auth_bp.route('/api/meu-perfil', methods=['GET'])
@jwt_required()
def meu_perfil():
    
    # Pega o ID do usuário de dentro do token
    current_user_id = get_jwt_identity()
    
    # Pega as 'claims' (role) que adicionamos no token
    claims = get_jwt()
    role = claims.get('role', 'Desconhecido')

    # Busca o usuário no banco
    usuario = Usuario.query.get(current_user_id)

    return jsonify(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        minha_funcao=role
    ), 200