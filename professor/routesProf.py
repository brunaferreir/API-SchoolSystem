from flask import Blueprint, request, jsonify
from professor.modelProf import ProfessorNaoEncontrado, professor_por_id, get_professores , apaga_tudo, create_professores, deleteProfessor, atualizarProfessor, atualizarParcialProfessor, dici

professores_blueprint = Blueprint('professores', __name__)


@professores_blueprint.route('/professores', methods=['GET'])
def listar_pofessores():
    professores = get_professores()
    return jsonify(professores), 200

@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def professor_por_id_rota(id_professor):
    try:

        professor = professor_por_id(id_professor)
        print(f"Rota GET professor: {professor}") #Debug
        return jsonify(professor), 200
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'professor nao encontrado'}), 400

# @professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
# def professor_por_id_rota(id_professor):
#     try:
#         professor = professor_por_id(id_professor)
#         return jsonify(professor), 200  
#     except ProfessorNaoEncontrado:
#         return jsonify({'erro': 'professor nao encontrado'}), 400
    

@professores_blueprint.route('/professores', methods=['POST'])
def criar_professor():
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json
    if 'id' not in dados or 'nome' not in dados or 'idade' not in dados or 'materia' not in dados or 'observacao' not in dados:
        return jsonify({'erro': 'Parâmetro obrigatório ausente'}), 400

    resposta = create_professores(dados.get('id'), dados.get('nome'), dados.get('idade'), dados.get('materia'), dados.get('observacao'))
    if "erro" in resposta:
        return jsonify(resposta), 400

    dici['professores'].append(resposta) 
    return jsonify(resposta, {'mensagem': 'Professor criado com sucesso'}), 200



@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT'])
def atualizarProfessor(id_professor):
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json

    if (not isinstance(dados.get('nome'), str) and dados.get('nome') is not None) or \
       (not isinstance(dados.get('idade'), int) and dados.get('idade') is not None) or \
       (not isinstance(dados.get('materia'), str) and dados.get('materia') is not None) or \
       (not isinstance(dados.get('observacao'), str) and dados.get('observacao') is not None):
        return jsonify({'erro': 'Tipos de dados inválidos'}), 400

    try:
        resposta, professor_atualizado = atualizarProfessor(id_professor, dados.get('nome'), dados.get('idade'), dados.get('materia'), dados.get('observacao'))
        if not professor_atualizado:
            return '', 204

        return jsonify({"mensagem": resposta, "professor": professor_atualizado}), 200

    except ProfessorNaoEncontrado as e:
        print(f"ProfessorNaoEncontrado: {e}") #Debug
        return jsonify({'erro': 'Professor não encontrado'}), 404
    except Exception as e:
        print(f"Erro inesperado: {e}") #Debug
        return jsonify({'erro': 'Erro interno do servidor'}), 500



# #DELETE ID

@professores_blueprint.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_profesor(id_professor):
    try:
        resposta, professor_deletado = deleteProfessor(id_professor)
        return jsonify({"mensagem": resposta})
    except ProfessorNaoEncontrado:
         return jsonify({'erro': 'professor nao encontrado'}), 400

# #PATCH ID

@professores_blueprint.route('/professores/<int:id_professor>', methods=['PATCH'])
def atualizar_parcial_professor(id_professor):
    if not request.is_json:
        return jsonify({'erro': 'JSON inválido ou não fornecido'}), 400

    dados = request.json 

    try:
        resposta, professor_atualizado = atualizarParcialProfessor(id_professor, dados)
        return jsonify({"mensagem": resposta, "professor": professor_atualizado}), 200
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404



@professores_blueprint.route('/reseta1', methods=['POST'])
def reseta():
    resposta = apaga_tudo()
    return jsonify(resposta), 200

