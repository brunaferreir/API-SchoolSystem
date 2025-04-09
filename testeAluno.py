import requests
import unittest
from app import app

class TestStringMethods(unittest.TestCase):

    def test_000_alunos_retorna_lista(self):
        r = requests.get('http://localhost:5002/alunos')

        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_001_adiciona_alunos(self):
        r = requests.post('http://localhost:5002/alunos',json={"id":5,"nome":"fernando"})
        r = requests.post('http://localhost:5002/alunos',json={"id":6,"nome":"roberto"})
        

        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()

        achei_fernando = False
        achei_roberto = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'fernando':
                achei_fernando = True
            if aluno['nome'] == 'roberto':
                achei_roberto = True

        if not achei_fernando:
            self.fail('aluno fernando nao apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('aluno roberto nao apareceu na lista de alunos')

    def test_002_aluno_por_id(self):
        r = requests.post('http://localhost:5002/alunos',json={"id":20,"nome":"mario"})

        resposta = requests.get('http://localhost:5002/alunos/20')
        dict_retornado = resposta.json()
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome',dict_retornado)
        self.assertEqual(dict_retornado['nome'],'mario')


    def test_003_reseta(self):
        r = requests.post('http://localhost:5002/alunos',json={'id':29,'nome':'cicero'})
        r_lista = requests.get('http://localhost:5002/alunos')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5002/reseta1')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_depois.json()),0)

   
    def test_004_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/alunos',json={'id':29,'nome':'cicero'})
        requests.post('http://localhost:5002/alunos',json={'id':28,'nome':'lucas'})
        requests.post('http://localhost:5002/alunos',json={'id':27,'nome':'marta'})

        r_lista = requests.get('http://localhost:5002/alunos')
        lista_retornada = r_lista.json()

        self.assertEqual(len(lista_retornada),3)

        requests.delete('http://localhost:5002/alunos/28')

        r_lista2 = requests.get('http://localhost:5002/alunos')
        lista_retornada2 = r_lista2.json()

        self.assertEqual(len(lista_retornada2),2) 

        acheiMarta = False
        acheiCicero = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'marta':
                acheiMarta=True
            if aluno['nome'] == 'cicero':
                acheiCicero=True
        if not acheiMarta or not acheiCicero:
            self.fail("voce parece ter deletado o aluno errado!")

        requests.delete('http://localhost:5002/alunos/27')

        r_lista3 = requests.get('http://localhost:5002/alunos')
        lista_retornada3 = r_lista3.json()

        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'cicero':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")


    def test_005_edita(self):
        #resetei
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)


        requests.post('http://localhost:5002/alunos',json={'id':28,'nome':'lucas'})
        #e peguei o dicionario dele
        r_antes = requests.get('http://localhost:5002/alunos/28')
        #o nome enviado foi lucas, o nome recebido tb
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5002/alunos/28', json={'nome':'lucas mendes'})
        #pego o novo dicionario do aluno 28
        r_depois = requests.get('http://localhost:5002/alunos/28')
        #agora o nome deve ser lucas mendes
        self.assertEqual(r_depois.json()['id'],28)
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    #tenta fazer GET, PUT e DELETE num aluno que nao existe
    def test_006_id_inexistente_no_put(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #estou tentando EDITAR um aluno que nao existe (verbo PUT)
        r = requests.put('http://localhost:5002/alunos/15',json={'id':15,'nome':'bowser'})
        #tem que dar erro 400 ou 404
        #ou seja, r.status_code tem que aparecer na lista [400,404]
        self.assertIn(r.status_code,[400,404])
        #qual a resposta que a linha abaixo pede?
        #um json, com o dicionario {"erro":"aluno nao encontrado"}
        self.assertEqual(r.json()['erro'],'Aluno não encontrado')
    

    def test_007_id_inexistente_no_get(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #agora faço o mesmo teste pro GET, a consulta por id
        r = requests.get('http://localhost:5002/alunos/15')
        self.assertIn(r.status_code,[400,404])
        #olhando pra essa linha debaixo, o que está especificado que o servidor deve retornar
        self.assertEqual(r.json()['erro'],'Aluno não encontrado')
        #                ------
       
    def test_008_id_inexistente_no_delete(self):
        #reseto
        r_reset = requests.post('http://localhost:5002/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5002/alunos/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'Aluno não encontrado')

    def test_009_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Cria um aluno com ID 1
        r_criar1 = requests.post('http://localhost:5002/alunos', json={'id': 1, 'nome': 'Alice'})
        self.assertEqual(r_criar1.status_code, 200)


        r_criar2 = requests.post('http://localhost:5002/alunos', json={'id': 1, 'nome': 'Bob'})
        self.assertEqual(r_criar2.status_code, 400)
        self.assertEqual(r_criar2.json()['erro'], 'id ja utilizada')


    def test_010_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        r = requests.post('http://localhost:5002/alunos',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
    

    def test_011_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno sem problemas
        r = requests.post('http://localhost:5002/alunos',json={'id':7,'nome':'maximus'})
        self.assertEqual(r.status_code,200)

        #mas tentei editar ele sem mandar o nome
        r = requests.put('http://localhost:5002/alunos/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')


    
 #--------------------------TESTES GIOVANA-----------------------------------   

    def test_012_post_com_tipos_invalidos(self):
        # Teste 1: "id" não é um número inteiro
        r = requests.post('http://localhost:5002/alunos', json={'id': 'g', 'nome': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro")

        # Teste 2: "nome" não é uma string
        r = requests.post('http://localhost:5002/alunos', json={'id': 7,'nome': 987})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")


    def test_013_put_com_tipos_invalidos(self):
        # Primeiro, cria um aluno para testar o PUT
        r = requests.post('http://localhost:5002/alunos', json={'id': 1,'nome': 'felipe'})

        # Teste 1: "id" não é um número inteiro
        r = requests.put('http://localhost:5002/alunos/1', json={'id': 'g', 'nome': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro")

        # Teste 2: "nome" não é uma string
        r = requests.put('http://localhost:5002/alunos/1', json={'id': 1, 'nome': 343})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")
        
        #Teste 3: "nome" não enviado
        r = requests.put('http://localhost:5002/alunos/1', json={'id': 2})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('erro'), 'aluno sem nome')

    

    def test_014_put_altera_id_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Cria dois alunos com IDs diferentes
        requests.post('http://localhost:5002/alunos', json={'id': 1, 'nome': 'carlos'})
        requests.post('http://localhost:5002/alunos', json={'id': 2, 'nome': ' joao'})

        # Tenta alterar o ID do primeiro aluno para o ID do segundo aluno
        r = requests.put('http://localhost:5002/alunos/1', json={'id': 2, 'nome': 'jose'})
        self.assertEqual(r.status_code, 400)  # Ou outro código de erro apropriado
        self.assertEqual(r.json().get('erro'), 'ID de aluno já existe') # Ou outra mensagem de erro


    def test_015_delete_inexistente_retorna_erro(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Tenta deletar um aluno com ID inexistente
        r_delete = requests.delete('http://localhost:5002/alunos/999')
        self.assertIn(r_delete.status_code, [400, 404])
        self.assertEqual(r_delete.json().get('erro'), 'Aluno não encontrado')    


def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()