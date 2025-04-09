import requests
import unittest
from app import app

class TestStringMethods(unittest.TestCase):

#----------------------ALUNO----------------------------

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



#----------------------------------------PROFESSOR--------------------------------------------------------------

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



#--------------------------------------TURMA-------------------------------------------------------------------

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