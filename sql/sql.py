import mysql.connector


Nomes=[]

class Connection():

    def Cadastro(self,nome,n_id,turma):


        comando = f'insert into aluno (nome, n_i_escolar, turma) values ("{nome}", "{n_id}", "{turma}")'
        self.cursor.execute(comando)
        self.conexao.commit()
        print("Aluno registado!")
        self.cursor.close()
        self.conexao.close()

    def connect_to_database(self):
        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="magna_db"
            )
            print("Conexão bem-sucedida!")
            return conn
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")
            return None

    def consult_admin(self,conn):
        try:
            cursor = conn.cursor()
            consulta_admin = "SELECT * FROM administrador"

            cursor.execute(consulta_admin)
            resultados_admin = cursor.fetchall()


            for linha in resultados_admin:
                print(linha)

            consulta_secre = "SELECT * FROM secretario"
            cursor.execute(consulta_secre)
            resultados_secre=cursor.fetchall()

            for linha in resultados_secre:
                print(linha)

        except mysql.connector.Error as err:
            print(f"Erro ao inserir usuário: {err}")



Connection().consult_admin(Connection().connect_to_database())


dict
