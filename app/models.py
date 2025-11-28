from sqlalchemy.dialects.mysql import INTEGER
from app.extensions import db # Importamos o db do arquivo extensions

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

class Funcao(db.Model):
    __tablename__ = 'funcoes'
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    nome_funcao = db.Column(db.String(50), unique=True, nullable=False)

class UsuarioFuncao(db.Model):
    __tablename__ = 'usuarios_funcoes'
    usuario_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('usuarios.id'), primary_key=True)
    funcao_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('funcoes.id'), primary_key=True)

class DadoProcessado(db.Model):
    __tablename__ = 'dados_processados'
    id = db.Column(db.Integer, primary_key=True)
    dado_bruto = db.Column(db.String(255), nullable=False)
    dado_limpo = db.Column(db.String(255), unique=True, nullable=False)
    processado_por_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('usuarios.id'), nullable=False)
    data_processamento = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_json(self):
        return {
            'id': self.id,
            'dado_bruto': self.dado_bruto,
            'dado_limpo': self.dado_limpo,
            'processado_por_id': self.processado_por_id,
            'data_processamento': self.data_processamento.isoformat() if self.data_processamento else None
        }