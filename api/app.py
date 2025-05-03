from swagger.swagger_config import configure_swagger
import pytest
import os
import sys
from config import app, db
from aluno.routesAluno import alunos_blueprint
from turma.routesTurma import turmas_blueprint
from professor.routesProf import professores_blueprint

app.register_blueprint(alunos_blueprint, url_prefix='/api')
app.register_blueprint(turmas_blueprint, url_prefix='/api')
app.register_blueprint(professores_blueprint, url_prefix='/api')

configure_swagger(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])