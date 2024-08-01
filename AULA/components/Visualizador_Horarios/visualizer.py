import flet as ft

class Visualizer(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Column()

class Card():
    def __init__(self):
        self.view = ft.Container(
            width=150,
            expand=True,
            content= ft.Column(
                expand=True,
                expand_loose=True,
                controls=[
                    ft.Text("Materia"),
                    ft.Text("Profesor"),
                    ft.Text("Aula")
                ]
        ),
        bgcolor="#1abc9c",
        on_click=lambda _: print("click"),
        border_radius=10,
        padding=10,
    )

def generar_rows(texto_primera_columna: str = ""):
    result = []
    result.append(ft.DataCell(ft.Text(f"{texto_primera_columna}", width=100), data="Horario"),)
    result.append(ft.DataCell(ft.Text("---"), data= "Lunes"),)
    result.append(ft.DataCell(ft.Text("---"), data = "Martes"),)
    result.append(ft.DataCell(ft.Text("---"), data="Miercoles"),)
    result.append(ft.DataCell(ft.Text("---"), data="Jueves"),)
    result.append(ft.DataCell(ft.Text("---"), data="Viernes"),)
    result.append(ft.DataCell(ft.Text("---"), data="Sabado"),)
    result.append(ft.DataCell(ft.Text("---"), data="Domingo"),)
    return result

def modificar_celda(tabla: ft.DataTable = None, fila: int = 0, columna: int = 0, contenido: ft.Container = None):
    if ((tabla != None) and (tabla is ft.DataTable)):



def main(page: ft.Page):
    generic_card = ft.Container(
        width=150,
        expand=True,
        content= ft.Column(
            expand=True,
            expand_loose=True,
            controls=[
                ft.Text("Materia"),
                ft.Text("Profesor"),
                ft.Text("Aula")
            ]
        ),
        bgcolor="#1abc9c",
        on_click=lambda e: print("click"),
        border_radius=10,
        padding=10,
    )
    tabla = ft.DataTable(
        data_row_max_height=float("inf"),
        expand=True,
        columns=[
            ft.DataColumn(ft.Text(""), data="Horarios"),
            ft.DataColumn(ft.Text("Lunes"), data="Lunes"),
            ft.DataColumn(ft.Text("Martes"), data="Martes"),
            ft.DataColumn(ft.Text("Miercoles"), data="Miercoles"),
            ft.DataColumn(ft.Text("Jueves"), data="Jueves"),
            ft.DataColumn(ft.Text("Viernes"), data="Viernes"),
            ft.DataColumn(ft.Text("Sabado"), data="Sabado"),
            ft.DataColumn(ft.Text("Domingo"), data="Domingo"),

        ],
        rows=[
            ft.DataRow(
                data="8>9",
                cells=[
                    ft.DataCell(ft.Text("8hs a 9hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="9>10",
                cells=[
                    ft.DataCell(ft.Text("9hs a 10hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="10>11",
                cells=[
                    ft.DataCell(ft.Text("10hs a 11hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="11>12",
                cells=[
                    ft.DataCell(ft.Text("11hs a 12hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="12>13",
                cells=[
                    ft.DataCell(ft.Text("12hs a 13hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="13>14",
                cells=[
                    ft.DataCell(ft.Text("13hs a 14hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="14>15",
                cell=[
                    ft.DataCell(ft.Text("14hs a 15hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="15>16",
                cells=[
                    ft.DataCell(ft.Text("15hs a 16hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data = "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="16>17",
                cells=[
                    ft.DataCell(ft.Text("16hs a 17hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                cell=[
                    ft.DataCell(ft.Text("14hs a 15hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="15>16",
                cells=[
                    ft.DataCell(ft.Text("15hs a 16hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data = "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="16>17",
                cells=[
                    ft.DataCell(ft.Text("16hs a 17hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data= "Lunes"),
                    ft.DataCell(generic_card, data = "Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="17>18",
                cells=[
                    ft.DataCell(ft.Text("17hs a 18hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data="Lunes"),
                    ft.DataCell(ft.Text("---"), data="Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="18>19",
                cells=[
                    ft.DataCell(ft.Text("18hs a 19hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data="Lunes"),
                    ft.DataCell(ft.Text("---"), data="Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="19>20",
                cells=[
                    ft.DataCell(ft.Text("19hs a 20hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data="Lunes"),
                    ft.DataCell(ft.Text("---"), data="Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="20>21",
                cells=[
                    ft.DataCell(ft.Text("20hs a 21hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data="Lunes"),
                    ft.DataCell(ft.Text("---"), data="Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="21>22",
                cells=[
                    ft.DataCell(ft.Text("21hs a 22hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data="Lunes"),
                    ft.DataCell(ft.Text("---"), data="Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
            ft.DataRow(
                data="22>23",
                cells=[
                    ft.DataCell(ft.Text("22hs a 23hs"), data="Horario"),
                    ft.DataCell(ft.Text("---"), data="Lunes"),
                    ft.DataCell(ft.Text("---"), data="Martes"),
                    ft.DataCell(ft.Text("---"), data="Miercoles"),
                    ft.DataCell(ft.Text("---"), data="Jueves"),
                    ft.DataCell(ft.Text("---"), data="Viernes"),
                    ft.DataCell(ft.Text("---"), data="Sabado"),
                    ft.DataCell(ft.Text("---"), data="Domingo"),
                ]
            ),
        ],
    )

    page.add(
        ft.Container(
            expand=True,
            content=tabla,
            alignment=ft.alignment.center,
        )
    )


if __name__ == '__main__':
    ft.app(target=main)
