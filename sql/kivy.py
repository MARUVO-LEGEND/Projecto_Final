from  import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ObjectProperty

class AlunoInfoButton(Button):
    aluno = ObjectProperty(None)

class AlunoInfoView(BoxLayout):
    nome = ObjectProperty(None)
    idade = ObjectProperty(None)
    curso = ObjectProperty(None)

class AlunoListItem(RecycleDataViewBehavior, BoxLayout):
    selected = BooleanProperty(False)
    aluno = ObjectProperty(None)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.aluno = data['aluno']
        self.nome.text = self.aluno.nome

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.selected_index = self.index
            return True
        return super().on_touch_down(touch)

class AlunoList(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'aluno': Aluno(f'Aluno {i}', 20 + i, 'Curso') } for i in range(50)]

    def show_aluno_info(self, aluno):
        self.parent.parent.info_view.nome.text = aluno.nome
        self.parent.parent.info_view.idade.text = str(aluno.idade)
        self.parent.parent.info_view.curso.text = aluno.curso

class Aluno:
    def __init__(self, nome, idade, curso):
        self.nome = nome
        self.idade = idade
        self.curso = curso

class MyApp(App):
    def build(self):
        return AlunoList()

if __name__ == '__main__':
    MyApp().run()
