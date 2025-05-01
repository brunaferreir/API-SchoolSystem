from flask_restx import Namespace, Resource, fields
from professor.modelProf import ProfessorNaoEncontrado, professor_por_id, get_professores , apaga_tudo, create_professores, deleteProfessor, atualizarProfessor, atualizarParcialProfessor



prof_ns = Namespace("professor", description="Dados relacionados aos professores")

prof_model = prof_ns.model("Professor", {
    "nome": fields.String(required=True, description="Nome do professor"),
    "idade":fields.Integer(required=True, description="Idade do professor"),
    "materia": fields.String(required=True, description="Materia lecionada"),
    "observacao":fields.String(required=True, description="Observação do professor")
})

prof_output_model = prof_ns.model("profOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(required=True, description="Nome do professor"),
    "idade":fields.Integer(required=True, description="Idade do professor"),
    "materia": fields.String(required=True, description="Materia lecionada"),
    "observacao":fields.String(required=True, description="Observação do professor")
})

@prof_ns.route("/")
class ProfResource(Resource):
    @prof_ns.marshal_list_with(prof_output_model)
    def get(self):
        """Lista todos os professores"""
        return get_professores()

    @prof_ns.expect(prof_model)
    def post(self):
        """Cria um novo professor"""
        data = prof_ns.payload
        print(f"Payload recebido: {data}")
        response, status_code = create_professores(data['nome'], data['idade'], data['materia'], data['observacao'])
        return response, status_code

@prof_ns.route("/<int:id_prof>")
class ProfIdResource(Resource):
    @prof_ns.marshal_with(prof_output_model)
    def get(self, id_prof):
        """Obtém um professor por ID"""
        return professor_por_id(id_prof)

    @prof_ns.expect(prof_model)
    def put(self, id_prof):
        """Atualiza um professor por ID"""
        data = prof_ns.payload
        atualizarParcialProfessor(id_prof, data)
        return data, 200

    def delete(self, id_prof):
        """Exclui um professor por ID"""
        deleteProfessor(id_prof)
        return {"message": "professor excluído com sucesso"}, 200