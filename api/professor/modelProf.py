# dici = {
#         "professores" : [
#         {"id":1,"nome":"carlos", "idade":30, "materia":"matematica", "observacao":"bom professor"}
#         ,{"id":2,"nome":"lucas", "idade":34, "materia":"POO", "observacao":"bom professor"} 
#         ]
# }
from config import db


class Professor(db.Model):
    __tablename__ = "professor"

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100))
    observacao = db.Column(db.String(200))

   # turmas = db.relationship("Turma", back_populates="professor")

    def __init__(self, nome, idade, materia, observacao):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacao = observacao

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacao': self.observacao
        }



class ProfessorNaoEncontrado(Exception):
    pass


def professor_por_id(id_professor):  
    professor = Professor.query.get(id_professor)
    if not professor:
        raise  ProfessorNaoEncontrado('Professor não encontrado')
    return professor.to_dict()


def get_professores():
    professores = Professor.query.all()
    print(professores)
    return [professor.to_dict() for professor in professores]

def apaga_tudo():
    try:
        db.session.query(Professor).delete()
        db.session.commit()
        return "message: Banco de dados resetado"
    except Exception as e:
        db.session.rollback()
        return f"Erro ao resetar o banco de dados: {e}"


def create_professores(nome, idade, materia, observacao):
    if not nome or not idade or not materia:
        return {'erro': 'Parâmetro obrigatório ausente'}, 400

    if not isinstance(nome, str):
        return {'erro': 'O nome deve ser uma string'}, 400
    if not isinstance(idade, int):
        return {'erro': 'A idade deve ser um número inteiro'}, 400
    if not isinstance(materia, str):
        return {'erro': 'A matéria deve ser uma string'}, 400
    if observacao is not None and not isinstance(observacao, str):
        return {'erro': 'A observação deve ser uma string'}, 400

    novo_prof = Professor(nome=nome, idade=idade, materia=materia, observacao=observacao)
    db.session.add(novo_prof)
    db.session.commit()
    return novo_prof.to_dict(), 201


def atualizarProfessor(id_professor, nome=None, idade=None, materia=None, observacao=None, body_id=None):
    try:
        professor_encontrado = Professor.query.get(id_professor)
        if professor_encontrado is None:
            raise ProfessorNaoEncontrado('Professor não encontrado')

        if nome is None:
            if body_id is None or body_id == id_professor:
                return 'erro: professor sem nome', None

        if nome and not isinstance(nome, str):
            return 'erro: O nome deve ser uma string', None

        if idade and not isinstance(idade, int):
            return 'erro:  a idade deve ser um numero inteiro', None

        if materia and not isinstance(materia, str):
            return 'erro:  a materia deve ser uma string', None

        if observacao and not isinstance(observacao, str):
            return 'erro:  a observacao deve ser uma string', None

        if body_id is not None and not isinstance(body_id, int):
            return 'erro: O id deve ser um número inteiro', None

        if body_id is not None and body_id != id_professor:
            professor_com_id_conflict = Professor.query.get(body_id)
            if professor_com_id_conflict:
                return 'erro: ID de professor já existe', None

        if nome is not None:
            professor_encontrado.nome = nome
        if idade is not None:
            professor_encontrado.idade = idade
        if materia is not None:
            professor_encontrado.materia = materia
        if observacao is not None:
            professor_encontrado.observacao = observacao
        if body_id is not None:
            professor_encontrado.id = body_id

        db.session.commit()

        return "mensagem: Professor atualizado com sucesso", professor_encontrado.to_dict()
    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}", None


def atualizarParcialProfessor(id_professor, dados):
    try:
        professor_encontrado = Professor.query.get(id_professor)
        if not professor_encontrado:
            raise ProfessorNaoEncontrado("Professor não encontrado")

        for chave, valor in dados.items():
            if hasattr(professor_encontrado, chave):
                setattr(professor_encontrado, chave, valor)

        db.session.commit()
        return "mensagem: Professor atualizada com sucesso", professor_encontrado.to_dict()

    except Exception as e:
        db.session.rollback()
        return f"erro: {str(e)}"


def deleteProfessor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
         raise ProfessorNaoEncontrado("Professor não encontrado")
    db.session.delete(professor)
    db.session.commit()
    return 'mensagem: Professor deletado com sucesso', professor


#print(professor_por_id(1))
#print(get_professores())
#print(create_professores(dici, 3,'lucas', 34, 'POO', 'bom professor'))
#print("-------------------------------")
#print(delete_profesor(1))
#print(apaga_tudo())
#print(get_professores())
#print(update_professor(3, {'nome': 'caio', 'idade': 50, 'materia': 'portugues', 'observacao': 'otimo professor'}))
#print(patch_professor(2,{'nome':'lua'}))

