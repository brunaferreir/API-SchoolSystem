#CRUD

# Professores;
# get - todos os professores
# get id  - um professor

# post - criar novo professor

# delete - todos os professores
# delete id -um professor

# put - atualizar professor
# path - 

#-----------------------------------------------------------

# Alunos;
# get - todoos os alunos
# get id  - um aluno

# post - criar novo aluno

# delete - todos os alunos
# delete id -um aluno

# put - atualizar aluno
# path - 

#-----------------------------------------------------------

# Turmas
# get - todas as turmas
# get id  - uma turma

# post - criar nova turma

# delete - todos as turmas
# delete id - uma turma

# put - atualizar turma
# path - 

from flask import Flask, jsonify, request

class AlunoNaoEncontrado(Exception):
    pass

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

def aluno_por_id(id_aluno):
    for aluno in dici['alunos']:
        if aluno['id'] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado

app = Flask(__name__)

#ALUNOS

#GET

@app.route('/alunos', methods=['GET'])
def get_alunos():
    dados = dici['alunos']
    return jsonify(dados)

#GET ID

@app.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return jsonify(aluno), 200  
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'aluno nao encontrado'}), 404


#POST

@app.route('/alunos', methods=['POST'])
def create_aluno():
    dados = request.json
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400

    id_aluno = dados.get('id')
    nome_aluno = dados.get('nome')

    # Validação da presença do nome DEVE vir primeiro
    if not nome_aluno:
        return jsonify({'erro': 'aluno sem nome'}), 400

    # Validação de tipos
    if not isinstance(id_aluno, int):
        return jsonify({'erro': 'O id deve ser um número inteiro'}), 400
    if not isinstance(nome_aluno, str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400

    # Verifica se o ID já existe
    for aluno in dici['alunos']:
        if aluno['id'] == id_aluno:
            return jsonify({'erro': 'id ja utilizada'}), 400

    # Adiciona o novo aluno
    dici['alunos'].append(dados)
    return jsonify(dados), 201




#RESET 

@app.route('/reseta', methods=['POST'])
def reseta():
    dici["alunos"] = []
    dici["professores"] = []
    dici["turmas"] = []
    return jsonify({"message": "Banco de dados resetado"}), 200





#PUT ID

def aluno_por_id(id_aluno):
    for aluno in dici['alunos']:
        if aluno['id'] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado


@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    dados = request.json
    if not dados:
        return jsonify({'erro': 'Dados inválidos'}), 400

    nome_aluno = dados.get('nome')
    id_novo = dados.get('id')

    if not nome_aluno:
        return jsonify({'erro': 'aluno sem nome'}), 400

    # Validação de tipos
    if id_novo is not None and not isinstance(id_novo, int):
        return jsonify({'erro': 'O id deve ser um número inteiro'}), 400
    if not isinstance(nome_aluno, str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400
    

    # Verifica se o novo ID já existe para outro aluno
    if id_novo is not None and id_novo != id_aluno:
        for aluno in dici['alunos']:
            if aluno['id'] == id_novo:
                return jsonify({'erro': 'ID de aluno já existe'}), 400


    try:
        aluno = aluno_por_id(id_aluno)
        # Atualiza apenas se as chaves existirem nos dados recebidos
        if 'nome' in dados:
            aluno['nome'] = nome_aluno
        if 'id' in dados:
            aluno['id'] = id_novo
        return jsonify(aluno), 200
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'aluno nao encontrado'}), 404




#PATCH ID

@app.route('/alunos/<int:id_aluno>', methods=['PATCH'])
def patch_aluno(id_aluno):
    dados = request.json
    try:
        aluno = aluno_por_id(id_aluno)
        for chave, valor in dados.items():
            aluno[chave] = valor
        return jsonify(aluno), 200
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404



#DELETE ID

@app.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        dici['alunos'].remove(aluno)
        return 'aluno deletado', 204
    except AlunoNaoEncontrado:
         return jsonify({'erro': 'aluno nao encontrado'}), 404

#DELETE TUDO   

@app.route('/alunos', methods=['DELETE'])
def delete_alunos():
    dici['alunos'] = []
    return 'alunos deletados', 204










#-------------------------PROFESSORES-----0.2---------------------------------------------


class ProfessorNaoEncontrado(Exception):
    pass


def professor_por_id(professor_id):
    for professor in dici['professores']:
        if professor['id'] == professor_id:
            return professor
    raise ProfessorNaoEncontrado


#GET

# @app.route('/professores', methods=['GET'])
# def get_professores():
#     dados = dici['professores']
#     return jsonify(dados)


@app.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(dici["professores"])



# #GET ID

@app.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        
        professor = professor_por_id(id_professor)
        return jsonify(professor), 200  
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'professor nao encontrado'}), 400


# #POST

# @app.route('/professores', methods=['POST'])
# def create_professores(): 
#       dados = request.json
#       dici['professores'].append(dados)
#       return jsonify(dados), 200


@app.route('/professores', methods=['POST'])
def create_professores():
    dados = request.json
    id_professor = dados.get('id')
    nome_professor = dados.get('nome')

    if not nome_professor:
        return jsonify({'erro': 'professor sem nome'}), 400
    
     # Validação de tipos (exemplo)
    if 'nome' in dados and not isinstance(dados['nome'], str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400
    
    if 'idade' in dados and not isinstance(dados['idade'], int):
        return jsonify({'erro': 'A idade deve ser um número inteiro'}), 400
    
    if 'materia' in dados and not isinstance(dados['materia'], str):
        return jsonify({'erro': 'A matéria deve ser uma string'}), 400
    
    if 'observacao' in dados and not isinstance(dados['observacao'], str):
        return jsonify({'erro': 'A observação deve ser uma string'}), 400


    # Verifica se o ID já existe
    for professor in dici['professores']:
        if professor['id'] == id_professor:
            return jsonify({'erro': 'id ja utilizada'}), 400

    dici['professores'].append(dados)
    return jsonify(dados), 200 # Use 201 Created para indicar que um novo recurso foi criado

 

# #PUT ID

# @app.route('/professores/<int:id_professor>', methods=['PUT'])
# def update_professor(id_professor):
#     dados = request.json
#     nome_professor = dados.get('nome')
   
#     if not nome_professor:
#         return jsonify({'erro': 'professor sem nome'}), 400 

#     try:
#         professor = professor_por_id(id_professor)
#         professor.update(dados)  
#         return jsonify(professor), 200   
#     except ProfessorNaoEncontrado:
#          return jsonify({'erro': 'professor nao encontrado'}), 400
     


@app.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    dados = request.json
    nome_professor = dados.get('nome')

    if not nome_professor:
        return jsonify({'erro': 'professor sem nome'}), 400

    # Validação de tipos (exemplo)
    if 'nome' in dados and not isinstance(dados['nome'], str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400
    
    if 'idade' in dados and not isinstance(dados['idade'], int):
        return jsonify({'erro': 'A idade deve ser um número inteiro'}), 400
    
    if 'materia' in dados and not isinstance(dados['materia'], str):
        return jsonify({'erro': 'A matéria deve ser uma string'}), 400
    
    if 'observacao' in dados and not isinstance(dados['observacao'], str):
        return jsonify({'erro': 'A observação deve ser uma string'}), 400

    try:
        professor = professor_por_id(id_professor)
        professor.update(dados)
        return jsonify(professor), 200
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'professor nao encontrado'}), 400




# #PATCH ID

@app.route('/professores/<int:id_professor>', methods=['PATCH'])
def patch_professor(id_professor):
    dados = request.json
    try:
        professor = professor_por_id(id_professor)
        for chave, valor in dados.items():
            professor[chave] = valor
        return jsonify(professor), 200
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 400



# #DELETE ID

@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_profesor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        dici['professores'].remove(professor)
        return 'professor deletado', 204
    except ProfessorNaoEncontrado:
         return jsonify({'erro': 'professor nao encontrado'}), 400


# #DELETE TUDO   

@app.route('/professores', methods=['DELETE'])
def delete_professores():
    dici['professores'] = []
    return 'professores deletados', 204







#----------------------------TURMAS-----------------------------------------



# CRUD TURMAS

# LISTAR TODAS AS TURMAS
@app.route('/turmas', methods=['GET'])
def getTurma():
    dados = dici["turmas"]
    return jsonify(dados)


# LISTAR TURMA POR ID
@app.route('/turmas/<int:idTurma>', methods=['GET'])
def getTurmaById(idTurma):
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            return jsonify(turma), 200
    return jsonify({"erro": "Turma não encontrada"}), 404


# CRIAR TURMA 
@app.route('/turmas', methods=['POST'])
def createTurma():
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json

    # verifica se todos os parâmetros obrigatórios estão presentes
    if 'id' not in dados or 'professor' not in dados:
        return jsonify({'erro': 'Parâmetro obrigatório ausente'}), 400
        
    if not isinstance(dados['id'], int) or dados['id'] <= 0:
        return jsonify({'erro': 'O id deve ser um número inteiro positivo'}), 400

    if not isinstance(dados['nome'], str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400

    if not isinstance(dados['professor'], str):
        return jsonify({'erro': 'O professor deve ser uma string'}), 400

    #verifica a id
    for turma in dici["turmas"]:
        if turma['id'] == dados['id']:
            return jsonify({'erro': 'id ja utilizada'}), 400
        
    dici['turmas'].append(dados)
    return jsonify(dados,{'mensagem': 'Turma criada com sucesso'}), 200


# DELETAR TURMA POR ID 
@app.route('/turmas/<int:idTurma>', methods=['DELETE'])
def deleteTurma(idTurma):
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            dici["turmas"].remove(turma)  
            return jsonify({"mensagem": "Turma deletada com sucesso", "turmas": turma}), 200
    
    # Se não encontrar, retorna erro 404
    return jsonify({"erro": "Turma não encontrada"}), 404


# ATUALIZAR TURMA POR ID
@app.route('/turmas/<int:idTurma>', methods=['PUT'])
def atualizarTurma(idTurma):
    dados = request.json
    print(f"Dados recebidos: {dados}")

    turma_encontrada = None
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            turma_encontrada = turma
            print(f"Turma encontrada: {turma}")
            break

    if turma_encontrada is None:
        return jsonify({"erro": "Turma não encontrada"}), 404

    if not all(k in dados for k in ["id", "nome", "professor"]):
        return jsonify({'erro': 'Campos id, nome e professor são obrigatórios'}), 400

    if not isinstance(dados["id"], int) or not isinstance(dados["nome"], str) or not isinstance(dados["professor"], str):
        return jsonify({'erro': 'Tipos de dados inválidos'}), 400

    if 'nome' in dados:
        turma_encontrada['nome'] = dados['nome']

    print(f"Turma atualizada: {turma_encontrada}")
    return jsonify({"mensagem": "Turma atualizada com sucesso", "turma": turma_encontrada}), 200


@app.route('/turmas/<int:idTurma>', methods=['PATCH'])
def atualizarParcialTurma(idTurma):
    dados = request.json

    turma_encontrada = False
    for turma in dici["turmas"]:
        if turma["id"] == idTurma:
            for chave, valor in dados.items():
                turma[chave] = valor
            turma_encontrada = True
            return jsonify({"mensagem": "Turma atualizada com sucesso", "turma": turma}), 200

    if not turma_encontrada:
        return jsonify({"erro": "Turma não encontrada"}), 404






if __name__ == '__main__':
    app.run(debug=True)






