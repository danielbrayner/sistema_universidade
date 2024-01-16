from flask import Flask, render_template, request, jsonify
import psycopg2
import json

app = Flask(__name__)

app.secret_key = 'unichristus'

class Aluno():
    def __init__(self, senha, nome_completo, matricula, curso, email, semestre, status):
        self.senha  = senha
        self.nome_completo  = nome_completo
        self.matricula = matricula
        self.curso = curso
        self.email= email
        self.semestre = semestre
        self.status = status

class Docente():
    def __init__(self, senha, nome_docente, matricula_docente, email):
        self.senha  = senha
        self.nome_docente  = nome_docente
        self.matricula_docente = matricula_docente
        self.email = email



def conectar_bd(banco_de_dados):
    conectar = psycopg2.connect(database=banco_de_dados, user="postgres", password="123", host="localhost")
    cur = conectar.cursor()

    return conectar, cur

def pegar_cpf_login(cur, tabela):
    cur.execute(f"SELECT cpf FROM {tabela}")
    resultado = cur.fetchall()

    lista_cpf = []
    for cpf in resultado:
        lista_cpf.append(cpf[0])

    return lista_cpf

def pegar_lista_disciplinas(cur):
    cur.execute(f"SELECT d.nome_disciplina "
                f"FROM aluno a JOIN aluno_turma at "
                f"ON a.cpf = at.cpf_aluno "
                f"JOIN turmas t "
                f"ON at.cod_turma = t.cod_turma "
                f"JOIN disciplina d ON t.cod_disciplina = d.cod_disciplina "
                f"WHERE a.cpf = '{login_digitado}'")
    lista_disciplinas = cur.fetchall()
    lista_disciplinas.sort()
    return lista_disciplinas

def pegar_notas_disciplinas(cur, lista_disciplinas):
    for i in range (len(lista_disciplinas)):
        cur.execute(f"SELECT nome_disciplina, np1, np2, np3 FROM disciplina d, notas n, aluno_turma alt, turmas t WHERE n.id_notas = alt.id_notas and alt.cod_turma  = t.cod_turma and t.cod_disciplina = d.cod_disciplina and alt.cpf_aluno = '{login_digitado}'")
        notas_bd = cur.fetchall()
    return notas_bd

def pegar_lista_disciplinas_docente (cur):
    cur.execute(f"SELECT nome_disciplina, cod_turma "
                f"FROM docente d, turmas t, disciplina di "
                f"WHERE d.cpf = t.cpf_professor and t.cod_disciplina = di.cod_disciplina and d.cpf = '{login_digitado}'")

    lista_disciplinas_docente = cur.fetchall()
    lista_disciplinas_docente.sort()
    return lista_disciplinas_docente

def pegar_codigos_turmas_docente_e_nome_disciplina(cur):
    cur.execute (f"SELECT t.cod_turma, di.nome_disciplina "
                 f"FROM turmas t "
                 f"JOIN docente d "
                 f"ON t.cpf_professor = d.cpf "
                 f"JOIN disciplina di "
                 f"ON t.cod_disciplina = di.cod_disciplina "
                 f"WHERE d.cpf = '{login_digitado}'");


    lista_codigo_turmas_docente = cur.fetchall()
    lista_codigo_turmas_docente.sort()
    return lista_codigo_turmas_docente

def pegar_lista_aluno_cada_disciplina(cur, lista_codigo_turmas_docente):
    lista_alunos_cada_disciplina = []
    for cod_turma in lista_codigo_turmas_docente:
        cur.execute(f"SELECT nome, id_notas "
                    f"FROM aluno a "
                    f"JOIN aluno_turma at "
                    f"ON a.cpf = at.cpf_aluno "
                    f"JOIN turmas t ON at.cod_turma = t.cod_turma "
                    f"WHERE t.cod_turma = '{cod_turma[0]}'")


        resultado = cur.fetchall()
        lista_alunos_cada_disciplina.append(cod_turma)
        lista_alunos_cada_disciplina.append(resultado)
    return lista_alunos_cada_disciplina


def atualizar_notas_banco_de_dados(conectar, cur, np1, np2, np3, id_notas):
    for i in range (len(np1)):
        print (np1[i])
        print (np2[i])
        print (np3[i])
        print (id_notas[i])
        cur.execute(f"UPDATE notas SET np1 = '{np1[i]}', np2 = '{np2[i]}', np3 = '{np3[i]}' WHERE id_notas = '{id_notas[i]}'")
    conectar.commit()
    return





@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        opcao = request.form.get('opcao')

        if opcao == 'opcao_aluno_online':


            conectar, cur = conectar_bd("unichristus")
            lista_cpf = pegar_cpf_login(cur, "aluno")

            global login_digitado
            login_digitado = request.form['usuario']
            password_digitado = request.form['password']

            if login_digitado in lista_cpf:

                cur.execute(f"SELECT senha, nome, matricula, curso, email, semestre, status FROM aluno WHERE cpf = '{login_digitado}'")
                dados = cur.fetchall()

                global aluno
                aluno = Aluno(dados[0][0], dados[0][1], dados[0][2], dados[0][3], dados[0][4], dados[0][5], dados[0][6])

                if aluno.senha == password_digitado:
                    conectar.close()
                    return sistema_aluno_aviso()

                else:
                    conectar.close()
                    return render_template('login.html', login_digitado="Login/Senha incorretos!")
            else:
                return render_template('login.html', login_digitado="Login/Senha incorretos!")

        elif opcao == 'opcao_docente_online':

            conectar, cur = conectar_bd("unichristus")
            lista_cpf = pegar_cpf_login(cur, "docente")

            login_digitado = request.form['usuario']
            password_digitado = request.form['password']

            if login_digitado in lista_cpf:
                cur.execute(f"SELECT senha, nome_docente, matricula_docente, email_docente FROM docente WHERE cpf = '{login_digitado}'")
                dados = cur.fetchall()

                global docente
                docente = Docente(dados[0][0], dados[0][1], dados[0][2], dados[0][3])


                if docente.senha == password_digitado:
                    conectar.close()
                    return sistema_docente_aviso()

                else:
                    conectar.close()
                    return render_template('login.html', login_digitado="Login/Senha incorretos!")

            return render_template('login.html', login_digitado="Login/Senha incorretos!")

        else:
            return render_template('login.html', login_digitado="Escolha uma opção!" )

    return render_template('login.html')


@app.route('/aluno_html/aviso')
def sistema_aluno_aviso():
    return render_template("/aluno_html/sistema_aluno_aviso.html", aluno = aluno.nome_completo, matricula = aluno.matricula, curso = aluno.curso,
                           semestre = aluno.semestre, email = aluno.email, status = aluno.status)

@app.route('/aluno_html/avaliacao')
def sistema_aluno_avaliacao():
    conectar, cur = conectar_bd("unichristus")

    lista_disciplinas = pegar_lista_disciplinas(cur)
    lista_disciplinas_json = json.dumps(lista_disciplinas)

    notas_disciplinas = pegar_notas_disciplinas(cur, lista_disciplinas)
    notas_disciplinas_json = json.dumps(notas_disciplinas)


    return render_template("/aluno_html/sistema_aluno_avaliacao.html", aluno=aluno.nome_completo, matricula=aluno.matricula,
                           curso=aluno.curso, semestre=aluno.semestre, email=aluno.email, status=aluno.status,
                           lista_disciplinas = lista_disciplinas_json, notas_disciplinas = notas_disciplinas_json, teste = notas_disciplinas)

@app.route('/aluno_html/financeiro')
def sistema_aluno_financeiro():
    return render_template("/aluno_html/sistema_aluno_financeiro.html", aluno = aluno.nome_completo, matricula = aluno.matricula, curso = aluno.curso,
                           semestre = aluno.semestre, email = aluno.email, status = aluno.status)

@app.route('/aluno_html/avaliacao_institucional')
def sistema_aluno_avaliacao_institucional():
    return render_template("/aluno_html/sistema_aluno_avaliacao_institucional.html", aluno = aluno.nome_completo, matricula = aluno.matricula, curso = aluno.curso,
                           semestre = aluno.semestre, email = aluno.email, status = aluno.status)



@app.route('/aluno_html/mudar_senha', methods=['GET', 'POST'])
def sistema_aluno_mudar_senha():

    if request.method == 'POST':
        senha_atual = request.form['senha-atual']
        nova_senha = request.form['nova-senha']
        confirme_senha = request.form['confirme-senha']


        if senha_atual == aluno.senha:
            if len(nova_senha) > 7 and len(nova_senha) < 20:
                if nova_senha == confirme_senha:
                    conectar, cur = conectar_bd("unichristus")
                    cur.execute(f"UPDATE aluno SET senha = '{nova_senha}' WHERE cpf = '{login_digitado}'")
                    conectar.commit()
                    cur.close()
                    conectar.close()

                    return render_template("/aluno_html/sistema_aluno_mudar_senha.html", msg_success="Senha alterada com sucesso!", aluno = aluno.nome_completo, matricula = aluno.matricula, curso = aluno.curso,
                               semestre = aluno.semestre, email = aluno.email, status = aluno.status)
                else:
                    return render_template("/aluno_html/sistema_aluno_mudar_senha.html",
                                           msg_error="As senhas precisam ser iguais!", aluno=aluno.nome_completo,
                                           matricula=aluno.matricula, curso=aluno.curso,
                                           semestre=aluno.semestre, email=aluno.email, status=aluno.status)
            else:
                return render_template("/aluno_html/sistema_aluno_mudar_senha.html",
                                       msg_error="A nova senha deve ter entre 8 e 20 caracteres!",
                                       aluno=aluno.nome_completo, matricula=aluno.matricula, curso=aluno.curso,
                                       semestre=aluno.semestre, email=aluno.email, status=aluno.status)

        else:
            return render_template("/aluno_html/sistema_aluno_mudar_senha.html", msg_error="Senha atual incorreta!", aluno = aluno.nome_completo, matricula = aluno.matricula, curso = aluno.curso,
                           semestre = aluno.semestre, email = aluno.email, status = aluno.status)

    return render_template("/aluno_html/sistema_aluno_mudar_senha.html", aluno = aluno.nome_completo, matricula = aluno.matricula, curso = aluno.curso,
                           semestre = aluno.semestre, email = aluno.email, status = aluno.status)




#sistema professor:

@app.route('/docente_html/sistema_docente_aviso')
def sistema_docente_aviso():
    return render_template("/docente_html/sistema_docente_aviso.html", docente = docente.nome_docente, matricula = docente.matricula_docente,
                           email = docente.email)


@app.route('/docente_html/sistema_docente_turmas')
def sistema_docente_turmas():

    conectar, cur = conectar_bd("unichristus")

    lista_disciplinas_docente = pegar_lista_disciplinas_docente(cur)
    lista_disciplinas_docente_json = json.dumps(lista_disciplinas_docente)

    lista_codigo_turmas_docente_e_nomes = pegar_codigos_turmas_docente_e_nome_disciplina(cur)

    lista_alunos_cada_disciplina = pegar_lista_aluno_cada_disciplina(cur, lista_codigo_turmas_docente_e_nomes)
    lista_alunos_cada_disciplina_json = json.dumps(lista_alunos_cada_disciplina)


    return render_template("/docente_html/sistema_docente_turmas.html",
                           lista_disciplinas_docente = lista_disciplinas_docente_json,
                           lista_alunos_cada_disciplina = lista_alunos_cada_disciplina_json, docente = docente.nome_docente,
                           matricula = docente.matricula_docente, email = docente.email)


@app.route('/docente_html/sistema_docente_financeiro')
def sistema_docente_financeiro():
    return render_template("/docente_html/sistema_docente_financeiro.html", docente = docente.nome_docente, matricula = docente.matricula_docente,
                           email = docente.email)

@app.route('/docente_html/sistema_docente_avaliacao_institucional')
def sistema_docente_avaliacao_institucional():
    return render_template("/docente_html/sistema_docente_avaliacao_institucional.html", docente = docente.nome_docente, matricula = docente.matricula_docente,
                           email = docente.email)

@app.route('/docente_html/sistema_docente_mudar_senha', methods=['GET', 'POST'])
def sistema_docente_mudar_senha():

    if request.method == 'POST':
        senha_atual = request.form['senha-atual']
        nova_senha = request.form['nova-senha']
        confirme_senha = request.form['confirme-senha']


        if senha_atual == docente.senha:
            if len(nova_senha) > 7 and len(nova_senha) < 20:
                if nova_senha == confirme_senha:
                    conectar, cur = conectar_bd("unichristus")
                    cur.execute(f"UPDATE docente SET senha = '{nova_senha}' WHERE cpf = '{login_digitado}'")
                    conectar.commit()
                    cur.close()
                    conectar.close()

                    return render_template("/docente_html/sistema_docente_mudar_senha.html", msg_success="Senha alterada com sucesso!", docente=docente.nome_docente,
                                           matricula=docente.matricula_docente,
                                           email=docente.email)
                else:
                    return render_template("/docente_html/sistema_docente_mudar_senha.html",
                                           msg_error="As senhas precisam ser iguais!", docente=docente.nome_docente,
                                           matricula=docente.matricula_docente,
                                           email=docente.email)
            else:
                return render_template("/docente_html/sistema_docente_mudar_senha.html",
                                       msg_error="A nova senha deve ter entre 8 e 20 caracteres!",
                                       docente=docente.nome_docente,
                                       matricula=docente.matricula_docente,
                                       email=docente.email)

        else:
            return render_template("/docente_html/sistema_docente_mudar_senha.html", msg_error="Senha atual incorreta!", docente=docente.nome_docente,
                                   matricula=docente.matricula_docente,
                                   email=docente.email)

    return render_template("/docente_html/sistema_docente_mudar_senha.html", docente=docente.nome_docente,
                           matricula=docente.matricula_docente,
                           email=docente.email)







@app.route ('/receber_notas_alunos_do_arquivo_js', methods = ['POST'])
def receber_notas_alunos_do_arquivo_js():
    dados_dos_alunos = request.json
    array_np1 = dados_dos_alunos['array_np1']
    array_np2 = dados_dos_alunos['array_np2']
    array_np3 = dados_dos_alunos['array_np3']
    array_id_notas = dados_dos_alunos['array_id_notas']

    conectar, cur = conectar_bd("unichristus")
    atualizar_notas_banco_de_dados(conectar, cur, array_np1, array_np2, array_np3, array_id_notas)
    conectar.close()

    return jsonify({"success": True, "resultado": [array_np1, array_np2, array_np3, array_id_notas]})










if __name__ == '__main__':
    app.run(debug=True)

