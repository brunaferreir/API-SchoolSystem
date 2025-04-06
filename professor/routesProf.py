from flask import Blueprint, request, jsonify
from professor.modelProf import ProfessorNaoEncontrado, apaga_tudo, professor_por_id

professores_blueprint = Blueprint('professores', __name__)


@professores_blueprint.route('/reseta', methods=['POST'])
def reseta():
    resposta = apaga_tudo()
    return jsonify(resposta), 200

@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        
        professor = professor_por_id(id_professor)
        return jsonify(professor), 200  
    except ProfessorNaoEncontrado:
        return jsonify({'erro': 'professor nao encontrado'}), 400