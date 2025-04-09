from flask import Blueprint, request, jsonify
from aluno.modelAluno import AlunoNaoEncontrado, aluno_por_id, get_alunos, create_aluno, apaga_tudo, atualizarAluno, atualizarParcialAluno, deleteAluno,dici

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = get_alunos()
    return jsonify(alunos), 200

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def aluno_por_id_rota(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return jsonify(aluno), 200
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

@alunos_blueprint.route('/alunos', methods=['POST'])
def criar_aluno():
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json
    if 'id' not in dados or 'nome' not in dados:
        return jsonify({'erro': 'aluno sem nome'}), 400

    resposta = create_aluno(dados.get('id'), dados.get('nome'))
    if "erro" in resposta:
        return jsonify(resposta), 400

    dici['alunos'].append(resposta)
    return jsonify(resposta, {'mensagem': 'Aluno criado com sucesso'}), 200



@alunos_blueprint.route('/reseta1', methods=['POST'])
def reseta():
    resposta = apaga_tudo()
    return jsonify(resposta), 200



@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json
    nome = dados.get('nome')
    body_id = dados.get('id')

    if body_id is not None and not isinstance(body_id, int):
        return jsonify({'erro': 'O id deve ser um número inteiro'}), 400

    if 'nome' in dados and not isinstance(nome, str):
        return jsonify({'erro': 'O nome deve ser uma string'}), 400

    if 'nome' not in dados:
        return jsonify({'erro': 'aluno sem nome'}), 400

    try:
        resposta, aluno_atualizado = atualizarAluno(id_aluno, nome, body_id)
        if "erro" in resposta:
            erro_mensagem = resposta.split(': ')[1] if ': ' in resposta else resposta
            return jsonify({'erro': erro_mensagem}), 400
        elif not aluno_atualizado:
            return '', 204
        return jsonify({"mensagem": resposta, "aluno": aluno_atualizado}), 200

    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PATCH'])
def atualizar_parcial_aluno(id_aluno):
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json 

    try:
       
        resposta, aluno_atualizado = atualizarParcialAluno(id_aluno, dados)
        return jsonify({"mensagem": resposta, "aluno": aluno_atualizado}), 200
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def deletar_aluno(id_aluno):
    try:
        resposta, aluno_deletado = deleteAluno(id_aluno)
        return jsonify({"mensagem": resposta}), 204
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404