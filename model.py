dici = {
    "alunos":[
        {"id":1,"nome":"Joao"}
       ,{"id":2,"nome":"Maria"}
       ,{"id":3,"nome":"Pedro"} 
],
    "professores":[
        {"id":1,"nome":"carlos", "idade":30, "materia":"matematica", "observacao":"bom professor"}
        ,{"id":2,"nome":"lucas", "idade":34, "materia":"POO", "observacao":"bom professor"} 
        ],
     "turmas" : [
        {'nome':'si','id':1, 'professor':"caio"},
        {'nome':'ads','id':28, 'professor':'caio'}
    ]    

}

class AlunoNaoEncontrado(Exception):
    pass


def aluno_por_id(id_aluno):
    for aluno in dici['alunos']:
        if aluno['id'] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado




class ProfessorNaoEncontrado(Exception):
    pass


def professor_por_id(professor_id):
    for professor in dici['professores']:
        if professor['id'] == professor_id:
            return professor
    raise ProfessorNaoEncontrado
