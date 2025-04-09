dici = {
        "professores" : [
        {"id":1,"nome":"carlos", "idade":30, "materia":"matematica", "observacao":"bom professor"}
        ,{"id":2,"nome":"lucas", "idade":34, "materia":"POO", "observacao":"bom professor"} 
        ]
}

class ProfessorNaoEncontrado(Exception):
    pass


def professor_por_id(id_professor):  
    for professor in dici['professores']:
        if professor['id'] == id_professor:
            return professor
    raise ProfessorNaoEncontrado


def get_professores():
    return dici["professores"]

def apaga_tudo():
    dici['professores'] = []
    return "message: Banco de dados resetado"


def create_professores(id, nome, idade, materia, observacao):
    if not id or not nome or not idade or not materia or not observacao:
        return {'erro': 'Parâmetro obrigatório ausente'}

    if not isinstance(id, int) or id <= 0:
        return {'erro': 'O id deve ser um número inteiro positivo'}

    if not isinstance(nome, str):
        return {'erro': 'O nome deve ser uma string'}

    if not isinstance(idade, int):
        return {'erro': 'A idade deve ser um número inteiro'}

    if not isinstance(materia, str):
        return {'erro': 'A matéria deve ser uma string'}

    if not isinstance(observacao, str):
        return {'erro': 'A observação deve ser uma string'}

    for professor in dici["professores"]:
        if professor['id'] == id:
            return {'erro': 'id ja utilizada'}

    return {'id': id,'nome': nome,'idade': idade,'materia': materia,'observacao': observacao}


def atualizarProfessor(id_professor, nome=None, idade=None, materia=None, observacao=None, body_id=None):  
        professor_encontrado = None
        for professor in dici['professores']:
            if professor["id"] == id_professor:
                professor_encontrado = professor
                break

        if professor_encontrado is None:
            raise ProfessorNaoEncontrado("Professor não encontrado")

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

        if nome is not None:
            professor_encontrado['nome'] = nome
        if idade is not None:
            professor_encontrado['idade'] = idade
        if materia is not None:
            professor_encontrado['materia'] = materia
        if observacao is not None:
            professor_encontrado['observacao'] = observacao
        if body_id is not None:
           professor_encontrado['id'] = body_id    
     
        return "mensagem: Professor atualizado com sucesso", professor_encontrado


def atualizarParcialProfessor(id_professor, dados):
        professor_encontrado = False
        for professor in dici['professores']:
            if professor["id"] == id_professor:
                
                for chave, valor in dados.items():
                    if chave in professor: 
                        professor[chave] = valor
                professor_encontrado = True
                return "mensagem: Professor atualizada com sucesso", professor

        if not professor_encontrado:
            return "erro: Professor não encontrado"


def deleteProfessor(id_professor):
    for professor in dici["professores"]:
        if professor["id"] == id_professor:
            dici["professores"].remove(professor)
            return 'mensagem: Turma deletada com sucesso', professor
    
    raise ProfessorNaoEncontrado("Professor não encontrado")

#print(professor_por_id(1))
#print(get_professores())
#print(create_professores(dici, 3,'lucas', 34, 'POO', 'bom professor'))
#print("-------------------------------")
#print(delete_profesor(1))
#print(apaga_tudo())
#print(get_professores())
#print(update_professor(3, {'nome': 'caio', 'idade': 50, 'materia': 'portugues', 'observacao': 'otimo professor'}))
#print(patch_professor(2,{'nome':'lua'}))

