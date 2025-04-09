import requests
import unittest
from app import app 

class TestStringMethods(unittest.TestCase):
      
      
    def test_100_professores_retorna_lista(self):
        r = requests.get('http://localhost:5002/professores')
        self.assertEqual(type(r.json()),type([]))
    

    def test_101_adiciona_professores(self):
        r = requests.post('http://localhost:5002/professores',json={"id":3,"nome":"fernando", "idade":30, "materia":"matematica", "observacao":"bom professor"})
        r = requests.post('http://localhost:5002/professores',json={'id':4,'nome':'roberto', "idade":50, "materia":"poo", "observacao":"bom professor"})
        r_lista = requests.get('http://localhost:5002/professores')
        achei_fernando = False
        achei_roberto = False
        for professor in r_lista.json():
            if professor['nome'] == 'fernando':
                achei_fernando = True
            if professor['nome'] == 'roberto':
                achei_roberto = True
        if not achei_fernando:
            self.fail('professor fernando nao apareceu na lista de professores')
        if not achei_roberto:
            self.fail('professor roberto nao apareceu na lista de professores')



    def test_102_professores_por_id(self):
        r = requests.post('http://localhost:5002/professores',json={"id": 5,"nome": "mario","idade": 34,"materia": "POO","observacao": "bom professor"})
        r_lista = requests.get('http://localhost:5002/professores/5')
        self.assertEqual(r_lista.json()['nome'],'mario')


    def test_103_reseta(self):
        r = requests.post('http://localhost:5002/professores',json={"id": 6,"nome": "mario","idade": 34,"materia": "POO","observacao": "bom professor"})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta2')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista_depois.json()),0)
  

    def test_104_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={"id": 29,"nome": "cicera","idade": 34,"materia": "POO","observacao": "bom professor"})
        requests.post('http://localhost:5002/professores',json={"id": 28,"nome": "lucas","idade": 34,"materia": "POO","observacao": "bom professor"})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/professores/28')
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),1)
    

    def test_105_edita(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5002/professores',json={"id": 28,"nome": "lucas","idade": 34,"materia": "POO","observacao": "bom professor"})
        #e peguei o dicionario dele
        r_antes = requests.get('http://localhost:5002/professores/28')
        #o nome enviado foi lucas, o nome recebido tb
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5002/professores/28', json={'nome':'lucas mendes'})
        #pego o novo dicionario do aluno 28
        r_depois = requests.get('http://localhost:5002/professores/28')
        #agora o nome deve ser lucas mendes
        self.assertEqual(r_depois.json()['id'],28)
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')
           


    def test_106_id_inexistente_no_put(self):
         #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #estou tentando EDITAR um aluno que nao existe (verbo PUT)
        r = requests.put('http://localhost:5002/professores/15',json={'id':15, "nome": "bowser", "idade": 34,"materia": "POO","observacao": "bom professor"})
        #tem que dar erro 400 ou 404
        #ou seja, r.status_code tem que aparecer na lista [400,404]
        self.assertIn(r.status_code,[400,404])
        #qual a resposta que a linha abaixo pede?
        #um json, com o dicionario {"erro":"aluno nao encontrado"}
        self.assertEqual(r.json()['erro'],'Professor não encontrado')


    def test_107_id_inexistente_no_get(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #agora faço o mesmo teste pro GET, a consulta por id
        r = requests.get('http://localhost:5002/professores/15')
        self.assertIn(r.status_code,[400,404])
        #olhando pra essa linha debaixo, o que está especificado que o servidor deve retornar
        self.assertEqual(r.json()['erro'],'Professor não encontrado')    

    def test_108_id_inexistente_no_delete(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/professores/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'Professor não encontrado')    
    

    def  test_109_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':15, "nome": "bowser", "idade": 34,"materia": "POO","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':15, "nome": "felipe", "idade": 34,"materia": "POO","observacao": "bom professor"})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_110_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        r = requests.post('http://localhost:5002/professores',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'Parâmetro obrigatório ausente')
    
    def test_111_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        #criei um professor sem problemas
        r = requests.post('http://localhost:5002/professores',json={'id':7,'nome':'maximus', 'idade': 34,'materia': 'POO','observacao': 'bom professor'})
        self.assertEqual(r.status_code,200)

        #mas tentei editar ele sem mandar o nome
        r = requests.put('http://localhost:5002/professores/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')

    def test_112_post_com_tipos_invalidos(self):
        # Teste 1: "id" não é um número inteiro
        r = requests.post('http://localhost:5002/professores', json={'id':"g", "nome": "bowser", "idade": 34,"materia": "POO","observacao": "bom professor"})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro positivo")

        # Teste 2: "nome" não é uma string
        r = requests.post('http://localhost:5002/professores', json={"id": 7,"nome": 987, "idade": 34,"materia": "POO","observacao": "bom professor"})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")


    def test_113_put_com_tipos_invalidos(self):
        # Primeiro, cria um professor para testar o PUT
        r = requests.post('http://localhost:5002/professores', json={'id': 1,'nome': 'felipe', 'idade': 34,'materia': 'POO','observacao': 'bom professor'})

        # Teste 1: "id" não é um número inteiro
        r = requests.put('http://localhost:5002/professores/1', json={'id': 'g','nome': 'felipe', 'idade': 34,'materia': 'POO','observacao': 'bom professor'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro")

        # Teste 2: "nome" não é uma string
        r = requests.put('http://localhost:5002/professores/1', json={'id': 1, 'nome': 343, 'idade': 34,'materia': 'POO','observacao': 'bom professor'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")
        
        #Teste 3: "nome" não enviado
        r = requests.put('http://localhost:5002/professores/1', json={'id': 2})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('erro'), 'professor sem nome')

    

    def test_114_put_altera_id_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Cria dois professores com IDs diferentes
        requests.post('http://localhost:5002/professores', json={'id': 1, 'nome': 'carlos','idade': 34,'materia': 'POO','observacao': 'bom professor'})
        requests.post('http://localhost:5002/professores', json={'id': 2, 'nome': ' joao', 'idade': 34,'materia': 'POO','observacao': 'bom professor'})

        # Tenta alterar o ID do primeiro professores para o ID do segundo professores
        r = requests.put('http://localhost:5002/professores/1', json={'id': 2, 'nome': 'jose', 'idade': 34,'materia': 'POO','observacao': 'bom professor'})
        self.assertEqual(r.status_code, 400)  # Ou outro código de erro apropriado
        self.assertEqual(r.json().get('erro'), 'ID de professor já existe') # Ou outra mensagem de erro
        
    def test_115_delete_inexistente_retorna_erro(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Tenta deletar um professores com ID inexistente
        r_delete = requests.delete('http://localhost:5002/professores/999')
        self.assertIn(r_delete.status_code, [400, 404])
        self.assertEqual(r_delete.json().get('erro'), 'Professor não encontrado')  



def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()