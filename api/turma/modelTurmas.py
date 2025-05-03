from config import db
from professor.modelProf import Professor

class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(100))
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"), nullable=False)
    ativo = db.Column(db.Boolean)
    #professor = db.relationship("Professor", back_populates="turmas")

    def __init__(self, descricao, ativo):
        self.descricao = descricao
        self.ativo = ativo


    def to_dict(self):
        professor_data = None
        if self.professor_id:
            professor_data = {'id': self.professor_id} 

        return {'id': self.id,
               'descricao': self.descricao,
               'professor_id': self.professor_id,
               'ativo': self.ativo}


class TurmaNaoEncontrada(Exception):
    pass


def turma_por_id(idTurma):
    turma = Turma.query.get(idTurma)

    if not turma:
        raise TurmaNaoEncontrada("Turma não encontrada")
    return turma.to_dict()

def getTurma():
    turmas = Turma.query.all()
    print(turmas)
    return [turma.to_dict() for turma in turmas]

def apaga_tudo():
    try:
        db.session.query(Turma).delete()
        db.session.commit()
        return "message: Banco de dados resetado"
    except Exception as e:
        db.session.rollback()
        return f"Erro ao resetar o banco de dados: {e}"


def createTurma(descricao, professor_id, ativo=True):
    if not descricao or not professor_id:
        return {'erro': 'Parâmetros obrigatórios ausentes'}, 400

    if not isinstance(descricao, str):
        return {'erro': 'A descrição deve ser uma string'}, 400
    if not isinstance(professor_id, int):
        return {'erro': 'O ID do professor deve ser um número inteiro'}, 400
    if not isinstance(ativo, bool):
        return {'erro': 'O status ativo deve ser um booleano'}, 400
    
   
    professor_existe = Professor.query.get(professor_id)
    if not professor_existe:
        return {'erro': f'Professor com ID {professor_id} não encontrado'}, 404

    nova_turma = Turma(descricao=descricao, ativo=ativo)
    nova_turma.professor_id = professor_id 
    db.session.add(nova_turma)
    db.session.commit()
    return nova_turma.to_dict(), 201

def deleteTurma(idTurma):
    turma = Turma.query.get(idTurma)
    if not turma:
        raise TurmaNaoEncontrada
    db.session.delete(turma)
    db.session.commit()
    return 'mensagem: Turma deletada com sucesso', turma


def atualizarTurma(idTurma, descricao=None, professor=None):
    try:
        turma_encontrada = Turma.query.get(idTurma)
        if turma_encontrada is None:
            raise TurmaNaoEncontrada("Turma não encontrada")

        if descricao is None and professor is None:
            return 'erro: Pelo menos um dos campos "descricao" ou "professor" deve ser fornecido', None

        if descricao and not isinstance(descricao, str):
            return 'erro: O descricao deve ser uma string', None
        if professor and not isinstance(professor, str):
            return 'erro: O professor deve ser uma string', None

        if descricao:
            turma_encontrada.descricao = descricao
        if professor:
            turma_encontrada.professor = professor

        db.session.commit()

        return "mensagem: Turma atualizada com sucesso", turma_encontrada.to_dict()

    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None


def atualizarParcialTurma(idTurma, dados):
    try:
        turma_encontrada = Turma.query.get(idTurma)
        if turma_encontrada is None:
            raise TurmaNaoEncontrada("Turma não encontrada")

        for chave, valor in dados.items():
            if hasattr(turma_encontrada, chave):
                setattr(turma_encontrada, chave, valor)

        db.session.commit()
        return "mensagem: Turma atualizada com sucesso", turma_encontrada.to_dict()

    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None

# print(turma_por_id(28))
# print(getTurma())
# print(createTurma(2,'ads','caio'))
# print(deleteTurma(1))
# print(atualizarTurma(28, nome='bd', professor=None))
# print(atualizarParcialTurma(2,{'professor':'luana'}))
