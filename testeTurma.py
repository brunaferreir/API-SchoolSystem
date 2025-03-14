import requests
import unittest
import json
from app import app

class TestStringMethods(unittest.TestCase):

    def test_000_turma_retorna_lista(self):

        r = requests.get('http://localhost:5000/turmas')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def teste_001_turma_criar(self):

        r= requests.post('http://localhost:5000/turmas',json={'nome':'ads','id':2,'professor':"caio"})
        r= requests.post('http://localhost:5000/turmas',json={'nome':'si','id':3,'professor':"caio"})

        r_lista = requests.get('http://localhost:5000/turmas')
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
    

    def test_002_reseta(self):
        #criei um aluno, com post
        r = requests.post('http://localhost:5000/turmas',json={'nome':'ads','id':25,'professor':'caio'})
        r_lista = requests.get('http://localhost:5000/turmas')
        self.assertTrue(len(r_lista.json()) > 0)

        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5000/turmas')
        self.assertEqual(len(r_lista_depois.json()),0)

    def teste_003_turma_deletar_id(self):
        #apago tudo
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        #crio 3 alunos
        requests.post('http://localhost:5000/turmas',json={'nome':'ads','id':25,'professor':'caio'})
        requests.post('http://localhost:5000/turmas',json={'nome':'si','id':28, 'professor':'felipe'})
        requests.post('http://localhost:5000/turmas',json={'nome':'bd','id':27, 'professor':'gustavo'})
        #pego a lista completa
        r_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista.json()
        self.assertEqual(len(lista_retornada),3)
        requests.delete('http://localhost:5000/turmas/28')
        r_lista2 = requests.get('http://localhost:5000/turmas')
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

        requests.delete('http://localhost:5000/turmas/27')

        r_lista3 = requests.get('http://localhost:5000/turmas')
        lista_retornada3 = r_lista3.json()
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'ads':
            pass
        else:
            self.fail("voce parece ter deletado a turma errada!")

    def teste_004_turmas_atualizar(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/turmas',json={'nome':'ads','id':28, 'professor':'caio'})
        r_antes = requests.get('http://localhost:5000/turmas/28')
        self.assertEqual(r_antes.json()['nome'],'ads')
        requests.put('http://localhost:5000/turmas/28', json={'nome':'ads manha'})
        r_depois = requests.get('http://localhost:5000/turmas/28')
        self.assertEqual(r_depois.json()['nome'],'ads manha')
        self.assertEqual(r_depois.json()['id'],28)

    def teste_005_atualizar_id_inexistente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        r = requests.put('http://localhost:5000/turmas/15',json={'nome':'eng. software','id':15, 'professor': 'joão'})

        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'Turma não encontrada')

    def teste_006_criar_faltando_parametro(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r_criacao = requests.post('http://localhost:5000/turmas', json={"id": 28})
        self.assertIn(r_criacao.status_code, [400, 422])
        resposta_json = r_criacao.json()
        self.assertIn('erro', resposta_json)
        self.assertEqual(resposta_json['erro'], 'Parâmetro obrigatório ausente')

    def teste_007_criar_com_id_existente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'banco de dados', 'id': 7, 'professor': 'joão'})
        self.assertEqual(r.status_code, 200)
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'ciencia da computação', 'id': 7, 'professor': 'caio'})
        self.assertEqual(r.status_code, 400)
        resposta_json = r.json()
        self.assertEqual(resposta_json.get('erro'), 'id ja utilizada')


    def teste_008_criar_com_tipos_invalidos(self):
        # Teste 1: "id" não é um número inteiro
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'ciencia da computação', 'id': 'g', 'professor': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro")

        # Teste 2: "nome" não é uma string
        r = requests.post('http://localhost:5000/turmas', json={'nome': 987, 'id': 7, 'professor': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")

        # Teste 3: "professor" não é uma string
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'ciencia da computação', 'id': 10, 'professor': 753})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O professor deve ser uma string")

    def teste_009_atualizar_com_tipos_invalidos(self):
        r = requests.put('http://localhost:5000/turmas/1', json={'nome': 'ciencia da computação', 'id': 'g', 'professor': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro")

        r = requests.put('http://localhost:5000/turmas/1', json={'nome': 987, 'id': 7, 'professor': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")

        r = requests.put('http://localhost:5000/turmas/1', json={'nome': 'ciencia da computação', 'id': 10, 'professor': 753})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O professor deve ser uma string")

if __name__ == '__main__':
    unittest.main()