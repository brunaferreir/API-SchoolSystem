from flask import Blueprint, request, jsonify
from Turma.modelTurmas import TurmaNaoEncontrada,turma_por_id, getTurma, apaga_tudo, createTurma, deleteTurma, atualizarTurma, atualizarParcialTurma, dici

turmas_blueprint = Blueprint('turmas', __name__)


@turmas_blueprint.route('/turmas', methods=['GET'])
def listar_turmas():
    turmas = getTurma()
    return jsonify(turmas), 200


@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['GET'])
def turma_por_id_rota(idTurma):
    try:
        turma = turma_por_id(idTurma)
        return jsonify(turma), 200
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404


@turmas_blueprint.route('/turmas', methods=['POST'])
def criar_turma():
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json
    if 'id' not in dados or 'nome' not in dados or 'professor' not in dados:
        return jsonify({'erro': 'Parâmetro obrigatório ausente'}), 400

    resposta = createTurma(dados.get('id'), dados.get('nome'), dados.get('professor'))
    if "erro" in resposta:
        return jsonify(resposta), 400

    dici['turmas'].append(resposta)
    return jsonify(resposta, {'mensagem': 'Turma criada com sucesso'}), 200


@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['PUT'])
def atualizar_turma(idTurma):
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json

    if (not isinstance(dados.get('nome'), str) and dados.get('nome') is not None) or \
       (not isinstance(dados.get('professor'), str) and dados.get('professor') is not None):
        return jsonify({'erro': 'Tipos de dados inválidos'}), 400

    try:
        resposta, turma_atualizada = atualizarTurma(idTurma, dados.get('nome'), dados.get('professor'))
        if not turma_atualizada:
            return '', 204
        
        return jsonify({"mensagem": resposta, "turma": turma_atualizada}), 200

    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['DELETE'])
def deletar_turma(idTurma):
    try:
        resposta, turma_deletada = deleteTurma(idTurma)
        return jsonify({"mensagem": resposta}), 204
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'Turma não encontrada'}), 404




@turmas_blueprint.route('/turmas/<int:idTurma>', methods=['PATCH'])
def atualizar_parcial_turma(idTurma):
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json 

    try:
       
        resposta, turma_atualizada = atualizarParcialTurma(idTurma, dados)
        return jsonify({"mensagem": resposta, "turma": turma_atualizada}), 200
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404


@turmas_blueprint.route('/reseta', methods=['POST'])
def reseta():
    resposta = apaga_tudo()
    return jsonify(resposta), 200



