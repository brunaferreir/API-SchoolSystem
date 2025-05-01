from flask_restx import Api

api = Api(
    version="1.0",
    title="API de Gestão Escolar",
    description=(
        "Documentação da API para Alunos, Professores e Turmas.\n\n"
        "Esta API RESTful facilita a gestão escolar, administrando alunos, professores e turmas. "
        "A  API segue os princípios do REST, utilizando JSON e códigos de status HTTP.\n\n"
        "**Funcionalidades Principais**\n\n"
        "A API possui três recursos principais:\n\n"
        "1.  **Aluno:** CRUD (Create, Read, Update, Delete) de registros de alunos.\n"
        "2.  **Professor:** CRUD (Create, Read, Update, Delete) de registros de professores.\n"
        "3.  **Turma:** CRUD (Create, Read, Update, Delete) de turmas, com associação de alunos e professores."
    )
    ,
    doc="/docs",
    mask_swagger=False,  # Desativa o X-Fields no Swagger,
    prefix="/api"
)