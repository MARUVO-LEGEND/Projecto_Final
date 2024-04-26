import os
import re
import shutil
import glob
import  PIL
import datetime
import numpy as np
import face_recognition
from unidecode import unidecode
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kaki.app import App
from kivy.factory import Factory
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
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

    DEBUG = 0  # set this to 0 make live app not working
    # *.kv files to watch
    KV_FILES = {
        os.path.join(os.getcwd(), "screens/screenmanager.kv"),
        os.path.join(os.getcwd(), "screens/login/loginscreen.kv"),
        os.path.join(os.getcwd(), "screens/loading/loadingscreen.kv"),
        os.path.join(os.getcwd(), "screens/monitorament/doormonitoramentscreen.kv"),
        os.path.join(os.getcwd(), "screens/secretaria/choicescreen.kv"),
        os.path.join(os.getcwd(), "screens/secretaria/signinscreen.kv"),
        os.path.join(os.getcwd(), "screens/secretaria/usersinformationscreen.kv"),
        os.path.join(os.getcwd(), "screens/aboutapp/aboutappscreen.kv"),
        os.path.join(os.getcwd(), "screens/monitorament/schoolmonitoramentscreen.kv"),
        os.path.join(os.getcwd(), "screens/admin/adminscreen.kv"),
        os.path.join(os.getcwd(), "screens/admin/editfuncionarioinformationscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configloginscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configsigninscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configdoormonitoramentscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configusersinformationscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configedituserinformationscreen.kv"),
        os.path.join(os.getcwd(), "screens/configuration/configschoolmoniotarmentscreen.kv"),
        os.path.join(os.getcwd(), "screens/secretaria/edituserinformationscreen.kv"),
    }
    # class to watch from *.py files
    CLASSES = {
        "MainScreenManager": "screens.screenmanager",
        "LoginScreen": "screens.login.loginscreen",
        "LoadingScreen": "screens.loading.loadingscreen",
        "DoorMonitoramentScreen": "screens.monitorament.doormonitoramentscreen",
        "AboutAppScreen": "screens.aboutapp.aboutappscreen",
        "UsersInformationScreen": "screens.secretaria.usersinformationscreen",
        "SignInScreen": "screens.secretaria.signinscreen",
        "ChoiceScreen": "screens.secretaria.choicescreen",
        "AdminScreen": "screens.admin.adminscreen",
        "EditFuncionarioInformationScreen": "screens.admin.editfuncionarioinformationscreen",
        "SchoolMonitoramentScreen": "screens.monitorament.schoolmonitoramentscreen",
        "ConfigLoginScreen": "screens.configuration.configloginscreen",
        "ConfigDoorMonitoramentScreen": "screens.configuration.configdoormonitoramentscreen",
        "ConfigSchoolMonitoramentScreen": "screens.configuration.configschoolmonitoramentscreen",
        "ConfigSignInScreen": "screens.configuration.configsigninscreen",
        "ConfigUsersInformationScreen": "screens.configuration.configusersinformationscreen",
        "ConfigEditUserInformationScreen": "screens.configuration.configedituserinformationscreen",
        "EditUserInformationScreen": "screens.secretaria.edituserinformationscreen",

    }
    # auto reload path
    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def build_app(self):

        #CONFIGURAÇÕES PARA O KIVY E KIVYMD
        Window.size = (1200, 600)
        self.icon="images/favicon.png"
        self.title="MAGNA - Aplicação De Final de Curso "
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.material_style = "M3"
        self.primary_theme = self.theme_cls
        self.theme_cls.theme_style = "Dark"
        self.primary_theme.primary_palette = "Cyan"
        self.primary_theme.primary_hue = "800"

        # LISTA ONDE SERÃO GUARDADOS OS DADOS DOS USUARIOS VINDO DO BANCO DE DADOS
        self.administradores=[]
        self.secretarios=[]
        self.monitores=[]
        self.porteiros=[]
        self.alunos=[]

        # CAMINHO DAS IMAGENS DA FACE DOS ALUNOS
        self.caminho_imagem_faces_alunos=r"C:\Users\venic\Programation\PycharmProjects\Project Final Course\Projecto_Final\faces_alunos"
        self.caminho_imagem_faces_aluno_gray=""
        self.caminho_imagem_faces_alunos_colored=""

        #VARIAVEIS ONDE SERÃO ARMAZENADAS OS TEXTFIELD DA SCREEN EDITUSERINFORMATIONSCREEN
        self.Nome_edit=None
        self.Nascimento_edit=None
        self.Turno_edit=None
        self.Turma_edit=None
        self.N_id_escolar=None
        self.N_id_turma=None
        self.Propina_edit=None

        #VARIAVEIS ONDE SERÃO ARMAZENADAS OS TEXTFIELD DA SCREEN ADMINSCREEN
        self.Nome_edit_adm=None
        self.Telefone_edit_adm=None
        self.Senha_edit_adm=None
        self.Id_funcionario_edit_adm=None

        self.camera_image_capture=None
        self.button_cp_capture=None
        self.label_nome_h1_capture=None
        self.label_curso_h1_capture=None
        self.nome_aluno_capture=None
        self.turma_aluno_capture=None
        self.classe_aluno_capture=None
        self.n_i_turma_aluno=None
        self.permicao_entrada=None
        self.image_aluno=None

        #VARIAVEIS PARA AUXILIAR NO CODIGO
        #bool que ira informar se a função list_of_alunos já foi executada uma vez
        self.executatar_funcao_once=False
        self.executatar_funcao_once_adm=False

        #
        self.edit_image=False
        # variavel que ira armazenar o valor da linea clicada na função on_row_press
        self.id_edit_user=""
        #bool que irá defenir se o botão "iniciar captura" do screen signinscreen foi clicado
        self.cp_on = False
        #armazena o ultimo frame capturado
        self.last_frame=[None]
        self.save_dataset_frames_colored=[]
        self.save_dataset_frames_gray=[]

        self.root_managerr=None

        self.função_adm=""

        self.executar_verificador_once=False
        self.executar_verificador=False
        self.executar_verificador_n=1

        self.tipo_tema = 0 # dark==0 | light=1
        self.theme_cyan_color_0=(202/255,223/255,203/255,1)
        self.theme_cyan_color_1=(28/255,80/255,82/255,1)
        self.theme_cyan_color_2=(33/255,54/255,53/255,1)
        self.theme_cyan_color_3=(10/255,12/255,13/255,1)
        self.função_sign_in=""

        self.number_frames_captured_dataset=0
        self.is_capturing_dataset=False
        self.is_capturing_profile=False

        self.faces=[]
        self.ids=[]
        return Factory.MainScreenManager()

    #  TEMA DA APP
    def theme_change(self, icon):


        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            self.tipo_tema = 0

        elif self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
            self.tipo_tema = 1

        icon.theme_text_color = "Custom"
        icon.md_bg_color = [0.1, 0.1, 0.1, 1] if icon.md_bg_color == [.9, .9, .9, 1] else [.9, .9, .9, 1]
        icon.text_color = [0.1, 0.1, 0.1, 1] if icon.text_color == [.9, .9, .9, 1] else [.9, .9, .9, 1]

    def verificador_tema_label(self, label):
        print(self.tipo_tema)
        label.theme_text_color = "Custom"
        if self.tipo_tema == 1:
            print("exe")
            label.text_color = (0, 0, 0, 1)
        elif self.tipo_tema == 0:
            print("exe")
            label.text_color = (1, 1, 1, 1)
    def verificador_tema_bg(self,fundo1,fundo2):
        print(self.tipo_tema)
        if self.tipo_tema == 0:
            print("tema preto")
            print(fundo2)
            fundo1.md_bg_color =(.1,.1,.1,1)
            fundo2.md_bg_color = self.theme_cyan_color_2

        elif self.tipo_tema == 1:
            print("tema branco")
            fundo1.md_bg_color = (1,1,1,1)
            fundo2.md_bg_color = (1,1,1,1)
    def theme_orange(self):
        self.theme_cls.primary_palette    = "Orange"
        self.primary_theme.primary_hue = "800"
    def theme_blue(self):
        self.theme_cls.primary_palette = "Cyan"
        self.primary_theme.primary_hue = "800"
    def theme_red(self):
        self.theme_cls.primary_palette = "Red"
        self.primary_theme.primary_hue = "800"
    # FUNÇÕES PARA ABRIR UM MENU DE OPÇÕES
    def open_menu_adm(self,container_dropdown,container_text):

        função=["Secretaria","Portaria","Monitoração"]
        menu_items = [
            {
                "text": f"{função[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{função[i]}":self.menu_callback_adm(x,menu,container_text),
            } for i in range(3)
        ]
        menu = MDDropdownMenu(
            caller=container_dropdown,
            ver_growth="up",
            radius=[20, 20, 20, 20],
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    def open_menu_signin(self,container_dropdown,text):


        função=["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
        menu_items = [
            {
                "text": f"{função[i]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{função[i]}":self.menu_callback_signin(x,menu,text),
            } for i in range(12)
        ]
        menu = MDDropdownMenu(
            caller=container_dropdown,
            ver_growth="up",
            radius=[20, 20, 20, 20],
            items=menu_items,
            width_mult=4,
        )
        menu.open()
    def menu_callback_adm(self, text_item,menu,c_text):
        menu.dismiss()
        c_text.text=f"{text_item}"
        print(text_item)
        self.função_sign_in = text_item
    def menu_callback_signin(self,text_item,menu,c_text):
        menu.dismiss()
        c_text.text = f"{text_item}"
        c_text.text_color="gray"
        print(c_text)
        self.sign_in_month_user = text_item

    # FUNÇÕES PARA INICIAR A CAPTURA FRAMES

    def create_path_aluno(self, nome, n_id_estudante):
        nome_formatado = nome.lower().replace(" ", "")
        nome_formatado_sem_acentos = unidecode(nome_formatado)
        formatado = f"{nome_formatado_sem_acentos}{n_id_estudante}"
        caminho_absoluto = self.caminho_imagem_faces_alunos
        caminho_completo = os.path.join(caminho_absoluto, f"{formatado}")
        os.makedirs(caminho_completo)
        caminho_gray_aluno=os.path.join(caminho_completo,f"gray")
        caminho_colored_aluno=os.path.join(caminho_completo,f"profile")
        return caminho_completo,caminho_gray_aluno,caminho_colored_aluno,formatado
    def start_capture_sign_in_dataset(self,camera_image, button_cp):


        self.capture = cv2.VideoCapture(0)
        self.camera_image = camera_image
        self.is_capturing_dataset = True

        self.cp_on=True if self.cp_on==False else self.cp_on==False
        self.button_cp = button_cp

        if self.cp_on==True:
            self.button_cp.text="Parar Captura"
            self.webcam=Clock.schedule_interval(self.update_sign_in_dataset, 1.0 / 30.0)  # Atualiza a tela a cada 1/30 segundos



        else:
            self.button_cp.text="Iniciar Captura"
            self.webcam.cancel()
    def start_capture(self, camera_image, button_cp,label_nome_h1,label_curso_h1,nome_aluno,turma_aluno,classe_aluno,n_i_turma_aluno,permicao_entrada,image_aluno):
        LiveApp.show_snackbar(self, "Carregando...")

        self.camera_image_capture=camera_image
        self.button_cp_capture=button_cp
        self.label_nome_h1_capture=label_nome_h1
        self.label_curso_h1_capture=label_curso_h1
        self.nome_aluno_capture=nome_aluno
        self.turma_aluno_capture=turma_aluno
        self.classe_aluno_capture=classe_aluno
        self.n_i_turma_aluno=n_i_turma_aluno
        self.permicao_entrada=permicao_entrada
        self.image_aluno=image_aluno

        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.cap = cv2.VideoCapture(0)
        self.clf = cv2.face.LBPHFaceRecognizer_create()
        self.clf.read("classifier.xml")

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
            self.button_cp.text="Parar Captura Perfil"
            self.webcam=Clock.schedule_interval(self.update_sign, 1.0 / 30.0)  # Atualiza a tela a cada 1/30 segundos
            self.is_capturing_profile=True
        else:
            self.button_cp.text="Iniciar Captura Prefil"
            self.webcam.cancel()
    def start_capture_edit(self, camera_image, button_cp):

        self.capture = cv2.VideoCapture(0)
        self.camera_image = camera_image

        self.cp_on=True if self.cp_on==False else self.cp_on==False
        self.button_cp = button_cp

        if self.cp_on==True:
            self.button_cp.text="Parar Captura"
            self.webcam=Clock.schedule_interval(self.update_edit, 1.0 / 30.0)  # Atualiza a tela a cada 1/30 segundos

        else:
            self.button_cp.text="Iniciar Captura"
            self.webcam.cancel()
    def save_last_frame(self, frame, nome, n_id_estudante):
        nome_formatado = nome.lower().replace(" ", "")
        nome_formatado_sem_acentos=unidecode(nome_formatado)
        formatado = f"{nome_formatado_sem_acentos}{n_id_estudante}"
        caminho_absoluto = self.caminho_imagem_faces_alunos
        caminho_completo = os.path.join(caminho_absoluto, f"{formatado}.jpg")
        cv2.imwrite(caminho_completo, frame)
        return formatado

    def recognize(self,img, clf, faceCascade):
        self.draw_boundary(img, faceCascade, scaleFactor=1.1, minNeighbors=5, color=(255, 255, 255), text="Face", clf=clf)
        return img
    def update(self, dt):
        ret, frame = self.capture.read()

        if ret:
            # Detect Faces
            frame_fr = self.recognize(frame, self.clf, self.faceCascade)

            # Converte a imagem de BGR para RGB para exibição no Kivy
            frame_rgb=cv2.cvtColor(frame_fr,cv2.COLOR_BGR2RGB)
            # Atualiza a imagem na interface do usuário0
            self.camera_image.texture = self.texture(frame_rgb)

    def draw_boundary(self,img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray, scaleFactor, minNeighbors)

        for (x, y, w, h) in features:
            # Aumentar a região capturada para incluir o queixo e parte do pescoço
            y -= int(0.1 * h)
            h += int(0.3 * h)

            # Desenhar retângulo ao redor do rosto detectado
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

            # Realizar o reconhecimento facial
            id, pred = clf.predict(gray[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            # Exibir o nome do usuário se a confiança for alta o suficiente
            if confidence > 77:
                name ="Reconhecendo..."

                for aluno in self.alunos:
                    if str(id) in aluno["n_i_escolar"]:

                        name=f"{aluno['nome']}"
                        self.label_nome_h1_capture.text = f"{self.converter_nome_p_u(aluno['nome'])}"
                        self.label_curso_h1_capture.text = f"{self.curso_conversor(aluno['turma'])}"
                        self.nome_aluno_capture.text = f"Nome                  {aluno['nome']}"
                        self.turma_aluno_capture.text = f"Turma                 {aluno['turma']}"
                        self.classe_aluno_capture.text = f"Classe                    {self.classe_aluno(aluno['turma'])}"
                        self.n_i_turma_aluno.text = f"Nº                           {aluno['n_i_turma']}"
                        self.permicao_entrada.text = f"Permição                           {self.autorizador_entrada(aluno['mes_propina_paga'])}"
                        self.image_aluno.source = os.path.join(self.caminho_imagem_faces_alunos,str(aluno["foto_caminho"]),"profile","frame_1.jpg")

                cv2.putText(img, name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            else:
                cv2.putText(img, "UNKNOWN", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
    def update_sign(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Converte a imagem de BGR para RGB para exibição no Kivy
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.last_frame=frame
            faces = face_cascade.detectMultiScale(frame_rgb, scaleFactor=1.3, minNeighbors=5)

            # Atualiza a imagem na interface do usuário
            self.camera_image.texture = self.texture(frame_rgb)

    def train_classifier(self,data_dir):
        # Lista todos os arquivos no diretório de dados
        faces = self.faces
        ids = self.ids
        pasta_principal=self.caminho_imagem_faces_alunos

        for path_alunos in os.listdir(pasta_principal):
            print(path_alunos)
            for path_aluno in os.listdir(os.path.join(pasta_principal, path_alunos)):
                if path_aluno == "gray":
                    for image in os.listdir(os.path.join(pasta_principal, path_alunos, path_aluno)):

                        image_dir=os.path.join(pasta_principal, path_alunos, path_aluno,image)
                        # Abre a imagem e converte para escala de cinza
                        img = cv2.imread(image_dir, cv2.IMREAD_GRAYSCALE)

                        # Extrai o ID do usuário da imagem
                        id_aluno,nome=self.separar_numeros_letras(path_alunos)
                        print(id_aluno)
                        id =int(id_aluno)


                        # Armazena o rosto e o ID correspondente nas listas
                        faces.append(img)
                        ids.append(id)

        print(faces)
        print(ids)
        # Converte as listas em arrays numpy
        faces = np.array(faces, dtype=np.uint8)
        ids = np.array(ids)

        # Inicializa o classificador LBPH
        clf = cv2.face.LBPHFaceRecognizer_create()

        # Treina o classificador com os dados de treinamento
        clf.train(faces, ids)

        # Salva o modelo treinado em um arquivo XML
        clf.save("classifier.xml")

        print("Training completed successfully.")
    def update_sign_in_dataset(self,dt):
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        def face_cropped(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                # Calcular a ampliação vertical da região capturada
                y_start = max(0, y - int(0.1 * h))
                y_end = min(y + int(1.1 * h), img.shape[0])

                # Manter a mesma largura da região capturada
                x_start = x
                x_end = x + w

                # Capturar a região do rosto
                cropped_face = img[y_start:y_end, x_start:x_end]
                return cropped_face

        cap = self.capture
        ret, frame = cap.read()
        if face_cropped(frame) is not None:
            self.number_frames_captured_dataset+=1
            face = cv2.resize(face_cropped(frame), (200, 200))

            gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            colored_face=cv2.cvtColor(face,cv2.COLOR_BGR2RGB)

            self.save_dataset_frames_gray.append(gray_face)
            # Exibir o ID da imagem na janela
            cv2.putText(colored_face, str(self.number_frames_captured_dataset), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            self.camera_image.texture = self.texture(colored_face)

    def update_edit(self, dt):
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


    # FUNÇÕES DA TELA ADMIN SCREEN
    def update_funcionario_adm(self,conn,nome,senha,telefone,n_id):
        id_convert=self.id_edit_user.split(" ")

        if self.função_adm=="Secretaria":
            id = int(id_convert[1])
            try:
                cursor = conn.cursor()
                sql = f'UPDATE secretario set nome="{str(nome)}",id_funcionario={int(n_id)},senha={str(senha)},telefone="{str(telefone)}" where id_secretario={id}'
                cursor.execute(sql)
                conn.commit()
                self.show_snackbar("Usuario Editado Com Sucesso!")
                print("Usuário atualizados com sucesso!")
                self.update_row_datatable_adm()
                self.change_screen_left(self.root_manager,"AdminScreen")
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar usuário: {err}")
        if self.função_adm=="Portaria":
            id = int(id_convert[1])
            try:
                cursor = conn.cursor()
                sql = f'UPDATE porteiro set nome="{str(nome)}",id_funcionario={int(n_id)},senha={str(senha)},telefone="{str(telefone)}" where id_porteiro={id}'
                cursor.execute(sql)
                conn.commit()
                self.show_snackbar("Usuario Editado Com Sucesso!")
                print("Usuário atualizados com sucesso!")
                self.update_row_datatable_adm()
                self.change_screen_left(self.root_manager,"AdminScreen")
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar usuário: {err}")

        if self.função_adm=="Monitoração":
            id = int(id_convert[1])
            try:
                cursor = conn.cursor()
                sql = f'UPDATE monitor set nome="{str(nome)}",senha="{str(senha)}",telefone="{str(telefone)}",id_funcionario={int(n_id)} where id_monitor={id}'
                cursor.execute(sql)
                conn.commit()
                self.show_snackbar("Usuario Editado Com Sucesso!")
                print("Usuário atualizados com sucesso!")
                self.update_row_datatable_adm()
                self.change_screen_left(self.root_manager,"AdminScreen")
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar usuário: {err}")
    def user_edit_send_adm(self,nome,senha,telefone,n_id):
        if nome!=""or senha!=""or telefone!="" or n_id!="":
            self.update_funcionario_adm(self.connect_to_database(),nome,senha,telefone,n_id)
        else:
            self.show_snackbar("Termine de Colocar os Dados")
    def update_row_datatable_adm(self):

        self.administradores.clear()
        self.secretarios.clear()
        self.monitores.clear()
        self.porteiros.clear()
        self.alunos.clear()


        for n in self.secretarios:
            if len(self.data_table_adm.row_data) > 0:
                self.data_table_adm.remove_row(self.data_table_adm.row_data[-1])
        for n in self.porteiros:
            if len(self.data_table_adm.row_data) > 0:
                self.data_table_adm.remove_row(self.data_table_adm.row_data[-1])
        for n in self.monitores:
            if len(self.data_table_adm.row_data) > 0:
                self.data_table_adm.remove_row(self.data_table_adm.row_data[-1])



        for funcionario in self.secretarios:
            id = funcionario["id"]
            receber_nome = funcionario["nome"]
            nome_convertido = receber_nome.split()
            nome = f"{nome_convertido[0]} {nome_convertido[-1]}"
            n_telefone = funcionario["telefone"]
            id_funcionario = funcionario["id_funcionario"]
            linha_funcionario = [" ", "Secretaria", ("information", [1, 1, 1, 1], f" {id}"), nome, n_telefone,
                                 id_funcionario]
            self.data_table_adm.row_data.append(linha_funcionario)
        for funcionario in self.porteiros:
            id = funcionario["id"]
            receber_nome = funcionario["nome"]
            nome_convertido = receber_nome.split()
            nome = f"{nome_convertido[0]} {nome_convertido[-1]}"
            n_telefone = funcionario["telefone"]
            id_funcionario = funcionario["id_funcionario"]
            linha_funcionario = [" ", "Portaria", ("information", [1, 1, 1, 1], f" {id} "), nome, n_telefone,
                                 id_funcionario]
            self.data_table_adm.row_data.append(linha_funcionario)
        for funcionario in self.monitores:
            id = funcionario["id"]
            receber_nome = funcionario["nome"]
            nome_convertido = receber_nome.split()
            nome = f"{nome_convertido[0]} {nome_convertido[-1]}"
            n_telefone = funcionario["telefone"]
            id_funcionario = funcionario["id_funcionario"]
            linha_funcionario = [" ", "Monitorização", ("information", [1, 1, 1, 1], f" {id}  "), nome,
                                 n_telefone, id_funcionario]
            self.data_table_adm.row_data.append(linha_funcionario)
    def show_dialog_adm(self,id,função):

        # Criar um layout MDBoxLayout para conter os MDTextField
        layout = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Adicionar vários MDTextField ao layout
        for _ in range(20):  # Adicione quantos MDTextField você precisar
            textfield = MDTextField(hint_text="City")
            layout.add_widget(textfield)

        # Colocar o layout dentro de um ScrollView
        scrollview = MDScrollView()
        scrollview.add_widget(layout)

        self.dialog = MDDialog(
            title="Alterar Informações",
            type="custom",
            text="Deseja Editar ou Apagar Informções Sobre o Aluno?",
            buttons=[
                MDFlatButton(
                    text="FECHAR",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x:self.close_dialog()
                ),
                MDFlatButton(
                    text="EDITAR",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                     on_release=lambda x:self.edit_adm(id,função)
                ),

                MDFlatButton(
                    text="APAGAR",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x:self.delete_funcionario_adm(self.connect_to_database(),id,função),
                ),
            ],
        )

        self.dialog.open()
    def save_edit_widgets_adm(self,Nome,Senha,Telefone,N_id):


        self.Nome_edit_adm=Nome
        self.Senha_edit_adm=Senha
        self.Telefone_edit_adm=Telefone
        self.Id_funcionario_edit_adm=N_id
    def delete_funcionario_adm(self, conn, id,funçao):

        if funçao=="Secretaria":
            try:
                cursor = conn.cursor()

                # Exclui o aluno
                delete_sql = f'DELETE FROM secretario WHERE id_secretario="{int(id)}"'
                cursor.execute(delete_sql)
                conn.commit()
                print("Usuário Apagado com Sucesso!")
                # Atualiza os IDs na tabela (assumindo que a tabela correta é 'tabela')
                organize_sql = f"UPDATE secretario SET id_secretario = id_secretario - 1 WHERE id_secretario > {int(id)}"
                cursor.execute(organize_sql)
                conn.commit()
                print("Usuários Organizados com Sucesso!")
                # Atualiza a lista de alunos e a data_table
                self.secretarios.clear()
                self.receive_users_from_bd(self.connect_to_database())
                self.data_table_adm.remove_row(self.data_table_adm.row_data[int(id) - 1])
                # Mostra a mensagem de sucesso
                self.show_snackbar(f"Funcionario ({funçao}) Apagado com Sucesso!")

            except mysql.connector.Error as err:
                print(f"Erro ao Apagar Usuário: {err}")
            # Se ocorrer um erro durante a exclusão, você pode querer lidar com isso aqui

        if funçao=="Portaria":
            try:
                cursor = conn.cursor()

                # Exclui o aluno
                delete_sql = f'DELETE FROM porteiro WHERE id_porteiro="{int(id)}"'
                cursor.execute(delete_sql)
                conn.commit()
                print("Usuário Apagado com Sucesso!")
                # Atualiza os IDs na tabela (assumindo que a tabela correta é 'tabela')
                organize_sql = f"UPDATE porteiro SET id_porteiro = id_porteiro - 1 WHERE id_porteiro > {int(id)}"
                cursor.execute(organize_sql)
                conn.commit()
                print("Usuários Organizados com Sucesso!")
                # Atualiza a lista de alunos e a data_table
                self.secretarios.clear()
                self.receive_users_from_bd(self.connect_to_database())
                self.data_table_adm.remove_row(self.data_table_adm.row_data[int(id) - 1])
                # Mostra a mensagem de sucesso
                self.show_snackbar(f"Funcionario ({funçao}) Apagado com Sucesso!")

            except mysql.connector.Error as err:
                print(f"Erro ao Apagar Usuário: {err}")
            # Se ocorrer um erro durante a exclusão, você pode querer lidar com isso aqui

        if funçao=="Monitoração":
            try:
                cursor = conn.cursor()

                # Exclui o aluno
                delete_sql = f'DELETE FROM monitor WHERE id_monitor="{int(id)}"'
                cursor.execute(delete_sql)
                conn.commit()
                print("Usuário Apagado com Sucesso!")
                # Atualiza os IDs na tabela (assumindo que a tabela correta é 'tabela')
                organize_sql = f"UPDATE monitor SET id_monitor = id_monitor - 1 WHERE id_monitor > {int(id)}"
                cursor.execute(organize_sql)
                conn.commit()
                print("Usuários Organizados com Sucesso!")
                # Atualiza a lista de alunos e a data_table
                self.secretarios.clear()
                self.receive_users_from_bd(self.connect_to_database())
                self.data_table_adm.remove_row(self.data_table_adm.row_data[int(id) - 1])
                # Mostra a mensagem de sucesso
                self.show_snackbar(f"Funcionario ({funçao}) Apagado com Sucesso!")

            except mysql.connector.Error as err:
                print(f"Erro ao Apagar Usuário: {err}")
            # Se ocorrer um erro durante a exclusão, você pode querer lidar com isso aqui
    def on_row_press_adm(self, instance_table, instance_row):

        print(len(instance_row.text))
        self.id_edit_user = instance_row.text
        if len(instance_row.text)==2:
            self.show_dialog_adm(self.id_edit_user,"Secretaria")
            print("Executado")
        elif len(instance_row.text)==3:
            self.show_dialog_adm(self.id_edit_user,"Portaria")
            print("Executado")
        elif len(instance_row.text)==4:
            self.show_dialog_adm(self.id_edit_user,"Monitoração")
            print("Executado")
    def edit_adm(self,*args):
        print("entrou")

        for arg in args:
            self.edit_id_information=arg
            self.change_screen_right(self.root_managerr,"EditFuncionarioInformationScreen")
            if self.root_managerr.current=="EditFuncionarioInformationScreen":
                self.close_dialog()
                func_id=None
                if arg=="Secretaria":
                    for arg in args:
                        if arg!="Secretaria":

                            func_id=int(arg)
                            funcionario=self.secretarios[func_id-1]
                            self.Nome_edit_adm.text=f"{funcionario['nome']}"
                            self.Senha_edit_adm.text=f"{funcionario['senha']}"
                            self.Telefone_edit_adm.text=f"{funcionario['telefone']}"
                            self.Id_funcionario_edit_adm.text=f"{funcionario['id_funcionario']}"
                            self.função_adm="Secretaria"
                if arg=="Portaria":
                    for arg in args:
                        if arg!="Portaria":
                            func_id=int(arg)
                            funcionario=self.porteiros[func_id-1]
                            self.Nome_edit_adm.text=f"{funcionario['nome']}"
                            self.Senha_edit_adm.text=f"{funcionario['senha']}"
                            self.Telefone_edit_adm.text=f"{funcionario['telefone']}"
                            self.Id_funcionario_edit_adm.text=f"{funcionario['id_funcionario']}"
                            self.função_adm="Portaria"
                if arg=="Monitoração":
                    for arg in args:
                        if arg!="Monitoração":
                            func_id=int(arg)
                            funcionario=self.monitores[func_id-1]
                            self.Nome_edit_adm.text=f"{funcionario['nome']}"
                            self.Senha_edit_adm.text=f"{funcionario['senha']}"
                            self.Telefone_edit_adm.text=f"{funcionario['telefone']}"
                            self.Id_funcionario_edit_adm.text=f"{funcionario['id_funcionario']}"
                            self.função_adm="Monitoração"
    def on_row_press(self, instance_table, instance_row):
        self.id_edit_user = instance_row.text
        if instance_row.selected and len(instance_row.text)==3:
            self.show_dialog_aluno(self.id_edit_user)
    def list_of_funcionarios(self,container):
        self.container_list_funcionarios = container

        if self.executatar_funcao_once_adm == False:
            if self.connect_to_database():

                self.administradores.clear()
                self.secretarios.clear()
                self.monitores.clear()
                self.porteiros.clear()
                self.alunos.clear()

                self.receive_users_from_bd(self.connect_to_database())

                print(self.alunos)

                self.data_table_adm = MDDataTable(
                    size_hint=(0.9, 0.9),
                    column_data=[
                        ("", (5)),
                        ("Função",(50)),
                        ("id", (50)),
                        ("Nome", (50)),
                        ("Telefone", (50)),
                        ("Nº Funcionario", (50)),
                    ],
                )
                container.add_widget(self.data_table_adm)
                self.data_table_adm .bind(on_row_press=self.on_row_press_adm)

                for funcionario in self.secretarios:

                    id = funcionario["id"]
                    receber_nome = funcionario["nome"]
                    nome_convertido = receber_nome.split()
                    nome = f"{nome_convertido[0]} {nome_convertido[-1]}"
                    n_telefone = funcionario["telefone"]
                    id_funcionario = funcionario["id_funcionario"]
                    linha_funcionario = [" ","Secretaria", ("information", [1, 1, 1, 1], f" {id}"), nome, n_telefone, id_funcionario ]
                    self.data_table_adm.row_data.append(linha_funcionario)
                for funcionario in self.porteiros:

                    id = funcionario["id"]
                    receber_nome = funcionario["nome"]
                    nome_convertido = receber_nome.split()
                    nome = f"{nome_convertido[0]} {nome_convertido[-1]}"
                    n_telefone = funcionario["telefone"]
                    id_funcionario = funcionario["id_funcionario"]
                    linha_funcionario = [" ","Portaria" ,("information", [1, 1, 1, 1], f" {id} "), nome, n_telefone, id_funcionario ]
                    self.data_table_adm.row_data.append(linha_funcionario)
                for funcionario in self.monitores:

                    id = funcionario["id"]
                    receber_nome = funcionario["nome"]
                    nome_convertido = receber_nome.split()
                    nome = f"{nome_convertido[0]} {nome_convertido[-1]}"
                    n_telefone = funcionario["telefone"]
                    id_funcionario = funcionario["id_funcionario"]
                    linha_funcionario = [" ","Monitorização" ,("information", [1, 1, 1, 1], f" {id}  "), nome, n_telefone, id_funcionario ]
                    self.data_table_adm.row_data.append(linha_funcionario)

                self.executatar_funcao_once_adm = True
            else:
                self.show_snackbar("Erro Ao Conectar Com O Servidor")
        else:
            pass
    def verificador_de_animacao(self,root,container):
        print("executado")

        if  self.root_managerr=="AboutAppScreen":
            pass
        else :
            if self.executar_verificador==False:
                container.remove_widget(container.children[-1])
                self.executar_verificador= True
    def clean_textfield_adm(self,Nome, Senha, Telefone, N_id):
        Nome.text=""
        Senha.text=""
        Telefone.text=""
        N_id.text=""
    def sign_in_funcionario(self,Nome,Senha,Telefone,N_id,conn,funcao):
        if Nome and Senha and Telefone and N_id !="":
            if funcao == "Secretaria":
                try:
                    cursor = conn.cursor()
                    sql = "INSERT INTO secretario (nome,senha,telefone,id_funcionario) VALUES (%s,%s,%s,%s)"
                    cursor.execute(sql, (Nome, Senha, Telefone, N_id))
                    conn.commit()
                    print("Usuário inserido com sucesso!")
                    self.show_snackbar("Usuário inserido com sucesso!")
                except mysql.connector.Error as err:
                    print(f"Erro ao inserir usuário: {err}")
            if funcao == "Portaria":
                try:
                    cursor = conn.cursor()
                    sql = "INSERT INTO porteiro (nome,senha,telefone,id_funcionario) VALUES (%s,%s,%s,%s)"
                    cursor.execute(sql, (Nome, Senha, Telefone, N_id))
                    conn.commit()
                    print("Usuário inserido com sucesso!")
                    self.show_snackbar("Usuário inserido com sucesso!")
                except mysql.connector.Error as err:
                    print(f"Erro ao inserir usuário: {err}")
            if funcao == "Monitoração":
                try:
                    cursor = conn.cursor()
                    sql = "INSERT INTO monitor (nome,senha,telefone,id_funcionario) VALUES (%s,%s,%s,%s)"
                    cursor.execute(sql, (Nome, Senha, Telefone, N_id))
                    conn.commit()
                    print("Usuário inserido com sucesso!")
                    self.show_snackbar("Usuário inserido com sucesso!")
                except mysql.connector.Error as err:
                    print(f"Erro ao inserir usuário: {err}")
            else:
                self.show_snackbar("Coloque a Função do Funcionario Nas Opções")
        else:
            self.show_snackbar("Termine de  Inserir os Dados")
    def send_funcionrios(self,Nome,Senha,Telefone,N_id):
        self.sign_in_funcionario(Nome,Senha,Telefone,N_id,self.connect_to_database(),self.função_sign_in)

    # FUNÇÕES DA TELA SIGN IN SCREEN
    def insert_user(self, conn, nome,n_id_escolar,n_id_turma,turma,foto_caminho,nascimnto,turno,propina):
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO aluno (nome,n_i_escolar,n_i_turma,foto_caminho,turma,nascimento,turno,mes_propina_paga) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (nome,n_id_escolar,n_id_turma,foto_caminho,turma,nascimnto,turno,propina))
            conn.commit()
            print("Usuário inserido com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir usuário: {err}")
    def convert_nascimento_dd_to_yy(self,nascimento):
        converter_nascimento = str(nascimento).split("/")
        nascimento_convertido = f"{converter_nascimento[2]}/{converter_nascimento[1]}/{converter_nascimento[0]}"
        return nascimento_convertido
    def update_user(self,conn,nome,n_id_escolar,n_id_turmaa,turma,nascimento,turno,propina):

        nascimento_convertido=self.convert_nascimento_dd_to_yy(nascimento)
        id_convert=self.id_edit_user.split(" ")
        id=int(id_convert[-1])
        try:
            cursor = conn.cursor()
            sql = f'UPDATE aluno set nome="{str(nome)}",n_i_escolar={int(n_id_escolar)},n_i_turma={int(n_id_turmaa)},turma="{str(turma)}",nascimento="{str(nascimento_convertido)}",turno="{str(turno)}",mes_propina_paga="{str(propina)}" where id_aluno={id}'
            cursor.execute(sql)
            conn.commit()
            self.show_snackbar("Usuario Editado Com Sucesso!")
            print("Usuário atualizados com sucesso!")
            self.update_row_datatable()
            self.change_screen_left(self.root_manager,"EditUserInformationScreen")
        except mysql.connector.Error as err:
            print(f"Erro ao atualizar usuário: {err}")
    def user_edit_send(self,Nome,N_id_turma,N_id_estudante,Turma,Nascimento,Turno,Propina):
        if self.edit_image==True:
            pass
        self.update_user(self.connect_to_database(),Nome,N_id_turma,N_id_estudante,Turma,Nascimento,Turno,Propina)
    def save_edit_widgets(self,Nome,Nascimento,Turno,Turma,N_id_escolar,N_id_turma,container,Propina):

        self.Nome_edit=Nome

        self.Nascimento_edit=Nascimento
        self.Turno_edit=Turno
        self.Turma_edit=Turma
        self.N_id_escolar_edit=N_id_escolar
        self.N_id_turma_edit=N_id_turma
        self.Container_imagem_edit=container
        self.Propina_edit=Propina
    def delete_aluno_path(self,id):
        print(id)
        nome=self.alunos[int(id)-1]["nome"]
        id_esc=self.alunos[int(id)-1]["n_i_escolar"]

        nome_formatado=self.convert_name_to_path(nome,id_esc)


        caminho_absoluto = self.caminho_imagem_faces_alunos

        caminho_delete=os.path.join(caminho_absoluto,nome_formatado)
        print(caminho_delete)
        shutil.rmtree(caminho_delete)
    def delete_aluno(self, conn, id):

        print(id)
        try:
            cursor = conn.cursor()

            # Exclui imagem de identificação

            self.delete_aluno_path(id)


            # Exclui o aluno
            delete_sql = f'DELETE FROM aluno WHERE id_aluno="{int(id)}"'
            cursor.execute(delete_sql)
            conn.commit()
            print("Usuário Apagado com Sucesso!")

            # Atualiza os IDs na tabela (assumindo que a tabela correta é 'tabela')
            organize_sql = f"UPDATE aluno SET id_aluno = id_aluno - 1 WHERE id_aluno > {int(id)}"
            cursor.execute(organize_sql)
            conn.commit()
            print("Usuários Organizados com Sucesso!")

            # Atualiza a lista de alunos e a data_table
            self.alunos.clear()
            self.receive_users_from_bd(self.connect_to_database())
            self.data_table.remove_row(self.data_table.row_data[int(id) - 1])

            self.train_classifier(self.caminho_imagem_faces_alunos)

            # Mostra a mensagem de sucesso
            self.show_snackbar("Aluno Apagado com Sucesso!")

        except mysql.connector.Error as err:
            print(f"Erro ao Apagar Usuário: {err}")
            # Se ocorrer um erro durante a exclusão, você pode querer lidar com isso aqui
    def edit_aluno(self,*args):
        print("entrou")

        for arg in args:

            self.edit_id_information=arg
            self.change_screen_right(self.root_manager,"EditUserInformationScreen")
            if self.root_manager.current=="EditUserInformationScreen":
                self.close_dialog()
                aluno=self.alunos[int(arg)-1]
                self.Nome_edit.text=f"{aluno['nome']}"

                converter_nascimento = str(aluno["nascimento"]).split("-")
                nascimento = f"{converter_nascimento[2]}/{converter_nascimento[1]}/{converter_nascimento[0]}"

                self.Nascimento_edit.text=f"{nascimento}"
                self.Turno_edit.text=f"{aluno['turno']}"
                self.Turma_edit.text=f"{aluno['turma']}"
                self.N_id_turma_edit.text=f"{aluno['n_i_escolar']}"
                self.N_id_escolar_edit.text=f"{aluno['n_i_turma']}"
                self.Propina_edit.text=f"{aluno['mes_propina_paga']}"

                self.Container_imagem_edit.source=f"faces_alunos/{str(aluno['foto_caminho'])}.jpg"
    def convert_name_to_file(self,nome,id_esc):
        nome_formatado = nome.lower().replace(" ", "")
        nome_formatado_sem_acentos = unidecode(nome_formatado)
        formatado = f"{nome_formatado_sem_acentos}{id_esc}.jpg"
        return formatado
    def convert_name_to_path(self,nome,id_esc):
        nome_formatado = nome.lower().replace(" ", "")
        nome_formatado_sem_acentos = unidecode(nome_formatado)
        formatado = f"{nome_formatado_sem_acentos}{id_esc}"
        return formatado
    def sign_in_send(self,nome,n_id_escolar,n_id_turma,turma,nascimento,turno,propina):


        if nome and n_id_turma and n_id_escolar and turma and nascimento and turno !="" and propina!="Propina":

            if self.is_capturing_dataset==False:
                self.show_snackbar("Termine de Capturar os Frames de Treinamento !")

            elif self.is_capturing_profile==False:

                self.show_snackbar("Termine de Tirar Foto de Perfil !")

            else:
                caminho_completo,caminho_gray,caminho_profile,caminho_foto_aluno=self.create_path_aluno(nome, n_id_escolar)
                os.makedirs(caminho_gray)
                os.makedirs(caminho_profile)

                for i, frame in enumerate(self.save_dataset_frames_gray):
                    cv2.imwrite(os.path.join(caminho_gray, 'frame_{}.jpg'.format(i + 1)), frame)
                cv2.imwrite(os.path.join(caminho_profile, 'frame_{}.jpg'.format(1)), self.last_frame)


                self.save_dataset_frames_gray = [None]
                self.last_frame=[None]
                self.is_capturing_profile=False
                self.is_capturing_dataset=False

                converter_nascimento = str(nascimento).split("-")
                converter_nascimento2=converter_nascimento[0].replace("'","")
                converter_nascimento3=converter_nascimento2.split("/")
                nascimento_convertido = f"{converter_nascimento3[2]}/{converter_nascimento3[1]}/{converter_nascimento3[0]}"
                self.insert_user(self.connect_to_database(),nome,n_id_escolar,n_id_turma,turma,caminho_foto_aluno,nascimento_convertido,turno,propina)

                self.train_classifier(self.caminho_imagem_faces_alunos)

                self.show_snackbar("Usuario Guardado com Sucesso")


        else:
            self.show_snackbar("Termine de Colocar os Dados!")
    def clean_textfield(self,Nome,Nascimento,Turno,Turma,N_id_escolar,N_id_turma,Propina):
        Nome.text=""
        Nascimento.text=""
        Turno.text=""
        Turma.text=""
        N_id_escolar.text=""
        N_id_turma.text=""
        Propina.text="Propina"
        Propina.text_color="white"


    #FUNÇÕES DA TELA LOGIN SCREEN
    def login_verification(self, root_manager, nome, senha):

        existence_user=[]

        for administrador in self.administradores:

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
                user_exist=True
                existence_user.append(user_exist)
                Clock.schedule_once(lambda x: setattr(root_manager, "current", "DoorMonitoramentScreen"), 5)

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

        self.root_managerr=root_manager

        if self.connect_to_database():

            root_manager.current = "LoadingScreen"
            self.receive_users_from_bd(self.connect_to_database())
            if self.login_verification(root_manager,nome, senha)==False:
                Clock.schedule_once(lambda x: setattr(root_manager, "current", "LoginScreen"), 5)



        else:
                Clock.schedule_once(lambda x: Snackbar(text="Erro Ao Conectar No Servidor", bg_color=(.5, .5, .5, 1)).open(), 1.5)


    #FUNÇÕES DA TELA USER INFORMATION SCREEN
    def update_row_datatable(self):

        self.administradores.clear()
        self.secretarios.clear()
        self.monitores.clear()
        self.porteiros.clear()
        self.alunos.clear()

        self.receive_users_from_bd(self.connect_to_database())

        for n in self.alunos:
            if len(self.data_table.row_data) > 0:
                self.data_table.remove_row(self.data_table.row_data[-1])

        for aluno in self.alunos:

            id = aluno["id"]
            receber_nome = aluno["nome"]
            nome_convertido = receber_nome.split()
            nome = f"{nome_convertido[0]} {nome_convertido[-1]}"
            turma = aluno["turma"]
            id_turma = aluno["n_i_turma"]
            id_escola = aluno["n_i_escolar"]
            if aluno["nascimento"] != None:
                print(str(aluno["nascimento"]))
                nascimento_row = re.findall(r'\d+', str(aluno["nascimento"]))
                nascimento = f"{nascimento_row[2]}/{nascimento_row[1]}/{nascimento_row[0]}"
            curso = self.curso_conversor(aluno["turma"])
            turno = aluno["turno"]
            propina=aluno["mes_propina_paga"]


            linha_aluno = [" ", ("information", [1, 1, 1, 1], f"  {id}"), nome, turma, id_turma, id_escola, curso,
                           turno, nascimento,propina ]

            self.data_table.row_data.append(linha_aluno)
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
                caminho_absoluto = self.caminho_imagem_faces_alunos

                container_imagem.source=f"{caminho_absoluto}\{foto_caminho}.jpg"

                container_texto.value=f"Nome: {nome}\nNº-Escolar: {n_i_escolar}\nNº-Turma: {n_i_turma}\nTurma: {turma}\nNascimento: {nascimento}\nTurno: {turno}"
    def show_dialog_aluno(self,id):

        # Criar um layout MDBoxLayout para conter os MDTextField
        layout = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Adicionar vários MDTextField ao layout
        for _ in range(20):  # Adicione quantos MDTextField você precisar
            textfield = MDTextField(hint_text="City")
            layout.add_widget(textfield)

        # Colocar o layout dentro de um ScrollView
        scrollview = MDScrollView()
        scrollview.add_widget(layout)

        self.dialog = MDDialog(
            title="Alterar Informações",
            type="custom",
            text="Deseja Editar ou Apagar Informções Sobre o Aluno?",
            buttons=[
                MDFlatButton(
                    text="FECHAR",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x:self.close_dialog()
                ),
                MDFlatButton(
                    text="EDITAR",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                     on_release=lambda x:self.edit_aluno(id)
                ),

                MDFlatButton(
                    text="APAGAR",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x:self.delete_aluno(self.connect_to_database(),id),
                ),
            ],
        )

        self.dialog.open()
    def list_of_alunos(self,container):

        self.container_list_alunos=container

        if self.executatar_funcao_once==False:
            if self.connect_to_database():

                self.administradores.clear()
                self.secretarios.clear()
                self.monitores.clear()
                self.porteiros.clear()
                self.alunos.clear()

                self.receive_users_from_bd(self.connect_to_database())

                print(self.alunos)

                self.data_table=MDDataTable(
                    size_hint=(0.9, 0.9),

                    use_pagination=True,
                    column_data=[
                        ("", (5)),
                        ("id", (28)),
                        ("Nome", (28)),
                        ("Turma", (28)),
                        ("Nº Turma", (28)),
                        ("Nº Escolar", (28)),
                        ("Curso", (28)),
                        ("Turno", (28)),
                        ("Nascimento", (28)),
                        ("Propina", (28)),

                    ],
                )
                container.add_widget(self.data_table)
                self.data_table.bind(on_row_press=self.on_row_press)

                for aluno in self.alunos:

                    id=aluno["id"]
                    receber_nome=aluno["nome"]
                    nome_convertido=receber_nome.split()
                    nome=f"{nome_convertido[0]} {nome_convertido[-1]}"
                    turma=aluno["turma"]
                    id_turma=aluno["n_i_turma"]
                    id_escola=aluno["n_i_escolar"]
                    turno=aluno["turno"]
                    propina=aluno["mes_propina_paga"]
                    if aluno["nascimento"]!=None:
                        print(str(aluno["nascimento"]))
                        nascimento_row=re.findall(r'\d+',str(aluno["nascimento"]))
                        nascimento=f"{nascimento_row[2]}/{nascimento_row[1]}/{nascimento_row[0]}"
                    curso=self.curso_conversor(aluno["turma"])




                    linha_aluno=[" ",("information",[1,1,1,1],f"  {id}"),nome,turma,id_turma,id_escola,curso,turno,nascimento,propina]

                    self.data_table.row_data.append(linha_aluno)

                self.executatar_funcao_once=True

            else:
                self.show_snackbar("Erro Ao Conectar Com O Servidor")
        else:
            pass
    def search_aluno(self,search_container_text):
        text=search_container_text
        print("executado")
        self.receive_users_from_bd(self.connect_to_database())
        for aluno in self.alunos:
            if aluno["n_i_escolar"]==str(text):

                for n in self.alunos:
                    if len(self.data_table.row_data) > 0:
                        self.data_table.remove_row(self.data_table.row_data[-1])

                id = aluno["id"]
                receber_nome = aluno["nome"]
                nome_convertido = receber_nome.split()
                nome = f"{nome_convertido[0]} {nome_convertido[-1]}"
                turma = aluno["turma"]
                id_turma = aluno["n_i_turma"]
                id_escola = aluno["n_i_escolar"]
                turno=aluno["turno"]
                if aluno["nascimento"] != None:
                    print(str(aluno["nascimento"]))
                    nascimento_row = re.findall(r'\d+', str(aluno["nascimento"]))
                    nascimento = f"{nascimento_row[2]}/{nascimento_row[1]}/{nascimento_row[0]}"
                curso = self.curso_conversor(aluno["turma"])


                linha_aluno = [" ", ("information", [1, 1, 1, 1], f"  {id}"), nome, turma, id_turma, id_escola,curso,turno, nascimento, ]

                self.data_table.row_data.append(linha_aluno)
            else:
                self.show_snackbar("ID Errado")


    #FUNÇÕES DA TELA SCHOOL MONITORAMENT SCREEN


    #FUNÇÕES GERAIS
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
                    aluno["mes_propina_paga"]=linha[8]
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
    def close_dialog(self, *args):
        self.dialog.dismiss()
    def curso_conversor(self,turma):

        turma_inciais = turma[:2]
        if turma_inciais =="TI":
            curso = "Técnico Informático"
        if turma_inciais == "DT":
            curso = "Desenhador Projetista"
        else:
            curso="None"
        return curso
    def separar_numeros_letras(self,string):
        numeros = ''.join(re.findall(r'\d+', string))
        letras = ''.join(re.findall(r'[a-zA-Z]+', string))
        return numeros, letras

    def converter_nome_p_u(self,nome):
        converter=str(nome).split(" ")
        nome_P_U=f"{converter[0]} {converter[-1]}"

        return nome_P_U

    def autorizador_entrada(self,mes):
        meses=["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Novembro","Dezembro"]
        mes_atual_index = datetime.datetime.now().month

        if mes in meses:
            mes_index=int(meses.index(mes))


            if (mes_index+1)<(mes_atual_index):
                return f"Recusado ({mes})"

            elif (mes_index+1)>=(mes_atual_index):
                return "Autorizado"

    def classe_aluno(self,turma):
        classe,letras=self.separar_numeros_letras(turma)
        return str(classe)



# finally, run the app
if __name__ == "__main__":
    LiveApp().run()