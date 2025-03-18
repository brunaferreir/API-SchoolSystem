import requests
import unittest

'''
Cada aluno será representado por um dicionário JSON como o seguinte: 
{"id":1,"nome":"marcos"}

Testes 000 e 001: Na URL /alunos, se o verbo for GET, 
retornaremos uma lista com um dicionário para cada aluno.

Na URL /alunos, com o verbo POST, ocorrerá a criação do aluno,
enviando um desses dicionários 

Teste 002
Na URL /alunos/<int:id>, se o verbo for GET, devolveremos o nome e id do aluno. 
(exemplo. /alunos/2 devolve o dicionário do aluno(a) de id 2)

Teste 003
Na URL /reseta, apagaremos a lista de alunos e professores (essa URL só atende o verbo POST e DELETE).

Teste 004
Na URL /alunos/<int:id>, se o verbo for DELETE, deletaremos o aluno.
(dica: procure lista.remove)

Teste 005
Na URL /alunos/<int:id>, se o verbo for PUT, 
editaremos o aluno, mudando seu nome. 
Para isso, o usuário vai enviar um dicionário 
com a chave nome, que deveremos processar

Se o usuário manda um dicionário {“nome”:”José”} para a url /alunos/40,
com o verbo PUT, trocamos o nome do usuário 40 para José

Tratamento de erros

No teste 007, id inexistente no GET, tento acessar um aluno que não existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno nao encontrado'}
No teste 008, id inexistente no DELETE, tento deletar um aluno que não existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno nao encontrado'}
No teste 009, tento criar um aluno com um id que já existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'id ja utilizada'}
No teste 010, tento criar um aluno sem nome. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno sem nome'}
No teste 011, tento editar um aluno sem nome. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno sem nome'}
No teste 012, tento criar um aluno com um id que não é inteiro. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'O id deve ser um número inteiro'}
No teste 013, tento editar um aluno com um id que não é inteiro. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'O id deve ser um número inteiro'}
No teste 014, tento editar um aluno com um id que já existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'ID de aluno já existe'}
No teste 015, tento deletar um aluno com um id que não existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno nao encontrado'}



Testes 100 a 115: Teremos as URLs análogas para professores.

No teste 100, tento acessar a lista de professores.
No teste 101, tento adicionar professores.
No teste 102, tento acessar um professor por id.
No teste 103, tento adicionar professores e resetar a lista.
No teste 104, tento deletar um professor.
No teste 105, tento editar um professor.
No teste 106, tento editar um professor que não existe.

No teste 107, tento adicionar um professor com um id que já existe.
No teste 108, tento adicionar ou editar um professor sem nome.
No teste 109, tento adicionar um professor com um tipo de idade inválido. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'A idade deve ser um número inteiro'}
No teste 110, tento adicionar um professor com um tipo de matéria inválido. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'A matéria deve ser uma string'}

No teste 111, tento editar um professor alterando outros campos.
No teste 112, tento editar um professor com o tipo do nome invalido. Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'O nome deve ser uma string'}
No teste 113, tento editar um professor que não existe. Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'professor nao encontrado'}

No teste 114, tento adicionar um professor e um aluno com o mesmo id. Nesse caso, devemos retornar um código de status 200 e um dicionário {“erro”:'id ja utilizada'}
No teste 115, tento deletar um professor que não existe. Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'professor nao encontrado'}


Testes 200 a 214: Teremos as URLs análogas para turmas.

No teste 200, tento acessar a lista de turmas.
No teste 201, tento adicionar turmas.
No teste 202, tento resetar a lista de turmas.
No teste 203, tento deletar uma turma.
No teste 204, tento editar uma turma.
No teste 205, tento editar uma turma que não existe.Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'turma nao encontrada'}

No teste 206, tento adicionar faltando paramentros. Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'faltando parametros'}
No teste 207, tento adicionar uma turma com o id existente. Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'id ja utilizada'}
No teste 208 tendo adicionar uma turma com tipos invalidos. 
No teste 209 tento editar uma turma com o tipos invalidos. 
No teste 210 tento deletar id inexistente no delete.Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'turma nao encontrada'}
no teste 211 busca turma id inesistente. Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'turma nao encontrada'}
no teste 212 tento editar parcialmete.
No teste 213 criar turm sem json. 
No teste 214 tento criar turma com id negativo. Nesse caso devemos retornar um código de status 400 e um dicionário {“erro”:'id negativo'}





'''

class TestStringMethods(unittest.TestCase):


    def test_000_alunos_retorna_lista(self):
        #pega a url /alunos, com o verbo get
        r = requests.get('http://localhost:5000/alunos')

        #o status code foi pagina nao encontrada?
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")

        try:
            obj_retornado = r.json()
            #r.json() é o jeito da biblioteca requests
            #de pegar o arquivo que veio e transformar
            #em lista ou dicionario.
            #Vou dar erro se isso nao for possivel
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        #no caso, tem que ser uma lista
        self.assertEqual(type(obj_retornado),type([]))

    def test_001_adiciona_alunos(self):
        #criar dois alunos (usando post na url /alunos)
        r = requests.post('http://localhost:5000/alunos',json={"id":5,"nome":"fernando"})
        r = requests.post('http://localhost:5000/alunos',json={"id":6,"nome":"roberto"})
        
        #pego a lista de alunos (do mesmo jeito que no teste 0)
        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()#le o arquivo que o servidor respondeu
                                        #e transforma num dict/lista de python

        #faço um for para garantir que as duas pessoas que eu criei 
        #aparecem
        achei_fernando = False
        achei_roberto = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'fernando':
                achei_fernando = True
            if aluno['nome'] == 'roberto':
                achei_roberto = True
        
        #se algum desses "achei" nao for True, dou uma falha
        if not achei_fernando:
            self.fail('aluno fernando nao apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('aluno roberto nao apareceu na lista de alunos')

    def test_002_aluno_por_id(self):
        #cria um aluno 'mario', com id 20
        r = requests.post('http://localhost:5000/alunos',json={"id":20,"nome":"mario"})

        #consulta a url /alunos/20, pra ver se o aluno está lá
        resposta = requests.get('http://localhost:5000/alunos/20')
        dict_retornado = resposta.json() #pego o dicionario retornado
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome',dict_retornado)#o dicionario dict_retornado, que veio do servidor, 
        #tem que ter a chave nome
        self.assertEqual(dict_retornado['nome'],'mario') # no dic, o nome tem que ser o 
                                                   # que eu mandei
                                                   # tem que ser mario


    #adiciona um aluno, mas depois reseta o servidor
    #e o aluno deve desaparecer
    def test_003_reseta(self):
        #criei um aluno, com post
        r = requests.post('http://localhost:5000/alunos',json={'id':29,'nome':'cicero'})
        #peguei a lista
        r_lista = requests.get('http://localhost:5000/alunos')
        #no momento, a lista tem que ter mais de um aluno
        self.assertTrue(len(r_lista.json()) > 0)

        #POST na url reseta: deveria apagar todos os dados do servidor
        r_reset = requests.post('http://localhost:5000/reseta')

        #estou verificando se a url reseta deu pau
        #se voce ainda nao definiu ela, esse cod status nao vai ser 200
        self.assertEqual(r_reset.status_code,200)

        #pego de novo a lista
        r_lista_depois = requests.get('http://localhost:5000/alunos')
        
        #e agora tem que ter 0 elementos
        self.assertEqual(len(r_lista_depois.json()),0)

   
    def test_004_deleta(self):
        #apago tudo
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        #crio 3 alunos
        requests.post('http://localhost:5000/alunos',json={'id':29,'nome':'cicero'})
        requests.post('http://localhost:5000/alunos',json={'id':28,'nome':'lucas'})
        requests.post('http://localhost:5000/alunos',json={'id':27,'nome':'marta'})
        #pego a lista completa
        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()
        #a lista completa tem que ter 3 elementos
        self.assertEqual(len(lista_retornada),3)
        #faço um request com delete, pra deletar o aluno de id 28
        requests.delete('http://localhost:5000/alunos/28')
        #pego a lista de novo
        r_lista2 = requests.get('http://localhost:5000/alunos')
        lista_retornada2 = r_lista2.json()
        #e vejo se ficou só um elemento
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

        requests.delete('http://localhost:5000/alunos/27')

        r_lista3 = requests.get('http://localhost:5000/alunos')
        lista_retornada3 = r_lista3.json()
        #e vejo se ficou só um elemento
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'cicero':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")


    #cria um usuário, depois usa o verbo PUT
    #para alterar o nome do usuário
    def test_005_edita(self):
        #resetei
        r_reset = requests.post('http://localhost:5000/reseta')
        #verifiquei se o reset foi
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno
        requests.post('http://localhost:5000/alunos',json={'id':28,'nome':'lucas'})
        #e peguei o dicionario dele
        r_antes = requests.get('http://localhost:5000/alunos/28')
        #o nome enviado foi lucas, o nome recebido tb
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5000/alunos/28', json={'nome':'lucas mendes'})
        #pego o novo dicionario do aluno 28
        r_depois = requests.get('http://localhost:5000/alunos/28')
        #agora o nome deve ser lucas mendes
        self.assertEqual(r_depois.json()['id'],28)
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    #tenta fazer GET, PUT e DELETE num aluno que nao existe
    def test_006_id_inexistente_no_put(self):
        #reseto
        r_reset = requests.post('http://localhost:5000/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #estou tentando EDITAR um aluno que nao existe (verbo PUT)
        r = requests.put('http://localhost:5000/alunos/15',json={'id':15,'nome':'bowser'})
        #tem que dar erro 400 ou 404
        #ou seja, r.status_code tem que aparecer na lista [400,404]
        self.assertIn(r.status_code,[400,404])
        #qual a resposta que a linha abaixo pede?
        #um json, com o dicionario {"erro":"aluno nao encontrado"}
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
    

    def test_007_id_inexistente_no_get(self):
        #reseto
        r_reset = requests.post('http://localhost:5000/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #agora faço o mesmo teste pro GET, a consulta por id
        r = requests.get('http://localhost:5000/alunos/15')
        self.assertIn(r.status_code,[400,404])
        #olhando pra essa linha debaixo, o que está especificado que o servidor deve retornar
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
        #                ------
       
    def test_008_id_inexistente_no_delete(self):
        #reseto
        r_reset = requests.post('http://localhost:5000/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5000/alunos/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')

    def test_009_criar_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Cria um aluno com ID 1
        r_criar1 = requests.post('http://localhost:5000/alunos', json={'id': 1, 'nome': 'Alice'})
        self.assertEqual(r_criar1.status_code, 201)

        # Tenta criar outro aluno com o mesmo ID
        r_criar2 = requests.post('http://localhost:5000/alunos', json={'id': 1, 'nome': 'Bob'})
        self.assertEqual(r_criar2.status_code, 400)  # ou 409
        self.assertEqual(r_criar2.json()['erro'], 'id ja utilizada')


    #cria alunos sem nome, o que tem que dar erro
    def test_010_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        #tentei criar um aluno, sem enviar um nome
        r = requests.post('http://localhost:5000/alunos',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')
    



    #tenta editar alunos sem passar nome, o que também
    #tem que dar erro (se vc nao mudar o nome, vai mudar o que?)
    def test_011_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno sem problemas
        r = requests.post('http://localhost:5000/alunos',json={'id':7,'nome':'maximus'})
        self.assertEqual(r.status_code,201)

        #mas tentei editar ele sem mandar o nome
        r = requests.put('http://localhost:5000/alunos/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'aluno sem nome')


    
 #--------------------------TESTES GIOVANA-----------------------------------   

    def test_012_post_com_tipos_invalidos(self):
        # Teste 1: "id" não é um número inteiro
        r = requests.post('http://localhost:5000/alunos', json={'id': 'g', 'nome': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro")

        # Teste 2: "nome" não é uma string
        r = requests.post('http://localhost:5000/alunos', json={'id': 7,'nome': 987})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")


    def test_013_put_com_tipos_invalidos(self):
        # Primeiro, cria um aluno para testar o PUT
        r = requests.post('http://localhost:5000/alunos', json={'id': 1,'nome': 'felipe'})

        # Teste 1: "id" não é um número inteiro
        r = requests.put('http://localhost:5000/alunos/1', json={'id': 'g', 'nome': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro")

        # Teste 2: "nome" não é uma string
        r = requests.put('http://localhost:5000/alunos/1', json={'id': 1, 'nome': 343})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")
        
        #Teste 3: "nome" não enviado
        r = requests.put('http://localhost:5000/alunos/1', json={'id': 2})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('erro'), 'aluno sem nome')

    

    def test_014_put_altera_id_existente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Cria dois alunos com IDs diferentes
        requests.post('http://localhost:5000/alunos', json={'id': 1, 'nome': 'carlos'})
        requests.post('http://localhost:5000/alunos', json={'id': 2, 'nome': ' joao'})

        # Tenta alterar o ID do primeiro aluno para o ID do segundo aluno
        r = requests.put('http://localhost:5000/alunos/1', json={'id': 2, 'nome': 'jose'})
        self.assertEqual(r.status_code, 400)  # Ou outro código de erro apropriado
        self.assertEqual(r.json().get('erro'), 'ID de aluno já existe') # Ou outra mensagem de erro


    def test_015_delete_inexistente_retorna_erro(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Tenta deletar um aluno com ID inexistente
        r_delete = requests.delete('http://localhost:5000/alunos/999')
        self.assertIn(r_delete.status_code, [400, 404])
        self.assertEqual(r_delete.json().get('erro'), 'aluno nao encontrado')    


    



















#--------------------------TESTES 100 A 110: PROFESSORES---------------------------


    def test_100_professores_retorna_lista(self):
        r = requests.get('http://localhost:5000/professores')
        self.assertEqual(type(r.json()),type([]))
    
    def test_101_adiciona_professores(self):
        r = requests.post('http://localhost:5000/professores',json={'id':1,'nome':'fernando'})
        r = requests.post('http://localhost:5000/professores',json={'id':2,'nome':'roberto'})
        r_lista = requests.get('http://localhost:5000/professores')
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
        r = requests.post('http://localhost:5000/professores',json={"id": 3,"idade": 34,"materia": "POO","nome": "mario","observacao": "bom professor"})
        r_lista = requests.get('http://localhost:5000/professores/3')
        self.assertEqual(r_lista.json()['nome'],'mario')


    
    def test_103_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5000/professores',json={"id": 4,"idade": 34,"materia": "POO","nome": "cicera","observacao": "bom professor"})
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_104_deleta(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5000/professores',json={"id": 29,"idade": 34,"materia": "POO","nome": "cicera","observacao": "bom professor"})
        requests.post('http://localhost:5000/professores',json={"id": 28,"idade": 34,"materia": "POO","nome": "lucas","observacao": "bom professor"})
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5000/professores/28')
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_105_edita(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5000/professores',json={"id": 28,"idade": 34,"materia": "POO","nome": "lucas","observacao": "bom professor"})
        r_antes = requests.get('http://localhost:5000/professores/28')
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5000/professores/28', json={'nome':'lucas mendes'})
        r_depois = requests.get('http://localhost:5000/professores/28')
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    def test_106_id_inexistente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5000/professores/15',json={'id':15,"idade": 34,"materia": "POO","nome": "bowser","observacao": "bom professor"})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.get('http://localhost:5000/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.delete('http://localhost:5000/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')

    def test_107_post_com_id_ja_existente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5000/professores',json={'id':15,"idade": 34,"materia": "POO","nome": "bowser","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5000/professores',json={'id':15,"idade": 30,"materia": "sql","nome": "felipe","observacao": "bom professor"})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'id ja utilizada')

    def test_108_post_ou_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5000/professores',json={'id':8})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')
        r = requests.post('http://localhost:5000/professores',json={"id": 7,"idade": 30,"materia": "sql","nome": "felipe","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)

        r = requests.put('http://localhost:5000/professores/7',json={'id':7})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor sem nome')

    def test_109_post_professor_idade_tipo_invalido(self):
        # Tenta criar um professor com um tipo de idade inválido
        payload = {'id': 5, 'nome': 'Professor E Atualizado', 'idade': 'quarenta'}
        r = requests.post('http://localhost:5000/professores', json=payload)

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'A idade deve ser um número inteiro')    


    def test_110_post_professor_materia_tipo_invalido(self):
    # Tenta criar um professor com um tipo de matéria inválido
        payload = {'id': 6, 'nome': 'Professor F Atualizado', 'materia': 456}
        r = requests.post('http://localhost:5000/professores', json=payload)

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'A matéria deve ser uma string')
    
    

    def test_111_put_altera_outros_campos(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Cria um professor
        requests.post('http://localhost:5000/professores',
                      json={'id': 1, "idade": 30, "materia": "POO", "nome": "Professor 1",
                            "observacao": "Bom professor"})

        # Altera outros campos
        r_atualizar = requests.put('http://localhost:5000/professores/1',
                                  json={'idade': 35, 'materia': 'Python',"nome": "Professor 1", 'observacao': 'Excelente professor'})
        self.assertEqual(r_atualizar.status_code, 200)

        # Verifica se os campos foram alterados corretamente
        r_get = requests.get('http://localhost:5000/professores/1')
        self.assertEqual(r_get.status_code, 200)
        professor_atualizado = r_get.json()
        self.assertEqual(professor_atualizado['idade'], 35)
        self.assertEqual(professor_atualizado['materia'], 'Python')
        self.assertEqual(professor_atualizado['observacao'], 'Excelente professor')
        self.assertEqual(professor_atualizado['nome'], 'Professor 1')  # Nome não deve ter mudado

    def test_112_put_professor_nome_tipo_invalido(self):
        # Cria um professor primeiro
        requests.post('http://localhost:5000/professores', json={'id': 3,'idade': 35, 'materia': 'Python',"nome": "Professor 1", 'observacao': 'Excelente professor'})

        # Tenta atualizar com um tipo de nome inválido
        payload = {'nome': 123}
        r = requests.put('http://localhost:5000/professores/3', json=payload)

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'O nome deve ser uma string') 


    def test_113_put_professor_nao_encontrado(self):
        # Tenta atualizar um professor que não existe
        payload = {'nome': 'Professor H Atualizado'}
        r = requests.put('http://localhost:5000/professores/999', json=payload)

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'professor nao encontrado')  


    def test_114_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        r = requests.post('http://localhost:5000/professores',json={'id':1,"idade": 34,"materia": "POO","nome": "fernando","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5000/professores',json={'id':2,"idade": 34,"materia": "sql","nome": "roberto","observacao": "bom professor"})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),2)
        r_lista_alunos = requests.get('http://localhost:5000/alunos')
        self.assertEqual(len(r_lista_alunos.json()),0)
    

    def test_115_delete_professor_nao_encontrado(self):
        # Tenta deletar um professor que não existe
        r = requests.delete('http://localhost:5000/professores/999')

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['erro'], 'professor nao encontrado') 





#---------------------------------TURMAS--------------------------------------- 
# Testes 200 a 215: Teremos as URLs análogas para turmas.
#   
    def test_200_turma_retorna_lista(self):

        r = requests.get('http://localhost:5000/turmas')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")

        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_201_turma_criar(self):

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
    

    def test_202_reseta(self):
        #criei um aluno, com post
        r = requests.post('http://localhost:5000/turmas',json={'nome':'ads','id':25,'professor':'caio'})
        r_lista = requests.get('http://localhost:5000/turmas')
        self.assertTrue(len(r_lista.json()) > 0)

        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5000/turmas')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_203_turma_deletar(self):
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
        

    def test_204_turmas_atualizar(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        # Cria uma turma para ser atualizada
        requests.post('http://localhost:5000/turmas', json={'nome': 'ads', 'id': 28, 'professor': 'caio'})

        # Verifica se a turma foi criada corretamente
        r_antes = requests.get('http://localhost:5000/turmas/28')
        self.assertEqual(r_antes.json()['nome'], 'ads')

        # Atualiza a turma usando PUT
        requests.put('http://localhost:5000/turmas/28', json={'nome': 'ads manha', 'id': 28, 'professor': 'caio'})

        # Verifica se a turma foi atualizada corretamente
        r_depois = requests.get('http://localhost:5000/turmas/28')
        self.assertEqual(r_depois.json()['nome'], 'ads manha')
        self.assertEqual(r_depois.json()['id'], 28)
        self.assertEqual(r_depois.json()['professor'], 'caio')

    def test_205_atualizar_id_inexistente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        r = requests.put('http://localhost:5000/turmas/15', json={'nome': 'eng. software'})

        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json()['erro'], 'Turma não encontrada')

    def test_206_criar_faltando_parametro(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        r_criacao = requests.post('http://localhost:5000/turmas', json={"id": 28})
        self.assertIn(r_criacao.status_code, [400, 422])
        resposta_json = r_criacao.json()
        self.assertIn('erro', resposta_json)
        self.assertEqual(resposta_json['erro'], 'Parâmetro obrigatório ausente')

    def test_207_criar_com_id_existente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'banco de dados', 'id': 7, 'professor': 'vinicius'})
        self.assertEqual(r.status_code, 200)
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'ciencia da computação', 'id': 7, 'professor': 'caio'})
        self.assertEqual(r.status_code, 400)
        resposta_json = r.json()
        self.assertEqual(resposta_json.get('erro'), 'id ja utilizada')


    def test_208_criar_com_tipos_invalidos(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        # Teste 1: "id" não é um número inteiro
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'ciencia da computação', 'id': 'g', 'professor': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O id deve ser um número inteiro positivo")

        # Teste 2: "nome" não é uma string
        r = requests.post('http://localhost:5000/turmas', json={'nome': 987, 'id': 7, 'professor': 'felipe'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O nome deve ser uma string")

        # Teste 3: "professor" não é uma string
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'ciencia da computação', 'id': 10, 'professor': 753})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get("erro"), "O professor deve ser uma string")

    def test_209_atualizar_com_tipos_invalidos(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/turmas', json={'nome': 'ads', 'id': 5, 'professor': 'caio'})

        # Atualizar com tipos inválidos
        r = requests.put('http://localhost:5000/turmas/5', json={'nome': 123, 'id': 'abc', 'professor': True})
        self.assertEqual(r.status_code, 400)

    def test_210_id_inexistente_no_delete(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5000/turmas/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'Turma não encontrada')

    def test_211_buscar_turma_id_inexistente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        
        r = requests.get('http://localhost:5000/turmas/99')
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json()['erro'], 'Turma não encontrada')

    def test_212_atualizar_parcialmente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        requests.post('http://localhost:5000/turmas', json={'nome': 'ads', 'id': 5, 'professor': 'caio'})
        
        # atualizar professor
        r = requests.patch('http://localhost:5000/turmas/5', json={'professor': 'vinicius'})
        self.assertEqual(r.status_code, 200)

        # verificar se mudou o prof
        r_turma = requests.get('http://localhost:5000/turmas/5')
        turma = r_turma.json()
        self.assertEqual(turma['nome'], 'ads')
        self.assertEqual(turma['id'], 5)
        self.assertEqual(turma['professor'], 'vinicius')

    def test_213_criar_turma_sem_json(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)
        r = requests.post('http://localhost:5000/turmas', data="")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('erro'), 'JSON inválido ou não fornecido')

    def test_214_criar_turma_com_id_negativo(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'ads', 'id': -5, 'professor': 'caio'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('erro'), 'O id deve ser um número inteiro positivo')






def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()