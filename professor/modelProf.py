dici = {
        "professores":[
        {"id":1,"nome":"carlos", "idade":30, "materia":"matematica", "observacao":"bom professor"}
        ,{"id":2,"nome":"lucas", "idade":34, "materia":"POO", "observacao":"bom professor"} 
        ]
}

class ProfessorNaoEncontrado(Exception):
    pass


def professor_por_id(professor_id):
    for professor in dici['professores']:
        if professor['id'] == professor_id:
            return professor
    raise ProfessorNaoEncontrado

def apaga_tudo():
    dici['professores'] = []
    return "message: Banco de dados resetado"

