from turma.modelTurmas import Turma
from datetime import datetime, date
from config import db

class Aluno(db.Model):
    __tablename__ = "alunos"

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    media_final = db.Column(db.Float, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)

    def __init__(self, nome, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, turma_id, media_final):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.turma_id = turma_id
        self.media_final = media_final
        self.idade = self.calcular_idade()

    def calcular_idade(self):
        today = date.today()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

    def to_dict(self):  
        return {'id': self.id, 
                'nome': self.nome, "idade": self.idade, 
                'data_nascimento': self.data_nascimento.isoformat(),
                "nota_primeiro_semestre": self.nota_primeiro_semestre, 
                "nota_segundo_semestre": self.nota_segundo_semestre, 
                "turma_id": self.turma_id, 
                "media_final": self.media_final}
    

class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise  AlunoNaoEncontrado("Aluno não encontrado")
    return aluno.to_dict()

def get_alunos():
    alunos = Aluno.query.all()
    print(alunos)
    return [aluno.to_dict() for aluno in alunos]


def apaga_tudo():
    try:
        db.session.query(Aluno).delete()
        db.session.commit()
        return "message: Banco de dados resetado"
    except Exception as e:
        db.session.rollback()
        return f"Erro ao resetar o banco de dados: {e}"


def create_aluno(novos_dados):
    turma = Turma.query.get(novos_dados['turma_id'])
    if turma is None:
        return None, "Turma não existe"

    campos_obrigatorios = ['nome', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'turma_id']
    for campo in campos_obrigatorios:
        if campo not in novos_dados:
            return None, f'Parâmetro obrigatório ausente: {campo}'

    if not isinstance(novos_dados['nome'], str):
        return None, 'O nome deve ser uma string'

    try:
        datetime.strptime(novos_dados['data_nascimento'], "%Y-%m-%d").date()
    except ValueError:
        return None, 'Formato de data de nascimento inválido (AAAA-MM-DD)'

    try:
        nota_primeiro_semestre = float(novos_dados['nota_primeiro_semestre'])
        nota_segundo_semestre = float(novos_dados['nota_segundo_semestre'])
        if not 0 <= nota_primeiro_semestre <= 10 or not 0 <= nota_segundo_semestre <= 10:
            return None, 'As notas devem estar entre 0 e 10'
    except ValueError:
        return None, 'As notas devem ser números'

    try:
        turma_id = int(novos_dados['turma_id'])
        if turma_id <= 0:
            return None, 'O ID da turma deve ser um número inteiro positivo'
    except ValueError:
        return None, 'O ID da turma deve ser um número inteiro'

    novo_aluno = Aluno(
        nome=novos_dados['nome'],
        data_nascimento=datetime.strptime(novos_dados['data_nascimento'], "%Y-%m-%d").date(),
        nota_primeiro_semestre=nota_primeiro_semestre,
        nota_segundo_semestre=nota_segundo_semestre,
        turma_id=turma_id,
        media_final=(nota_primeiro_semestre + nota_segundo_semestre) / 2,
    )

    db.session.add(novo_aluno)
    db.session.commit()

    return novo_aluno, None


def atualizarAluno(id_aluno, nome=None, body_id=None, data_nasc=None):
    try:
        aluno_encontrado = Aluno.query.get(id_aluno)
        if aluno_encontrado is None:
            raise AlunoNaoEncontrado("Aluno não encontrado")

        if nome is None:
            if body_id is None or body_id == id_aluno:
                return 'erro: aluno sem nome', None

        if nome is not None and not isinstance(nome, str):
            return 'erro: O nome deve ser uma string', None
        
        if data_nasc is not None:
            try:
                aluno_encontrado.data_nascimento = datetime.strptime(data_nasc['data_nascimento'], "%Y-%m-%d").date()
            except ValueError:
                return 'erro: Formato de data de nascimento inválido (AAAA-MM-DD)', None
            
        if body_id is not None and not isinstance(body_id, int):
            return 'erro: O id deve ser um número inteiro', None
        
        if body_id != id_aluno:
                aluno_com_id_conflict = Aluno.query.get(body_id)
                if aluno_com_id_conflict:
                    return 'erro: ID de aluno já existe'
                aluno_encontrado.id = body_id
        if nome:
            aluno_encontrado.nome = nome
        db.session.commit()

        return "mensagem: aluno atualizado com sucesso", aluno_encontrado.to_dict()
    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None
    
def atualizarParcialAluno(id_aluno,dados):
    try:
        aluno_encontrado = Aluno.query.get(id_aluno)
        if aluno_encontrado is None:
            raise AlunoNaoEncontrado("Aluno não encontrado")

        for chave, valor in dados.items():
            if hasattr(aluno_encontrado, chave):
                setattr(aluno_encontrado, chave, valor)

        db.session.commit()
        return "mensagem: aluno atualizada com sucesso", aluno_encontrado.to_dict()

    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None
    
def deleteAluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado("Aluno não encontrado")
    db.session.delete(aluno)
    db.session.commit()
    return 'mensagem: Aluno deletado com sucesso', aluno
    