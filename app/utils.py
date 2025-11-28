from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def limpar_e_padronizar_dado(dado_bruto):
    if not dado_bruto:
        return ""
    dado_limpo = dado_bruto.strip()
    dado_limpo = dado_limpo.lower()
    dado_limpo = dado_limpo.replace('.', '').replace(',', '')
    return dado_limpo

def role_required(role_name):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request() 
            except Exception:
                return jsonify(msg="Token inválido ou ausente"), 401
            
            claims = get_jwt()
            if claims.get('role') == role_name:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg=f"Acesso Proibido. Requer função: {role_name}"), 403
        return decorator
    return wrapper