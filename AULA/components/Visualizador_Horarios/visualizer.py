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

def generar_rows(texto_primera_columna: str = ""):
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
        columns=[
            ft.DataColumn(ft.Text("", text_align=ft.TextAlign.CENTER), data="Horarios"),
            ft.DataColumn(ft.Text("Lunes", text_align=ft.TextAlign.CENTER), data="Lunes"),
            ft.DataColumn(ft.Text("Martes", text_align=ft.TextAlign.CENTER), data="Martes"),
            ft.DataColumn(ft.Text("Miercoles", text_align=ft.TextAlign.CENTER), data="Miercoles"),
            ft.DataColumn(ft.Text("Jueves", text_align=ft.TextAlign.CENTER), data="Jueves"),
            ft.DataColumn(ft.Text("Viernes", text_align=ft.TextAlign.CENTER), data="Viernes"),
            ft.DataColumn(ft.Text("Sabado", text_align=ft.TextAlign.CENTER), data="Sabado"),
            ft.DataColumn(ft.Text("Domingo", text_align=ft.TextAlign.CENTER), data="Domingo"),

        ],
        rows=[
            ft.DataRow(
                data="8>9",
                cells=generar_rows("8-9")
            ),
            ft.DataRow(
                data="9>10",
                cells=generar_rows("9-10")
            ),
            ft.DataRow(
                data="10>11",
                cells=generar_rows("10-11")
            ),
            ft.DataRow(
                data="11>12",
                cells=generar_rows("11-12")
            ),
            ft.DataRow(
                data="12>13",
                cells=generar_rows("12-13")
            ),
            ft.DataRow(
                data="13>14",
                cells=generar_rows("13-14")
            ),
            ft.DataRow(
                data="14>15",
                cells=generar_rows("14-15")
            ),
            ft.DataRow(
                data="15>16",
                cells=generar_rows("15-16")
            ),
            ft.DataRow(
                data="16>17",
                cells=generar_rows("16-17")
            ),
            ft.DataRow(
                data="17>18",
                cells=generar_rows("17-18")
            ),
            ft.DataRow(
                data="18>19",
                cells=generar_rows("18-19")
            ),
            ft.DataRow(
                data="19>20",
                cells=generar_rows("19-20")
            ),
            ft.DataRow(
                data="20>21",
                cells=generar_rows("20-21")
            ),
            ft.DataRow(
                data="21>22",
                cells=generar_rows("21-22")
            ),
            ft.DataRow(
                data="22>23",
                cells=generar_rows("22-23")
            )
        ],
    )

    test_data = [
        [(5, "B102"),(2,"Fisica 2"),(40, "CATERINA"), "Lunes",8,9]
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
        "Defensa contra las artes oscuras": ft.colors.PINK,
        "Ingenieria de Software": ft.colors.ORANGE
    }

    for data_asignacion in test_data:
        modificar_celda(
            tabla=tabla,
            fila= data_asignacion[4] - 7,
            columna= dias[data_asignacion[3]],
            contenido= Custom_Card(
                bgcolor = bgcolor_segun_materia[data_asignacion[1][1]],
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
