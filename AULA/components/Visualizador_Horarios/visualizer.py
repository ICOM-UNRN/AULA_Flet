from typing import Callable
import flet as ft
#from components.ABM_form.Form import DeleteModifyForm
import os
import sys
import random

# Agregar la ruta relativa al sys.path
ruta_relativa = os.path.join(os.path.dirname(__file__), '..','..')
sys.path.insert(0, ruta_relativa)

from api.db import connect_to_db
from api.asignacion.asignacion import Asignacion
from api.aula.aula import Aula
from api.materia.materia import Materia
from api.profesor.profesor import Profesor
# from api.edificio.edificio import Edificio
# from api.evento.evento import Evento
# from api.profesor.profesor_por_materia import Profesor_por_materia
# from api.recurso.recurso import Recurso
# from api.recurso.recurso_por_aula import Recurso_por_aula

db = connect_to_db()
asignacion_db = Asignacion(conn=db)
aula_db = Aula(conn=db)
materia_db = Materia(conn=db)
profesor_db = Profesor(conn=db)
# edificio_db = Edificio(conn=db)
# evento_db = Evento(conn=db)
# recurso_por_aula_db = Recurso_por_aula(conn=db)
# recurso_db = Recurso(conn=db)
# profesor_por_materia_db = Profesor_por_materia(conn=db)

class Custom_Card(ft.Container):
    def __init__(self, func_on_click: Callable = None,materia: str = "", horario_comienzo: int = 8, horario_fin: int = 9, profesor: str = "", aula: str = "", dia: str = "", id_asignacion: int = None, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.data= {
            "materia": materia,
            "horario_comienzo": horario_comienzo,
            "horario_fin": horario_fin,
            "profesor": profesor,
            "aula": aula,
            "dia": dia,
            "id_asignacion": id_asignacion
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
    
    def set_on_click(self, func):
        self.on_click = func

    def build(self):
        return self


def establecer_asignaciones_materias(carrera, edificio, aula) -> dict:
    asignaciones = asignacion_db.get_materias_eventos_asignados(carrera, edificio, aula)
    datos = asignaciones["rows"]
    data = []
    for linea in datos:
        delta_horario = linea[9] - (linea[8])
        while delta_horario > 0:
            data.append([(linea[0],linea[1]),(linea[2],linea[3]),linea[6],linea[7],linea[8]+(delta_horario-1), linea[8]+delta_horario,linea[10]])
            delta_horario -= 1
    return data

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
    result.append(ft.DataColumn(ft.Text("", text_align=ft.TextAlign.CENTER, size=20), data="Horarios"),)
    result.append(ft.DataColumn(ft.Text("Lunes", text_align=ft.TextAlign.CENTER, size=20), data="Lunes"),)
    result.append(ft.DataColumn(ft.Text("Martes", text_align=ft.TextAlign.CENTER, size=20), data="Martes"),)
    result.append(ft.DataColumn(ft.Text("Miercoles", text_align=ft.TextAlign.CENTER, size=20), data="Miercoles"),)
    result.append(ft.DataColumn(ft.Text("Jueves", text_align=ft.TextAlign.CENTER, size=20), data="Jueves"),)
    result.append(ft.DataColumn(ft.Text("Viernes", text_align=ft.TextAlign.CENTER, size=20), data="Viernes"),)
    result.append(ft.DataColumn(ft.Text("Sabado", text_align=ft.TextAlign.CENTER, size=20), data="Sabado"),)
    result.append(ft.DataColumn(ft.Text("Domingo", text_align=ft.TextAlign.CENTER, size=20), data="Domingo"),)
    return result

def generar_all_rows():
    result = []
    for i in range(8, 23):
        result.append(ft.DataRow(data=f"{i}>{i+1}", cells=generar_cells_of_rows(f"{i}-{i+1}")))
    return result

def modificar_celda(tabla: ft.DataTable = None, fila: int = 0, columna: int = 0, contenido: ft.Container = None):
    if (tabla is not None) and isinstance(tabla, ft.DataTable):
        tabla.rows[fila].cells[columna].content = contenido

def generar_codigo_hexadecimal():
    caracteres = "0123456789ABCDEF"
    codigo = "#"
    for _ in range(6):
        codigo += random.choice(caracteres)
    return codigo

def crear_tabla(page, carrera = None, edificio = None, aula = None):
    def click_card(e: ft.ControlEvent):
        card = e.control
        data_card = card.get_card_data()
        print(data_card)
        page.overlay[1].open = True
        page.update()
        cargar_valores_a_textfields(page, data_card)

    tabla = ft.DataTable(
        data_row_max_height=float("inf"),
        expand=True,
        columns=generar_row_of_columns(),
        rows=generar_all_rows(),
    )

    test_data = establecer_asignaciones_materias(carrera,edificio,aula)
    # [
    #     [(6, "B142"),(5,"Defensa Contra las Artes Obscuras"),(40, "CATERINA"), "Lunes",8,9],
    #     [(5, "Aula 102"),(2,"Fisica 2"),("Profesor 1", 40), "Lunes",8,9],
    #     [(10, "Aula 102"),(3,"Matematica"),("Profesor 2", 40), "Lunes",9,10],
    #     [(24, "Aula 142"),(5,"Defensa Contra las Artes Obscuras"),("Profesor 3", 40), "Lunes",10,11],
    #     [(3, "Aula 101"),(4,"Programacion"),("Profesor 4", 30), "Martes",11,12],
    #     [(9, "Aula 101"),(1,"Algebra"),("Profesor 5", 30), "Martes",12,13],
    #     [(2, "Aula 141"),(6,"Estadistica"),("Profesor 6", 30), "Martes",13,14],
    #     [(7, "Aula 103"),(8,"Informatica"),("Profesor 7", 25), "Miercoles",14,15],
    #     [(4, "Aula 105"),(7,"Filosofia"),("Profesor 8", 25), "Miercoles",15,16],
    #     [(1, "Aula 143"),(9,"Historia"),("Profesor 9", 25), "Miercoles",16,17],
    #     [(8, "Aula 104"),(10,"Sociologia"),("Profesor 10", 18), "Jueves",17,18]
    # ]

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
    }

    for data_asignacion in test_data:
        materia = data_asignacion[1][1]
        if not bgcolor_segun_materia.get(materia, None):
            color = generar_codigo_hexadecimal()
            bgcolor_segun_materia[materia] = color
            bg_color_card = color
        else:
            bg_color_card = bgcolor_segun_materia.get(materia, "#9B6B6B")
        modificar_celda(
            tabla=tabla,
            fila= data_asignacion[4] - 8,
            columna= dias[data_asignacion[3]],
            contenido= Custom_Card(
                bgcolor = bg_color_card,
                aula= data_asignacion[0],
                materia= data_asignacion[1],
                profesor= data_asignacion[2],
                dia= data_asignacion[3],
                horario_comienzo= data_asignacion[4],
                horario_fin= data_asignacion[5],
                id_asignacion= data_asignacion[6],
                func_on_click= click_card
            )
        )

    return tabla

# (deprecated xd) -----------------------------------------------------------------------------------
# def injectar_funcion_bottomsheet_onclick_on_cell(page: ft.Page, table: ft.DataTable):
    
#     def mostrar_bottom_sheet(page, table, row, column):
#         print(f"{page.route}")
#         print(f"...[{i}][{j}]")
#         #print(f"...[{i}][{j}]|{table.rows[i].cells[j].content.get_card_data()}")
#         # page.overlay[1].open = True
#         # page.update()
    
#     for i in range(len(table.rows)):
#         print(f"-----------------|{i}|-----------------")
#         for j in range(0, len(table.rows[i].cells)):
#             if isinstance(table.rows[i].cells[j].content, Custom_Card):
#                 print(f"[{i}][{j}]|{table.rows[i].cells[j].content.get_card_data()}")
#                 aux = copy.copy(i)
#                 #print(table.rows[i].cells[j].content.content.controls[0].value)
#                 table.rows[i].cells[j].content.set_on_click(lambda e: mostrar_bottom_sheet(page, table, aux, j))
#             else:
#                 #print(table.rows[i].cells[j].content.value)
#                 pass
# ---------------------------------------------------------------------------------------------------
def eliminar_asignacion(page, campos):
    asignacion_db.delete_asignacion(campos[0].value)
    
    page.session.get("main_container").content = crear_tabla(page)    
    page.overlay[1].open = False
    page.update()

def insertar_asignacion(page, campos):
    valores = {
        "id_asignacion": campos[0].value,
        "id_aula": campos[2].value,
        "id_materia": campos[1].value,
        "dia": campos[3].value,
        "horario_inicio": campos[4].value,
        "hora_fin":campos[5].value
    }
    asignacion_db.insert_asignacion(valores["id_aula"],valores["dia"],valores["horario_inicio"],valores["hora_fin"],valores["id_materia"])
    
    campos[0].value=""
    campos[1].value=""
    campos[2].value=""
    campos[3].value=""
    campos[4].value=""
    campos[5].value=""
    
    page.session.get("main_container").content = crear_tabla(page)    
    page.overlay[2].open = False
    page.update()
    
# Función para guardar los valores y vaciar los campos de texto
def guardar_y_vaciar_campos(page, campos):
    valores = {
        "id_asignacion": campos[0].value,
        "id_aula": campos[2].value,
        "id_materia": campos[1].value,
        "dia": campos[3].value,
        "horario_inicio": campos[4].value,
        "hora_fin":campos[5].value
    }
    print("Valores guardados:", valores)
    asignacion_db.update_asignacion(valores["id_asignacion"],valores["id_aula"],valores["id_materia"],None,valores["dia"],valores["horario_inicio"],valores["hora_fin"])
    page.session.get("main_container").content = crear_tabla(page)
    # campos[0].value = ""
    # campos[1].value = ""
    # campos[2].value = ""
    
    page.overlay[1].open = False
    page.update()

def cargar_valores_a_textfields(page, valores):
    print(f"||||{valores}|||")
    valores_db = asignacion_db.get_asignacion_por_id(valores['id_asignacion'])["rows"][0]
    controles = page.overlay[1].content.content.controls[0]
    controles.controls[0].value = valores['id_asignacion']
    controles.controls[0].update()
    controles.controls[1].value = valores_db[1]
    controles.controls[1].update()
    controles.controls[2].value = valores_db[0]
    controles.controls[2].update()
    # page.overlay[1].content.content.controls[0].controls[3].value = valores['profesor']
    # page.overlay[1].content.content.controls[0].controls[3].update()
    controles.controls[3].value = valores_db[2]
    controles.controls[3].update()
    controles.controls[4].value = valores_db[3]
    controles.controls[4].update()
    controles.controls[5].value = valores_db[4]
    controles.controls[5].update()
    page.update()


############################################################################################################################
# DROPDOWNS PARA LOS BOTTOMSHEETS DE LAS CARTAS, PARA PODER MODIFICARLAS SOLO CON VALORES YA EXISTENTES EN LA BASE DE DATOS
############################################################################################################################

def get_dropdown_materias():
    result = []
    for aux in materia_db.get_materias()["rows"]:
        result.append(ft.dropdown.Option(aux[0], text=aux[3]))
    return result

def get_dropdown_aulas():
    result = []
    for aux in aula_db.get_aulas()["rows"]:
        result.append(ft.dropdown.Option(aux[0], text=aux[2]))
    return result

def get_dropdown_profesores():
    result = []
    for aux in profesor_db.get_profesores()["rows"]:
        nombre_apellido = aux[2]+" "+aux[3]
        result.append(ft.dropdown.Option(aux[0], text=nombre_apellido))
    return result

def get_dropdown_dias():
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo",]
    result = []
    for aux in dias:
        result.append(ft.dropdown.Option(aux, text=aux))
    return result

def get_dropdown_horas_posibles(inicio: bool = False):
    result = []
    for i in range(8, 24):
        if inicio and i==23:
            break
        result.append(ft.dropdown.Option(i, text=i))
    return result

############################################################################################################################
def cerrar_bottom_sheet_insertar(page,campos):
    campos[0].value=""
    campos[1].value=""
    campos[2].value=""
    campos[3].value=""
    campos[4].value=""
    campos[5].value=""
    page.overlay[2].open = False
    page.update()

def nueva_asignacion(page):
    page.overlay[2].open = True
    page.update()

def habilitar_modificación_horario(page):
    page.overlay[1].content.content.controls[0].controls[3].disabled = False
    page.update()

def crear_bottomsheet(page, insert: bool):
    # Campos de texto
    campos = [
        ft.TextField(
            label="ID asignacion",
            disabled=True
            ),
        ft.Dropdown(
            options=get_dropdown_materias(),
            label = "Materia",
        ),
        ft.Dropdown(
            options=get_dropdown_aulas(),
            label = "Aula",
        ),
        # ft.Dropdown(
        #     options=get_dropdown_profesores(),
        #     label = "Profesor",
        # ),
        ft.Dropdown(
            options=get_dropdown_dias(),
            label = "Dia",
        ),
        ft.Dropdown(
            options=get_dropdown_horas_posibles(True),
            label = "Horario Comienzo",
            # disabled=True
        ),
        ft.Dropdown(
            options=get_dropdown_horas_posibles(),
            label = "Horario Fin",
            # disabled=True
        ),
    ]
    
    if insert :
        bottom_sheet_content = ft.Container(
        content=ft.Column([
            ft.Column(campos),
            ft.Row([
                ft.ElevatedButton(text="Guardar", bgcolor=ft.colors.BLUE_400,
                                      color=ft.colors.BLACK, icon=ft.icons.SAVE, on_click=lambda e: insertar_asignacion(page, campos)),
                ft.ElevatedButton(text="Cancelar", bgcolor=ft.colors.RED_400, color=ft.colors.BLACK,
                                      icon=ft.icons.CANCEL, on_click=lambda e: cerrar_bottom_sheet_insertar(page,campos)),
            ]),
            
        ]),
        padding=20,
        margin=20,
    )
    else:
        # Contenido del BottomSheet
        bottom_sheet_content = ft.Container(
            content=ft.Column([
                ft.Column(campos),
                ft.Row([
                    ft.ElevatedButton("Guardar Cambios", bgcolor=ft.colors.AMBER_400,
                                        color=ft.colors.BLACK, icon=ft.icons.EDIT, on_click=lambda e: guardar_y_vaciar_campos(page, campos)),
                    ft.ElevatedButton("Borrar Asignación", bgcolor=ft.colors.RED_400,
                                        color=ft.colors.BLACK, icon=ft.icons.DELETE, on_click=lambda e: eliminar_asignacion(page, campos)),
                ]),
                
            ]),
            padding=20,
            margin=20,
        )

    return ft.BottomSheet(content=bottom_sheet_content, is_scroll_controlled=True)

def main_er(page : ft.Page):
    # Añade el BottomSheet a la página
    bottom_sheet = crear_bottomsheet(page,False)
    bottom_sheet_insertar = crear_bottomsheet(page,True)
    page.overlay.append(bottom_sheet)
    page.overlay.append(bottom_sheet_insertar)

    tabla = crear_tabla(page)
    main_container = ft.Container(
                        expand=True,
                        content=tabla,
                        bgcolor= ft.colors.with_opacity(0.90, "#3A3A3A"),
                        border_radius=20,
                        alignment=ft.alignment.center,
                        # scale=0.75
                    )
    page.session.set("main_container", main_container)
    return(main_container)

    # # Añade botón para agregar asignaciones manualmente
    # page.add(
    #     ft.ElevatedButton("Agregar Asignación Manualmente", on_click=lambda e: nueva_asignacion(page))#mostrar_bottom_sheet(page, tabla, 0, 0)
    # )


if __name__ == '__main__':
    ft.app(target=main_er)
