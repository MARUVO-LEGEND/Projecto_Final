import os
from unidecode import unidecode
from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineRightIconListItem
from kivymd.uix.list import IconRightWidget
# Importaçãos de Aplicção Externa
import mysql.connector
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from screens.screenmanager import MainScreenManager


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# main app class for kaki app with kivymd modules
class LiveApp(MDApp, App):
    """ Hi Windows users """

    DEBUG = 1  # set this to 0 make live app not working

    # *.kv files to watch
    KV_FILES = {
        os.path.join(os.getcwd(), "screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "screens/login/loginscreen.kv"),
        os.path.join(os.getcwd(), "screens/loading/loadingscreen.kv"),
        os.path.join(os.getcwd(), "screens/monitorament/monitoramentscreen.kv"),
        os.path.join(os.getcwd(), "screens/secretaria/choicescreen.kv"),
        os.path.join(os.getcwd(), "screens/secretaria/signinscreen.kv"),
        os.path.join(os.getcwd(), "screens/secretaria/usersinformationscreen.kv"),
        os.path.join(os.getcwd(), "screens/aboutapp/aboutappscreen.kv"),
        os.path.join(os.getcwd(), "screens/monitorament/schoolmonitoramentscreen.kv"),
        os.path.join(os.getcwd(), "screens/admin/adminscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configloginscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configsigninscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configmonitoramentscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configusersinformationscreen.kv"),
    }

    # class to watch from *.py files
    CLASSES = {
        "MainScreenManager": "screens.screenmanager",
        "LoginScreen": "screens.login.loginscreen",
        "LoadingScreen": "screens.loading.loadingscreen",
        "MonitoramentScreen": "screens.monitorament.monitoramentscreen",
        "AboutAppScreen": "screens.aboutapp.aboutappscreen",
        "UsersInformationScreen": "screens.secretaria.usersinformationscreen",
        "SignInScreen": "screens.secretaria.signinscreen",
        "ChoiceScreen": "screens.secretaria.choicescreen",
        "AdminScreen": "screens.admin.adminscreen",
        "SchoolMonitoramentScreen": "screens.monitorament.schoolmonitoramentscreen",
        "ConfigLoginScreen": "screens.configuration.configloginscreen",
        "ConfigMonitoramentScreen": "screens.configuration.configmonitoramentscreen",
        "ConfigSignInScreen": "screens.configuration.configsigninscreen",
        "ConfigUsersInformationScreen": "screens.configuration.configusersinformationscreen",

    }

    # auto reload path
    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def build_app(self):


        Window.size = (1200, 600)

        self.administradores=[]

        self.secretarios=[]


        self.monitores=[]


        self.porteiros=[]



        self.alunos=[]

        self.executatar_funcao_once=False


        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.material_style = "M3"
        self.primary_theme = self.theme_cls
        self.theme_cls.theme_style = "Dark"
        self.primary_theme.primary_palette = "LightBlue"
        self.primary_theme.primary_hue = "800"

        self.cp_on = False
        self.last_frame=None

        self.SM = MainScreenManager()

        return Factory.MainScreenManager()

    def theme_dark(self):

        self.theme_cls.primary_palette = (
            "Blue" if self.theme_cls.primary_palette == "LightBlue" else "LightBlue"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

        if self.theme_cls.primary_palette == "Blue":
            self.primary_theme.primary_hue = "600"
        else:
            self.theme_cls.primary_hue = "800"

    def theme_orange(self):
        self.theme_cls.primary_palette = "Orange"
        self.primary_theme.primary_hue = "600"

    def theme_blue(self):
        self.theme_cls.primary_palette = "Blue"
        self.primary_theme.primary_hue = "600"

    def theme_red(self):
        self.theme_cls.primary_palette = "Red"
        self.primary_theme.primary_hue = "900"


    def login_verification(self, root_manager, nome, senha):


        existence_user=[]

        for administrador in self.administradores:
            print(administrador["nome"])
            print(administrador["senha"])
            print(nome.text)
            print(senha.text)
            if administrador["nome"]==nome.text and administrador["senha"]==senha.text:
                user_exist=True
                existence_user.append(user_exist)

                Clock.schedule_once(lambda x: setattr(root_manager, "current", "AdminScreen"), 5)
            else:
                user_exist=False
                existence_user.append(user_exist)
                nome.error = True
                senha.error = True


        for secretario in self.secretarios:

            if secretario["nome"]==nome.text and secretario["senha"]==senha.text:
                user_exist=True
                existence_user.append(user_exist)
                Clock.schedule_once(lambda x: setattr(root_manager, "current", "ChoiceScreen"), 5)

            else:
                user_exist=False
                existence_user.append(user_exist)
                nome.error = True
                senha.error = True

        for monitor in self.monitores:

            if monitor["nome"]==nome.text and monitor["senha"]==senha.text:
                user_exist=True
                existence_user.append(user_exist)
                Clock.schedule_once(lambda x: setattr(root_manager, "current", "SchoolMonitoramentScreen"), 5)
            else:
                user_exist=False
                existence_user.append(user_exist)
                nome.error = True
                senha.error = True

        for porteiro in self.porteiros:

            if porteiro["nome"]==nome.text and porteiro["senha"]==senha.text:
                existence_user.append(True)
                Clock.schedule_once(lambda x: setattr(root_manager, "current", "MonitoramentScreen"), 5)
            else:
                existence_user.append(False)
                nome.error = True
                senha.error = True


        if True in existence_user:Clock.schedule_once(lambda x: Snackbar(text="Login Bem Sucedido", bg_color=(.5, .5, .5, 1)).open(), 1.5)
        else:
            Clock.schedule_once(lambda x: setattr(root_manager, "current", "LoginScreen"), 5)
            Clock.schedule_once(lambda x: Snackbar(text="Erro Ao Fazer Login", bg_color=(.5, .5, .5, 1)).open(), 1.5)
        return existence_user

    def on_login_button_click(self, root_manager, nome, senha):

        print(nome)
        print(senha)

        if self.connect_to_database():

            root_manager.current = "LoadingScreen"
            self.receive_users_from_bd(self.connect_to_database())
            if self.login_verification(root_manager,nome, senha)==False:
                Clock.schedule_once(lambda x: setattr(root_manager, "current", "LoginScreen"), 5)



        else:
                Clock.schedule_once(lambda x: Snackbar(text="Erro Ao Conectar No Servidor", bg_color=(.5, .5, .5, 1)).open(), 1.5)

    def start_capture(self, camera_image, button_cp):

        self.capture = cv2.VideoCapture(0)
        self.camera_image = camera_image

        self.cp_on=True if self.cp_on==False else self.cp_on==False
        self.button_cp = button_cp

        if self.cp_on==True:
            self.button_cp.text="Parar Captura"
            self.webcam=Clock.schedule_interval(self.update, 1.0 / 30.0)  # Atualiza a tela a cada 1/30 segundos

        else:
            self.button_cp.text="Iniciar Captura"
            self.webcam.cancel()

    def start_capture_sign(self, camera_image, button_cp):

        self.capture = cv2.VideoCapture(0)
        self.camera_image = camera_image

        self.cp_on=True if self.cp_on==False else self.cp_on==False
        self.button_cp = button_cp

        if self.cp_on==True:
            self.button_cp.text="Parar Captura"
            self.webcam=Clock.schedule_interval(self.update_sign, 1.0 / 30.0)  # Atualiza a tela a cada 1/30 segundos

        else:
            self.button_cp.text="Iniciar Captura"
            self.webcam.cancel()

    def save_last_frame(self, frame, nome, n_id_estudante):
        nome_formatado = nome.lower().replace(" ", "")
        print(nome_formatado)
        nome_formatado_sem_acentos=unidecode(nome_formatado)
        print(nome_formatado_sem_acentos)
        formatado = f"{nome_formatado_sem_acentos}{n_id_estudante}"
        print(formatado)
        caminho_absoluto = r"C:\Users\venic\Programation\PycharmProjects\Project Final Course\Projecto_Final\faces_alunos"
        caminho_completo = os.path.join(caminho_absoluto, f"{formatado}.jpg")
        cv2.imwrite(caminho_completo, frame)
        return formatado


    def sign_in_send(self,nome,n_id_escolar,n_id_turma,turma,nascimnto,turno):
        foto_caminho_save=self.save_last_frame(self.last_frame,nome,n_id_escolar)
        self.insert_user(self.connect_to_database(),nome,n_id_escolar,n_id_turma,turma,foto_caminho_save,nascimnto,turno)
        Clock.schedule_once(self.show_snackbar("Usuario Guardado com Sucesso"))

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Converte a imagem de BGR para RGB para exibição no Kivy
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.last_frame=frame_rgb


            # Atualiza a imagem na interface do usuário
            self.camera_image.texture = self.texture(frame_rgb)

    def update_sign(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Converte a imagem de BGR para RGB para exibição no Kivy
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.last_frame=frame
            faces = face_cascade.detectMultiScale(frame_rgb, scaleFactor=1.3, minNeighbors=5)

            # Atualiza a imagem na interface do usuário
            self.camera_image.texture = self.texture(frame_rgb)

    def texture(self, frame):
        # Converte a imagem OpenCV em um formato adequado para o Kivy
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        return texture

    def change_screen_right(self, screen_root, screen_name):
        self.root_manager = screen_root
        self.root_manager_transition = screen_root.transition
        self.root_manager_transition.direction = "left"
        self.root_manager.current = screen_name

    def change_screen_left(self, screen_root, screen_name):
        self.root_manager = screen_root
        self.root_manager_transition = screen_root.transition
        self.root_manager_transition.direction = "right"
        self.root_manager.current = screen_name

    def receive_users_from_bd(self,conn):
            try:
                cursor = conn.cursor()

                consulta_administradores = "SELECT * FROM administrador"
                cursor.execute(consulta_administradores)
                resultados_administradores = cursor.fetchall()

                for linha in resultados_administradores:

                    administrador={}
                    administrador["id"]=linha[0]
                    administrador["nome"]=linha[1]
                    administrador["senha"]=linha[2]
                    self.administradores.append(administrador)




                consulta_secretario = "SELECT * FROM secretario"
                cursor.execute(consulta_secretario)
                resultados_secretario = cursor.fetchall()
                contador=0

                for linha in resultados_secretario:


                    secretario={}

                    secretario["id"]=linha[0]
                    secretario["nome"]=linha[1]
                    secretario["senha"]=linha[2]
                    secretario["telefone"]=linha[3]
                    secretario["id_funcionario"]=linha[4]
                    self.secretarios.append(secretario)


                consulta_porteiro = "SELECT * FROM porteiro"
                cursor.execute(consulta_porteiro)
                resultados_porteiro = cursor.fetchall()

                for linha in resultados_porteiro:

                    porteiro={}
                    porteiro["id"]=linha[0]
                    porteiro["nome"]=linha[1]
                    porteiro["senha"]=linha[2]
                    porteiro["telefone"]=linha[3]
                    porteiro["id_funcionario"]=linha[4]
                    self.porteiros.append(porteiro)

                consulta_monitor = "SELECT * FROM monitor"
                cursor.execute(consulta_monitor)
                resultados_monitor = cursor.fetchall()

                for linha in resultados_monitor:
                    monitor={}
                    monitor["id"]=linha[0]
                    monitor["nome"]=linha[1]
                    monitor["senha"]=linha[2]
                    monitor["telefone"]=linha[3]
                    monitor["id_funcionario"]=linha[4]
                    self.monitores.append(monitor)

                consulta_alunos = "SELECT * FROM aluno"
                cursor.execute(consulta_alunos)
                resultados_alunos = cursor.fetchall()

                for linha in resultados_alunos:
                    aluno={}
                    aluno["id"]=linha[0]
                    aluno["nome"]=linha[1]
                    aluno["n_i_escolar"]=linha[2]
                    aluno["n_i_turma"]=linha[3]
                    aluno["foto_caminho"]=linha[4]
                    aluno["turma"]=linha[5]
                    aluno["nascimento"]=linha[6]
                    aluno["turno"]=linha[7]
                    self.alunos.append(aluno)




            except mysql.connector.Error as err:
                print(f"Erro ao inserir usuário: {err}")


    def show_snackbar(self, text):
        snackbar = Snackbar(text=text)
        snackbar.open()

    def connect_to_database(self):
        print("Conexão Iniciada")
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

    def insert_user(self, conn, nome,n_id_escolar,n_id_turma,turma,foto_caminho,nascimnto,turno):
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO aluno (nome,n_i_escolar,n_i_turma,foto_caminho,turma,nascimento,turno) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (nome,n_id_escolar,n_id_turma,foto_caminho,turma,nascimnto,turno))
            conn.commit()
            print("Usuário inserido com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir usuário: {err}")

    def teste(self):
        print("teste completo")

    def show_aluno_data(self,id,container_imagem,container_texto):

        for aluno in self.alunos:
            if aluno["id"]==id:

                nome=aluno["nome"]
                n_i_escolar=aluno["n_i_escolar"]
                n_i_turma=aluno["n_i_turma"]
                foto_caminho=aluno["foto_caminho"]
                turma=aluno["turma"]
                nascimento=aluno["nascimento"]
                turno=aluno["turno"]
                caminho_absoluto = r"C:\Users\venic\Programation\PycharmProjects\Project Final Course\Projecto_Final\faces_alunos"

                container_imagem.source=f"{caminho_absoluto}\{foto_caminho}.jpg"

                container_texto.value=f"Nome: {nome}\nNº-Escolar: {n_i_escolar}\nNº-Turma: {n_i_turma}\nTurma: {turma}\nNascimento: {nascimento}\nTurno: {turno}"

    def list_of_alunos(self,container,container_imagem,container_texto):
        if self.executatar_funcao_once==False:
            if self.connect_to_database():
                self.receive_users_from_bd(self.connect_to_database())
                print(self.alunos)
                for aluno in self.alunos:
                    id=aluno["id"]
                    receber_nome=aluno["nome"]
                    nome_convertido=receber_nome.split()
                    nome=f"{nome_convertido[0]} {nome_convertido[-1]}"
                    turma=aluno["turma"]
                    curso=""
                    curso_tipo=turma[:2]

                    if curso_tipo=="TI":
                        curso="Técnico Informático"

                    container.add_widget(
                        OneLineRightIconListItem(IconRightWidget(icon="information",on_release=setattr()),text=f"Nome:{nome}   Turma:{turma}    Curso:{curso}" ,width=100)
                    )


                self.executatar_funcao_once=True

            else:
                self.show_snackbar("Erro Ao Conectar Com O Servidor")
        else:
            pass



# finally, run the app
if __name__ == "__main__":
    LiveApp().run()
