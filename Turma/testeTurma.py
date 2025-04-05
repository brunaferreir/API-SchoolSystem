import requests
import unittest
from app import app 

class TestStringMethods(unittest.TestCase):

    def test_200_turma_retorna_lista(self):

        r = requests.get('http://localhost:5002/turmas')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_201_turma_criar(self):

            r= requests.post('http://localhost:5002/turmas',json={'nome':'ads','id':2,'professor':"caio"})
            r= requests.post('http://localhost:5002/turmas',json={'nome':'si','id':3,'professor':"caio"})

            r_lista = requests.get('http://localhost:5002/turmas')
            lista_retornada = r_lista.json()
            achei_ads = False
            achei_si = False
            for turmas in lista_retornada:
                if turmas['nome'] == 'ads':
                    achei_ads= True
                if turmas['nome'] == 'si':
                    achei_si = True
            
            if not achei_ads:
                self.fail('turma ads não encontrada na lista de turmas')
            if not achei_si:
                self.fail('turma si não encontrada na lista de turmas')
        

    def test_202_reseta(self):
            
            r = requests.post('http://localhost:5002/turmas',json={'nome':'ads','id':25,'professor':'caio'})
            r_lista = requests.get('http://localhost:5002/turmas')
            self.assertTrue(len(r_lista.json()) > 0)

            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)
            r_lista_depois = requests.get('http://localhost:5002/turmas')
            self.assertEqual(len(r_lista_depois.json()),0)

    def test_203_turma_deletar(self):
            #apago tudo
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)
            #crio 3 alunos
            requests.post('http://localhost:5002/turmas',json={'nome':'ads','id':25,'professor':'caio'})
            requests.post('http://localhost:5002/turmas',json={'nome':'si','id':28, 'professor':'felipe'})
            requests.post('http://localhost:5002/turmas',json={'nome':'bd','id':27, 'professor':'gustavo'})
            #pego a lista completa
            r_lista = requests.get('http://localhost:5002/turmas')
            lista_retornada = r_lista.json()
            self.assertEqual(len(lista_retornada),3)
            requests.delete('http://localhost:5002/turmas/28')
            r_lista2 = requests.get('http://localhost:5002/turmas')
            lista_retornada2 = r_lista2.json()
            self.assertEqual(len(lista_retornada2),2)

            acheiBD = False
            acheiAds = False
            for aluno in lista_retornada:
                if aluno['nome'] == 'bd':
                    acheiBD=True
                if aluno['nome'] == 'ads':
                    acheiAds=True
            if not acheiBD or not acheiAds:
                self.fail("voce parece ter deletado a turma errada!")

            requests.delete('http://localhost:5002/turmas/27')

            r_lista3 = requests.get('http://localhost:5002/turmas')
            lista_retornada3 = r_lista3.json()
            self.assertEqual(len(lista_retornada3),1) 

            if lista_retornada3[0]['nome'] == 'ads':
                pass
            else:
                self.fail("voce parece ter deletado a turma errada!")
            

    def test_204_turmas_atualizar(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)
            # Cria uma turma para ser atualizada
            requests.post('http://localhost:5002/turmas', json={'nome': 'ads', 'id': 28, 'professor': 'caio'})

            # Verifica se a turma foi criada corretamente
            r_antes = requests.get('http://localhost:5002/turmas/28')
            self.assertEqual(r_antes.json()['nome'], 'ads')

            # Atualiza a turma usando PUT
            requests.put('http://localhost:5002/turmas/28', json={'nome': 'ads manha', 'id': 28, 'professor': 'caio'})

            # Verifica se a turma foi atualizada corretamente
            r_depois = requests.get('http://localhost:5002/turmas/28')
            self.assertEqual(r_depois.json()['nome'], 'ads manha')
            self.assertEqual(r_depois.json()['id'], 28)
            self.assertEqual(r_depois.json()['professor'], 'caio')

    def test_205_atualizar_id_inexistente(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)

            r = requests.put('http://localhost:5002/turmas/15', json={'nome': 'eng. software'})

            self.assertEqual(r.status_code, 404)
            self.assertEqual(r.json()['erro'], 'Turma não encontrada')

    def test_206_criar_faltando_parametro(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)

            r_criacao = requests.post('http://localhost:5002/turmas', json={"id": 28})
            self.assertIn(r_criacao.status_code, [400, 422])
            resposta_json = r_criacao.json()
            self.assertIn('erro', resposta_json)
            self.assertEqual(resposta_json['erro'], 'Parâmetro obrigatório ausente')
            
    def test_207_criar_com_id_existente(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)
            r = requests.post('http://localhost:5002/turmas', json={'nome': 'banco de dados', 'id': 7, 'professor': 'vinicius'})
            self.assertEqual(r.status_code, 200)
            r = requests.post('http://localhost:5002/turmas', json={'nome': 'ciencia da computação', 'id': 7, 'professor': 'caio'})
            self.assertEqual(r.status_code, 400)
            resposta_json = r.json()
            self.assertEqual(resposta_json.get('erro'), 'id ja utilizada')

    def test_208_criar_com_tipos_invalidos(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)
            # Teste 1: "id" não é um número inteiro
            r = requests.post('http://localhost:5002/turmas', json={'nome': 'ciencia da computação', 'id': 'g', 'professor': 'felipe'})
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro positivo")

            # Teste 2: "nome" não é uma string
            r = requests.post('http://localhost:5002/turmas', json={'nome': 987, 'id': 7, 'professor': 'felipe'})
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")

            # Teste 3: "professor" não é uma string
            r = requests.post('http://localhost:5002/turmas', json={'nome': 'ciencia da computação', 'id': 10, 'professor': 753})
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json().get("erro"), "O professor deve ser uma string")

    def test_209_atualizar_com_tipos_invalidos(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)

            requests.post('http://localhost:5002/turmas', json={'nome': 'ads', 'id': 5, 'professor': 'caio'})

            # Atualizar com tipos inválidos
            r = requests.put('http://localhost:5002/turmas/5', json={'nome': 123, 'id': 'abc', 'professor': True})
            self.assertEqual(r.status_code, 400)

#erro
    def test_210_id_inexistente_no_delete(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)
            r = requests.delete('http://localhost:5002/turmas/15')
            self.assertIn(r.status_code,[400,404])
            self.assertEqual(r.json()['erro'],'Turma não encontrada')

    def test_211_buscar_turma_id_inexistente(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)
            
            r = requests.get('http://localhost:5002/turmas/99')
            self.assertIn(r.status_code, [400, 404])
            self.assertEqual(r.json()['erro'], 'Turma não encontrada')

#erro
    def test_212_atualizar_parcialmente(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code,200)

            requests.post('http://localhost:5002/turmas', json={'nome': 'ads', 'id': 5, 'professor': 'caio'})
            
            # atualizar professor
            r = requests.patch('http://localhost:5002/turmas/5', json={'professor': 'vinicius'})
            self.assertEqual(r.status_code, 200)

            # verificar se mudou o prof
            r_turma = requests.get('http://localhost:5002/turmas/5')
            turma = r_turma.json()
            self.assertEqual(turma['nome'], 'ads')
            self.assertEqual(turma['id'], 5)
            self.assertEqual(turma['professor'], 'vinicius')

#erro
    def test_213_criar_turma_sem_json(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code, 200)
            r = requests.post('http://localhost:5002/turmas', data="")
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json().get('erro'), 'JSON inválido ou não fornecido')

#erro
    def test_214_criar_turma_com_id_negativo(self):
            r_reset = requests.post('http://localhost:5002/reseta')
            self.assertEqual(r_reset.status_code, 200)
            r = requests.post('http://localhost:5002/turmas', json={'nome': 'ads', 'id': -5, 'professor': 'caio'})
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json().get('erro'), 'O id deve ser um número inteiro positivo')



def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()