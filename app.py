from flask import Flask, jsonify, request

app = Flask(__name__)

dici = {
    "alunos" : [
        {"id": 1, "nome": "bruna"}
        ],
    "professores" : [
        {'id': 1, 'nome':'caio'}
    ],
    "turmas" : [
        {'nome':'si','id':1, 'professor':"caio"},
        {'nome':'ads','id':28, 'professor':'caio'}
    ]
}

# ------- TURMA -------

# RESET

@app.route('/reseta', methods=['POST'])
def reseta():
    dici["turmas"] = []
    return jsonify({"message": "Banco de dados resetado"}), 200


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
