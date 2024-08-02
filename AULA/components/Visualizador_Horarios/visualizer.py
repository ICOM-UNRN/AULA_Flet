from typing import Callable
import flet as ft

class Custom_Card(ft.Container):
    def __init__(self, func_on_click: Callable = None,materia: str = "", horario_comienzo: int = 8, horario_fin: int = 9, profesor: str = "", aula: str = "", dia: str = "", *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.data= {
            "materia": materia,
            "horario_comienzo": horario_comienzo,
            "horario_fin": horario_fin,
            "profesor": profesor,
            "aula": aula,
            "dia": dia
        }
        self.width=150
        self.expand=True
        self.content= ft.Column(
            expand=True,
            expand_loose=True,
            controls=[
                ft.Text(materia[1]),
            ]
        )
        self.on_click= func_on_click
        self.border_radius=10
        self.padding=10

    def get_card_data(self) -> dict:
        """Returns de card actual data"""
        return self.data

    def set_card_data(self, data : dict):
        """
        Sets de card actual data
        
        Args:
            data (dict): data to set
        """
        self.data = data
    
    def build(self):
        return self

def generar_cells_of_rows(texto_primera_columna: str = ""):
    result = []
    result.append(ft.DataCell(ft.Text(f"{texto_primera_columna}", width=100), data="Horario"))
    result.append(ft.DataCell(ft.Text("---"), data= "Lunes"),)
    result.append(ft.DataCell(ft.Text("---"), data = "Martes"),)
    result.append(ft.DataCell(ft.Text("---"), data="Miercoles"),)
    result.append(ft.DataCell(ft.Text("---"), data="Jueves"),)
    result.append(ft.DataCell(ft.Text("---"), data="Viernes"),)
    result.append(ft.DataCell(ft.Text("---"), data="Sabado"),)
    result.append(ft.DataCell(ft.Text("---"), data="Domingo"),)
    return result

def generar_row_of_columns():
    result = []
    result.append(ft.DataColumn(ft.Text("", text_align=ft.TextAlign.CENTER), data="Horarios"),)
    result.append(ft.DataColumn(ft.Text("Lunes", text_align=ft.TextAlign.CENTER), data="Lunes"),)
    result.append(ft.DataColumn(ft.Text("Martes", text_align=ft.TextAlign.CENTER), data="Martes"),)
    result.append(ft.DataColumn(ft.Text("Miercoles", text_align=ft.TextAlign.CENTER), data="Miercoles"),)
    result.append(ft.DataColumn(ft.Text("Jueves", text_align=ft.TextAlign.CENTER), data="Jueves"),)
    result.append(ft.DataColumn(ft.Text("Viernes", text_align=ft.TextAlign.CENTER), data="Viernes"),)
    result.append(ft.DataColumn(ft.Text("Sabado", text_align=ft.TextAlign.CENTER), data="Sabado"),)
    result.append(ft.DataColumn(ft.Text("Domingo", text_align=ft.TextAlign.CENTER), data="Domingo"),)
    return result

def generar_all_rows():
    result = []
    for i in range(8, 23):
        result.append(ft.DataRow(data=f"{i}>{i+1}", cells=generar_cells_of_rows(f"{i}-{i+1}")))
    return result

def modificar_celda(tabla: ft.DataTable = None, fila: int = 0, columna: int = 0, contenido: ft.Container = None):
    if (tabla is not None) and isinstance(tabla, ft.DataTable):
        tabla.rows[fila].cells[columna].content = contenido

def crear_tabla():
    def click_card(e: ft.ControlEvent):
        card = e.control
        data_card = card.get_card_data()
        print(data_card)

    tabla = ft.DataTable(
        data_row_max_height=float("inf"),
        expand=True,
        columns=generar_row_of_columns(),
        rows=generar_all_rows()
    )

    test_data = [
        [(6, "B142"),(5,"Defensa Contra las Artes Obscuras"),(40, "CATERINA"), "Lunes",8,9],
        [(5, "Aula 102"),(2,"Fisica 2"),("Profesor 1", 40), "Lunes",8,9],
        [(10, "Aula 102"),(3,"Matematica"),("Profesor 2", 40), "Lunes",9,10],
        [(24, "Aula 142"),(5,"Defensa Contra las Artes Obscuras"),("Profesor 3", 40), "Lunes",10,11],
        [(3, "Aula 101"),(4,"Programacion"),("Profesor 4", 30), "Martes",11,12],
        [(9, "Aula 101"),(1,"Algebra"),("Profesor 5", 30), "Martes",12,13],
        [(2, "Aula 141"),(6,"Estadistica"),("Profesor 6", 30), "Martes",13,14],
        [(7, "Aula 103"),(8,"Informatica"),("Profesor 7", 25), "Miercoles",14,15],
        [(4, "Aula 105"),(7,"Filosofia"),("Profesor 8", 25), "Miercoles",15,16],
        [(1, "Aula 143"),(9,"Historia"),("Profesor 9", 25), "Miercoles",16,17],
        [(8, "Aula 104"),(10,"Sociologia"),("Profesor 10", 18), "Jueves",17,18]
    ]

    dias = {
        "Lunes": 1,
        "Martes": 2,
        "Miercoles": 3,
        "Jueves": 4,
        "Viernes": 5,
        "Sabado": 6,
        "Domingo": 7
    }

    bgcolor_segun_materia = {
        "Fisica 2": ft.colors.BLUE,
        "Matematica": ft.colors.RED,
        "Geometria": ft.colors.GREEN,
        "Defensa Contra las Artes Obscuras": ft.colors.PINK,
        "Ingenieria de Software": ft.colors.ORANGE,
        "Historia": ft.colors.RED_600,
        "Programacion": ft.colors.LIGHT_BLUE,
        "Estadistica": ft.colors.LIGHT_GREEN_900
    }

    for data_asignacion in test_data:
        materia = data_asignacion[1][1]
        bg_color_card = bgcolor_segun_materia.get(materia, "#FFFFFF")
        modificar_celda(
            tabla=tabla,
            fila= data_asignacion[4] - 7,
            columna= dias[data_asignacion[3]],
            contenido= Custom_Card(
                bgcolor = bg_color_card,
                aula= data_asignacion[0],
                materia= data_asignacion[1],
                profesor= data_asignacion[2],
                dia= data_asignacion[3],
                horario_comienzo= data_asignacion[4],
                horario_fin= data_asignacion[5],
                func_on_click= click_card
            )
        )

    return tabla

def main(page : ft.Page):
    tabla = crear_tabla()
    page.add(
        ft.Container(
            expand=True,
            content=tabla,
            alignment=ft.alignment.center,
        )
    )


if __name__ == '__main__':
    ft.app(target=main)
