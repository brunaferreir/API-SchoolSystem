# API de Gestão Escolar

## Descrição

Esta é uma API RESTful construída com Flask e Flask-RESTx para gerenciar os dados de uma instituição de ensino. Ela permite a administração de alunos, professores e turmas, incluindo a criação, leitura, atualização e exclusão de registros. A API segue os princípios do REST, utilizando JSON para a troca de dados e códigos de status HTTP para indicar o resultado das operações. A documentação da API é gerada automaticamente com o Swagger, facilitando o uso por outros desenvolvedores.

## Funcionalidades

A API oferece as seguintes funcionalidades:

* **Alunos:**
    * Criação, leitura, atualização e exclusão de alunos.
    * Recuperação de um único aluno por ID.
    * Recuperação de todos os alunos.
* **Professores:**
    * Criação, leitura, atualização e exclusão de professores.
    * Recuperação de um único professor por ID.
    * Recuperação de todos os professores.
* **Turmas:**
    * Criação, leitura, atualização e exclusão de turmas.
    * Recuperação de uma única turma por ID.
    * Recuperação de todas as turmas.
    * Associação de alunos a turmas.
    * Associação de professores a turmas.
* **Documentação:**
    * Documentação interativa da API gerada com Swagger, acessível através do endpoint `/api/docs`.

## Tecnologias Utilizadas

* Python
* Flask
* Flask-RESTx
* SQLAlchemy (ORM)
* Swagger

## Pré-requisitos

* Python 3.x
* pip (gerenciador de pacotes do Python)
* Um banco de dados compatível com SQLAlchemy (SQLite, MySQL, PostgreSQL, etc.)

## Instalação

1.  **Clone o repositório:**

    ```bash
    git clone <URL do repositório>
    cd <nome do repositório>
    ```

2.  **Crie um ambiente virtual (recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate  # No Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o banco de dados:**

    * Crie um arquivo de configuração (por exemplo, `config.py`) com as configurações do seu banco de dados. Exemplo para SQLite:

        ```python
        class Config:
            DEBUG = True
            SQLALCHEMY_DATABASE_URI = 'sqlite:///escola.db'  # Ou outro URI de banco de dados
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            HOST = '0.0.0.0'
            PORT = 5000
        ```

    * Se você estiver usando um banco de dados diferente, ajuste a string de conexão (`SQLALCHEMY_DATABASE_URI`) de acordo.

5.  **Configure as variáveis de ambiente:**

    * Defina a variável `FLASK_APP` para o nome do seu arquivo principal (geralmente `app.py` ou `__init__.py`).

    * Exemplo no Linux/macOS:

        ```bash
        export FLASK_APP=app.py
        ```

    * Exemplo no Windows:

        ```bash
        set FLASK_APP=app.py
        ```

## Execução

1.  **Inicialize o banco de dados:**

    ```bash
    flask shell
    >>> db.create_all()
    ```

2.  **Execute a aplicação:**

    ```bash
    flask run
    ```

    Ou, se você estiver usando o arquivo principal para executar a aplicação:

    ```bash
    python app.py
    ```

3.  **Acesse a documentação:**

    * A API estará disponível em `http://0.0.0.0:5000/api/` (ou na porta e host configurados).
    * A documentação do Swagger estará disponível em `http://0.0.0.0:5000/api/docs`.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

    ```
    ├── aluno/
    │   ├── __init__.py
    │   ├── modelAluno.py
    │   └── routesAluno.py
    ├── professor/
    │   ├── __init__.py
    │   ├── modelProf.py
    │   └── routesProf.py
    ├── turma/
    │   ├── __init__.py
    │   ├── modelTurmas.py
    │   └── routesTurma.py
    ├── swagger/
    │   ├── __init__.py
    │   ├── namespace/
    │   │   ├── __init__.py
    │   │   ├── alunonamespace.py
    │   │   ├── profnamespace.py
    │   │   └── turmanamespace.py
    │   └── swagger_config.py
    ├── config.py
    ├── extensions.py
    ├── app.py       # Ou __init__.py
    ├── requirements.txt
    └── README.md
    ```

* `aluno/`, `professor/`, `turma/`: Contêm os modelos e rotas para os respectivos recursos.
* `swagger/`: Contém a configuração do Swagger.
* `config.py`: Arquivo de configuração da aplicação.
* `extensions.py`: Inicialização de extensões do Flask (como SQLAlchemy).
* `app.py`: Ponto de entrada da aplicação Flask.
* `requirements.txt`: Lista de dependências do projeto.
* `README.md`: Este arquivo.

## Configuração

A aplicação é configurada através da classe `Config` no arquivo `config.py`. As seguintes opções estão disponíveis:

* `DEBUG`: Ativa/desativa o modo de depuração do Flask.
* `SQLALCHEMY_DATABASE_URI`: URI de conexão do banco de dados.
* `SQLALCHEMY_TRACK_MODIFICATIONS`: Ativa/desativa o rastreamento de modificações do SQLAlchemy.
* `HOST`: Endereço IP em que o servidor irá rodar.
* `PORT`: Porta em que o servidor irá rodar.

## Testes

Para executar os testes, utilize o `pytest`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

\[Coloque aqui o tipo de licença\]
