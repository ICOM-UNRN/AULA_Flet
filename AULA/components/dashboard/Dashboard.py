import flet as ft
from .Data_table import DataTableCustom

class Dashboard(ft.Container):
    def __init__(self, data):
        super().__init__()
        self.dashboard_data = data
        self.expand = True
        self.data_table = DataTableCustom(
            data_columns = self.dashboard_data["colums"],
            data_rows= self.dashboard_data["rows"]
        )
        self.content= self.data_table.build()


def main(page : ft.Page):
    page.title = "Dashboard" 
    dashboard = Dashboard(
        data={
            "colums" : ["dni", "nombre", "apellido", "condicion", "categoria", "dedicacion", "periodo_a_cargo"],
            "rows" : [(12345678, "Javier", "Hernandez", "Activo", "Licenciado", "Dedicacion", "2022-2023")]
        }
    )
    page.add(dashboard)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)