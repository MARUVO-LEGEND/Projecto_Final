from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: "10dp"

    MDTextField:
        id: text_field1
        hint_text: "Selecione uma opção"
        on_focus: if self.focus: app.show_menu1()

    MDTextField:
        id: text_field2
        hint_text: "Selecione outra opção"
        on_focus: if self.focus: app.show_menu2()
'''

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_menu1(self):
        menu_items = [
            {"text": "Opção 1", "viewclass": "OneLineListItem", "on_release": lambda x="Opção 1": self.select_option(x, 1)},
            {"text": "Opção 2", "viewclass": "OneLineListItem", "on_release": lambda x="Opção 2": self.select_option(x, 1)},
            {"text": "Opção 3", "viewclass": "OneLineListItem", "on_release": lambda x="Opção 3": self.select_option(x, 1)},
        ]
        self.menu1 = MDDropdownMenu(items=menu_items, width_mult=4)
        self.menu1.open()

    def show_menu2(self):
        menu_items = [
            {"text": "Opção A", "viewclass": "OneLineListItem", "on_release": lambda x="Opção A": self.select_option(x, 2)},
            {"text": "Opção B", "viewclass": "OneLineListItem", "on_release": lambda x="Opção B": self.select_option(x, 2)},
            {"text": "Opção C", "viewclass": "OneLineListItem", "on_release": lambda x="Opção C": self.select_option(x, 2)},
        ]
        self.menu2 = MDDropdownMenu(items=menu_items, width_mult=4)
        self.menu2.open()

    def select_option(self, text, field_id):
        if field_id == 1:
            self.root.ids.text_field1.text = text
            self.menu1.dismiss()
        elif field_id == 2:
            self.root.ids.text_field2.text = text
            self.menu2.dismiss()

TestApp().run()
