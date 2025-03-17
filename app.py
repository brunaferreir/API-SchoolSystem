from flask import Flask, jsonify, request
import dici

app = Flask(__name__)

# ------- TURMA -------

# RESET

@app.route('/reseta', methods=['POST'])
def reseta():
    dici.dici["turmas"] = []
    return jsonify({"message": "Banco de dados resetado"}), 200


# CRUD TURMAS

# LISTAR TODAS AS TURMAS
@app.route('/turmas', methods=['GET'])
def getTurma():
    dados = dici.dici["turmas"]
    return jsonify(dados)


# LISTAR TURMA POR ID
@app.route('/turmas/<int:idTurma>', methods=['GET'])
def getTurmaById(idTurma):
    for turma in dici.dici["turmas"]:
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
    for turma in dici.dici["turmas"]:
        if turma['id'] == dados['id']:
            return jsonify({'erro': 'id ja utilizada'}), 400
        
    dici.dici['turmas'].append(dados)
    return jsonify(dados,{'mensagem': 'Turma criada com sucesso'}), 200


# DELETAR TURMA POR ID 
@app.route('/turmas/<int:idTurma>', methods=['DELETE'])
def deleteTurma(idTurma):
    for turma in dici.dici["turmas"]:
        if turma["id"] == idTurma:
            dici.dici["turmas"].remove(turma)  
            return jsonify({"mensagem": "Turma deletada com sucesso", "turmas": turma}), 200
    
    # Se não encontrar, retorna erro 404
    return jsonify({"erro": "Turma não encontrada"}), 404


# ATUALIZAR TURMA POR ID
@app.route('/turmas/<int:idTurma>', methods=['PUT', 'PATCH'])
def atualizarTurma(idTurma):
    dados = request.json

    # Verificação do tipo dos dados antes de atualizar
    if "id" in dados and not isinstance(dados['id'], int) or dados['id'] <= 0:
        return jsonify({'erro': 'O id deve ser um número inteiro'}), 400

    if "nome" in dados and not isinstance(dados["nome"], str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400

    if "professor" in dados and not isinstance(dados["professor"], str):
        return jsonify({'erro': 'O professor deve ser uma string'}), 400

    # Procura a turma pelo ID
    for turma in dici.dici["turmas"]:
        if turma["id"] == idTurma:
            # Atualiza apenas os campos fornecidos
            if "nome" in dados:
                turma["nome"] = dados["nome"]
            
            if "professor" in dados:
                turma["professor"] = dados["professor"]

            return jsonify({"mensagem": "Turma atualizada com sucesso", "turma": turma}), 200

    return jsonify({"erro": "Turma não encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True)
