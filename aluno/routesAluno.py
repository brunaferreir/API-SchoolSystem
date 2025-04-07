from flask import Blueprint, request, jsonify
from aluno.modelAluno import AlunoNaoEncontrado

alunos_blueprint = Blueprint('alunos', __name__)