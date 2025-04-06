import os
from config import app
from turma.routesTurma import turmas_blueprint
from aluno.routesAluno import alunos_blueprint
from professor.routesProf import professores_blueprint


app.register_blueprint(turmas_blueprint)
app.register_blueprint(alunos_blueprint)
app.register_blueprint(professores_blueprint)


if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )