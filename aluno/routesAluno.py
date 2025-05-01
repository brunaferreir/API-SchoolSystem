from flask import Blueprint, request, jsonify ,render_template,redirect, url_for
from datetime import datetime
from aluno.modelAluno import AlunoNaoEncontrado, aluno_por_id, get_alunos, create_aluno, apaga_tudo, atualizarAluno, atualizarParcialAluno, deleteAluno
from config import db

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

    dados = request.get_json()

    novo_aluno, erro = create_aluno(dados)
    if erro:
        status_code = 400 if erro != "Turma não existe" else 404
        return jsonify({'erro': erro}), status_code
    
    aluno_dict = novo_aluno.to_dict()
    
    return jsonify({
        'aluno': aluno_dict,
        'mensagem': 'Aluno criado com sucesso'
    }), 201
    


@alunos_blueprint.route('/reseta1', methods=['POST'])
def reseta():
    resposta = apaga_tudo()
    return jsonify(resposta), 200


@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno_rota(id_aluno):
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.get_json()

    if not dados:
        return jsonify({'erro': 'Nenhum dado para atualizar fornecido'}), 400
    
    mensagem, aluno_atualizado = atualizarAluno(id_aluno, dados)

    if "erro" in mensagem:
        status_code = 404 if "Aluno não encontrado" in mensagem else 400
        return jsonify({'erro': mensagem}), status_code

    return jsonify({"mensagem": mensagem, "aluno": aluno_atualizado}), 200


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