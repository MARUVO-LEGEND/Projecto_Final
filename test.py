from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDFlatButton


class MyApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Definindo os dados da tabela
        data = {
            "Header 1": "Value 1",
            "Header 2": "Value 2",
            "Header 3": "Value 3",
        }

        # Criando a tabela
        table = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            check=True,
            column_data=[
                ("Column 1", (30)),
                ("Column 2", (30)),
                ("Column 3", (30)),
            ],
            row_data=[
                (f"{key}", f"{value}", f"Additional Data {value}") for key, value in data.items()
            ]
        )

        # Associando dados adicionais a cada linha da tabela
        for row in table.row_data:
            row.data = {"Additional_Info": row.text + " - Additional Info"}

        # Adicionando a tabela ao layout
        layout.add_widget(table)
        return layout


if __name__ == "__main__":
    MyApp().run()
