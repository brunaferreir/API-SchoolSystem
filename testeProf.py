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

        r_reset = requests.post('http://localhost:5002/reseta1')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista_depois.json()),0)
  

    def test_104_deleta(self):
        r_reset = requests.post('http://localhost:5002/reseta1')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5002/professores',json={"id": 29,"nome": "cicera","idade": 34,"materia": "POO","observacao": "bom professor"})
        requests.post('http://localhost:5002/professores',json={"id": 28,"nome": "lucas","idade": 34,"materia": "POO","observacao": "bom professor"})
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5002/professores/28')
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),1)
    









    def test_105_edita(self):
            r_reset = requests.post('http://localhost:5002/reseta1')
            self.assertEqual(r_reset.status_code,200)
        
            requests.post('http://localhost:5002/professores', json={"id": 28,"nome": "lucas","idade": 34,"materia": "POO","observacao": "bom professor"})

            r_antes = requests.get('http://localhost:5002/professores/28')
            self.assertEqual(r_antes.json()['nome'], 'lucas')

          
            requests.put('http://localhost:5002/professores/28', json={"id": 28,"nome": "lucas mendes","idade": 34,"materia": "POO","observacao": "bom professor"})

            r_depois = requests.get('http://localhost:5002/professores/28')
            self.assertEqual(r_depois.json()['id'], 28)
            self.assertEqual(r_depois.json()['nome'], 'lucas mendes')
            self.assertEqual(r_depois.json()['idade'], 34)
            self.assertEqual(r_depois.json()['materia'], 'POO')
            self.assertEqual(r_depois.json()['observacao'], 'bom professor')




    def test_106_id_inexistente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5002/professores/15',json={'id':15, "nome": "bowser", "idade": 34,"materia": "POO","observacao": "bom professor"})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.get('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.delete('http://localhost:5002/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')

    def test_107_post_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':15, "nome": "bowser", "idade": 34,"materia": "POO","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':15, "nome": "felipe", "idade": 34,"materia": "POO","observacao": "bom professor"})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_108_post_ou_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')
        r = requests.post('http://localhost:5002/professores',json={"id": 7,"idade": 30,"materia": "sql","nome": "felipe","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)

        r = requests.put('http://localhost:5002/professores/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')

    def test_109_post_professor_idade_tipo_invalido(self):
        # Tenta criar um professor com um tipo de idade inválido
        payload = {'id': 5, 'nome': 'Professor E Atualizado', 'idade': 'quarenta'}
        r = requests.post('http://localhost:5002/professores', json=payload)

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'A idade deve ser um número inteiro')    


    def test_110_post_professor_materia_tipo_invalido(self):
    # Tenta criar um professor com um tipo de matéria inválido
        payload = {'id': 6, 'nome': 'Professor F Atualizado', 'materia': 456}
        r = requests.post('http://localhost:5002/professores', json=payload)

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'A matéria deve ser uma string')
    
    

    def test_111_put_altera_outros_campos(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Cria um professor
        requests.post('http://localhost:5002/professores',
                      json={'id': 1, "idade": 30, "materia": "POO", "nome": "Professor 1",
                            "observacao": "Bom professor"})

        # Altera outros campos
        r_atualizar = requests.put('http://localhost:5000/professores/1',
                                  json={'idade': 35, 'materia': 'Python',"nome": "Professor 1", 'observacao': 'Excelente professor'})
        self.assertEqual(r_atualizar.status_code, 200)

        # Verifica se os campos foram alterados corretamente
        r_get = requests.get('http://localhost:5002/professores/1')
        self.assertEqual(r_get.status_code, 200)
        professor_atualizado = r_get.json()
        self.assertEqual(professor_atualizado['idade'], 35)
        self.assertEqual(professor_atualizado['materia'], 'Python')
        self.assertEqual(professor_atualizado['observacao'], 'Excelente professor')
        self.assertEqual(professor_atualizado['nome'], 'Professor 1')  # Nome não deve ter mudado

    def test_112_put_professor_nome_tipo_invalido(self):
        # Cria um professor primeiro
        requests.post('http://localhost:5002/professores', json={'id': 3,'idade': 35, 'materia': 'Python',"nome": "Professor 1", 'observacao': 'Excelente professor'})

        # Tenta atualizar com um tipo de nome inválido
        payload = {'nome': 123}
        r = requests.put('http://localhost:5002/professores/3', json=payload)

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'O nome deve ser uma string') 


    def test_113_put_professor_nao_encontrado(self):
        # Tenta atualizar um professor que não existe
        payload = {'nome': 'Professor H Atualizado'}
        r = requests.put('http://localhost:5002/professores/999', json=payload)

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'professor nao encontrado')  


    def test_114_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5002/reseta')
        r = requests.post('http://localhost:5002/professores',json={'id':1,"idade": 34,"materia": "POO","nome": "fernando","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5002/professores',json={'id':2,"idade": 34,"materia": "sql","nome": "roberto","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5002/professores')
        self.assertEqual(len(r_lista.json()),2)
        r_lista_alunos = requests.get('http://localhost:5002/alunos')
        self.assertEqual(len(r_lista_alunos.json()),0)
    

    def test_115_delete_professor_nao_encontrado(self):
        # Tenta deletar um professor que não existe
        r = requests.delete('http://localhost:5002/professores/999')

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'professor nao encontrado') 



def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()