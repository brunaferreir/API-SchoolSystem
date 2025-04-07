dici = {
    "alunos":[
        {"id":1,"nome":"Joao"}
       ,{"id":2,"nome":"Maria"}
       ,{"id":3,"nome":"Pedro"}
    ] 
}

class AlunoNaoEncontrado(Exception):
    pass


def aluno_por_id(id_aluno):
    for aluno in dici['alunos']:
        if aluno['id'] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado