dici = {
    "alunos":[
        {"id":1,"nome":"Joao"},
        {"id":2,"nome":"Maria"},
        {"id":3,"nome":"Pedro"}
    ] 
}

class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    for aluno in dici['alunos']:
        if aluno['id'] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado

def get_alunos():
    return dici['alunos']


def apaga_tudo():
    dici['alunos'] = []
    return "message: Banco de dados resetado"


def create_aluno(id, nome):
    if not id or not nome:
        return {'erro': 'Parâmetro obrigatório ausente'}

    if not isinstance(id, int) or id <= 0:
        return {'erro': 'O id deve ser um número inteiro'}

    if not isinstance(nome, str):
        return {'erro': 'O nome deve ser uma string'}

    for aluno in dici["alunos"]:
        if aluno['id'] == id:
            return {'erro': 'id ja utilizada'}

    return {'id': id, 'nome': nome}


def atualizarAluno(id_aluno, nome=None, body_id=None):
    aluno_encontrado = None
    for aluno in dici['alunos']:
        if aluno["id"] == id_aluno:
            aluno_encontrado = aluno
            break

    if aluno_encontrado is None:
        raise AlunoNaoEncontrado("Aluno não encontrado")

    if nome is None:
        if body_id is None or body_id == id_aluno:
            return 'erro: aluno sem nome', None

    if nome is not None and not isinstance(nome, str):
        return 'erro: O nome deve ser uma string', None

    if body_id is not None and not isinstance(body_id, int):
        return 'erro: O id deve ser um número inteiro', None

    if body_id is not None and body_id != id_aluno:
        for aluno in dici['alunos']:
            if aluno['id'] == body_id:
                return 'erro: ID de aluno já existe', None

    if nome is not None:
        aluno_encontrado['nome'] = nome
    if body_id is not None:
        aluno_encontrado['id'] = body_id

    return "mensagem: aluno atualizado com sucesso", aluno_encontrado
    
def atualizarParcialAluno(id_aluno,dados):
    aluno_encontrado = False
    for aluno in dici['alunos']:
        if aluno["id"] == id_aluno:
            
            for chave, valor in dados.items():
                if chave in aluno: 
                    aluno[chave] = valor
            aluno_encontrado = True
            return "mensagem: Aluno atualizado com sucesso", aluno

    if not aluno_encontrado:
        return "erro: Aluno não encontrado"
    
def deleteAluno(id_aluno):
    for aluno in dici["alunos"]:
        if aluno["id"] == id_aluno:
            dici["alunos"].remove(aluno)
            return 'mensagem: Aluno deletado com sucesso', aluno
    
    raise AlunoNaoEncontrado("Aluno não encontrado")
    
