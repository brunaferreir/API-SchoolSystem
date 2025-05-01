from . import api
from swagger.namespace.alunonamespace import alunos_ns
from swagger.namespace.profnamespace import prof_ns
from swagger.namespace.turmanamespace import turma_ns

# Função para registrar os namespaces
def configure_swagger(app):
    api.init_app(app)
    api.add_namespace(alunos_ns, path="/alunos")
    api.add_namespace(prof_ns, path="/professores")
    api.add_namespace(turma_ns, path="/turmas")
    api.mask_swagger = False