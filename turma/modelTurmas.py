dici = {
     "turmas" : [
        {'nome':'si','id':1, 'professor':"caio"},
        {'nome':'ads','id':28, 'professor':'caio'}
    ]    
}


class TurmaNaoEncontrada(Exception):
    pass


def turma_por_id(idTurma):
    for turma in dici['turmas']:
        if turma['id'] == idTurma:
            return turma
    raise TurmaNaoEncontrada

def getTurma():
    return dici["turmas"]

def apaga_tudo():
    dici['turmas'] = []
    return "message: Banco de dados resetado"

def createTurma(id, nome, professor):
    if not id or not nome or not professor:
        return {'erro': 'Parâmetro obrigatório ausente'}

    if not isinstance(id, int) or id <= 0:
        return {'erro': 'O id deve ser um número inteiro positivo'}

    if not isinstance(nome, str):
        return {'erro': 'O nome deve ser uma string'}

    if not isinstance(professor, str):
        return {'erro': 'O professor deve ser uma string'}

    for turma in dici["turmas"]:
        if turma['id'] == id:
            return {'erro': 'id ja utilizada'}

    return {'id': id, 'nome': nome, 'professor': professor}


def deleteTurma(idTurma):
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            dici["turmas"].remove(turma)
            return 'mensagem: Turma deletada com sucesso', turma
    
    raise TurmaNaoEncontrada("Turma não encontrada")


def atualizarTurma(idTurma, nome=None, professor=None):
    turma_encontrada = None
    for turma in dici['turmas']:
        if turma["id"] == idTurma:
            turma_encontrada = turma
            print(f"Turma encontrada: {turma}")
            break

    if turma_encontrada is None:
        raise TurmaNaoEncontrada("Turma não encontrada")

    if nome is None and professor is None:
        return 'erro: Pelo menos um dos campos "nome" ou "professor" deve ser fornecido', None

    if nome and not isinstance(nome, str):
        return 'erro: O nome deve ser uma string', None
    if professor and not isinstance(professor, str):
        return 'erro: O professor deve ser uma string', None

    if nome:
        turma_encontrada['nome'] = nome
    if professor:
        turma_encontrada['professor'] = professor

    print(f"Estado do banco de dados após a atualização: {dici['turmas']}")

    return "mensagem: Turma atualizada com sucesso", turma_encontrada


def atualizarParcialTurma(idTurma,dados):
    turma_encontrada = False
    for turma in dici['turmas']:
        if turma["id"] == idTurma:
            
            for chave, valor in dados.items():
                if chave in turma: 
                    turma[chave] = valor
            turma_encontrada = True
            return "mensagem: Turma atualizada com sucesso", turma

    if not turma_encontrada:
        return "erro: Turma não encontrada"

# print(turma_por_id(28))
# print(getTurma())
# print(createTurma(2,'ads','caio'))
# print(deleteTurma(1))
# print(atualizarTurma(28, nome='bd', professor=None))
# print(atualizarParcialTurma(2,{'professor':'luana'}))
