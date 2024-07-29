import re
import flet as ft
from components.dashboard.Dashboard import Dashboard
# from components.RailBar.Railbar import RailBarCustom
from components.ABM_form.Form import DeleteModifyForm
from visualizer_UI.schedules_v1 import create_calendar_table_headers_first_row,create_calendar_rows,create_calendar_hours_intervals,ItemList_Creator,ItemList_Remover,ItemList_Modifier
from api.db import connect_to_db
from api.aula.aula import Aula
from api.materia.materia import Materia
from api.asignacion.asignacion import Asignacion
from api.edificio.edificio import Edificio
from api.evento.evento import Evento
from api.profesor.profesor import Profesor
from api.profesor.profesor_por_materia import Profesor_por_materia
from api.recurso.recurso import Recurso
from api.recurso.recurso_por_aula import Recurso_por_aula

def main(page: ft.Page):
    page.title = "AULA - Administracion Unificada de Lugares Academicos"
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    db = connect_to_db()

    ###################################################################################
    #                                FUNC VER HORARIOS                                #
    ###################################################################################

    def crear_visualizacion_horarios():
        dias = [" ", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        intervalos_horarios = create_calendar_hours_intervals(8, 23)

        creador = ItemList_Creator(page, "ItemList_creador")
        removedor = ItemList_Remover(page, "ItemList_removedor")
        modificador = ItemList_Modifier(page, "ItemList_modoficador")

        column_visualizer = ft.Column(
            alignment= "start",
            scroll= ft.ScrollMode.ALWAYS,
            controls=[
                ft.Row(
                    vertical_alignment="start",
                    scroll= ft.ScrollMode.ALWAYS,
                    controls=[
                        ft.Column(controls=[creador, removedor, modificador]),
                        ft.Column(
                            scroll=ft.ScrollMode.ADAPTIVE,
                            expand=True,
                            alignment="start",
                            controls=[
                                ft.DataTable(
                                    columns=create_calendar_table_headers_first_row(dias),
                                    rows=create_calendar_rows(intervalos_horarios, dias, page),
                                    data_row_min_height = 130,
                                    data_row_max_height = float("inf"),
                                    bgcolor='#3A3A3A',
                                    column_spacing=5,
                                    heading_row_color= ft.colors.GREY_300
                                ),
                            ],
                        )
                    ],
                )
            ],
        )
        
        container_horarios.content = column_visualizer

    def load_search_bars():
        carreras = Materia(db).get_carreras()["rows"]
        edificios = Edificio(db).get_edificios()["rows"]
        aulas = Aula(db).get_aulas()["rows"]

        for carrera in carreras:
            listas_busquedas["search_bar_carrera"].append(ft.ListTile(title=ft.Text(carrera[0]), on_click=close_search_bar_carrera))
        for edificio in edificios:
            listas_busquedas["search_bar_edificio"].append(ft.ListTile(title=ft.Text(edificio[1]), on_click=close_search_bar_edifico))
        for aula in aulas:
            listas_busquedas["search_bar_aula"].append(ft.ListTile(title=ft.Text(aula[2]), on_click=close_search_bar_aula))

    def close_search_bar_edifico(e):
        text = f"{e.control.title.value}"
        print(text)
        search_bar_edificio.close_view(text)

    def close_search_bar_aula(e):
        text = f"{e.control.title.value}"
        print(text)
        search_bar_aula.close_view(text)

    def close_search_bar_carrera(e):
        text = f"{e.control.title.value}"
        print(text)
        search_bar_carrera.close_view(text)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")
        if e.data == "":
            print(listas_busquedas[e.control.data])
            e.control.controls = listas_busquedas[e.control.data]
            e.control.update()
            return

        result = [
            value
            for value in listas_busquedas[e.control.data]
            if re.search(e.data, value.title.value, re.IGNORECASE)
        ]
        print(result)
        e.control.controls = result
        e.control.update()

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")
        if e.data == "":
            print(listas_busquedas[e.control.data])
            e.control.controls = listas_busquedas[e.control.data]
            e.control.update()
            return

        result = [
            value
            for value in listas_busquedas[e.control.data]
            if re.search(e.data, value.title.value, re.IGNORECASE)
        ]
        print(result)
        if len(result) == 1:
            e.control.close_view(result[0].title.value)
        e.control.controls = result
        e.control.update()

    def handle_tap(e):
        e.control.open_view()


    ###################################################################################
    #                                  CAMBIO DE RUTAS                                #
    ###################################################################################
    def navigation_change(e):
        destination = e.control.destinations[int(e.data)].label
        if destination == "Inicio":
            page.go("/")
        else:
            page.go(f"/{destination.lower()}")

    def dismiss_bottom_sheet_func(_):
        page.session.get("actual_form").clear_fields()
        dashboard = page.session.get("actual_data_table")
        dashboard.data_table.deselectAll()
        page.close_bottom_sheet()

    def update_func(_):
        route = page.route
        bottom_sheet = page.session.get("actual_form")
        data = bottom_sheet.get_fields_actual_data()
        if route == "/asignaciones":
            asignacion = Asignacion(db)
            asignacion.update_asignacion(id=data[0],aula=data[1],materia=data[2],evento=data[3],dia=data[4],comienzo=data[5],fin=data[6])
        elif route == "/aulas":
            aula = Aula(db)
            aula.update_aula(id=data[0],nombre=data[2],edificio=data[1],capacidad=data[3])
        elif route == "/edificios":
            edificio = Edificio(db)
            edificio.update_edificio(id=data[0],nombre=data[1],calle=data[2],altura=data[3])
        elif route == "/eventos":
            evento = Evento(db)
            evento.update_evento(id=data[0],nombre=data[1],descripcion=data[2],comienzo=data[3],fin=data[4])
        elif route == "/materias":
            materia = Materia(db)
            materia.update_materia(id=data[0],codigo_guarani=data[1],carrera=data[2],nombre=data[3],anio=data[4],cuatrimestre=data[5],taxonomia=data[6],horas_semanales=data[7],comisiones=data[8],alumnos_esperados=data[9])
        elif route == "/profesores":
            profesor = Profesor(db)
            profesor.update_profesor(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
        elif route == "/profesores_por_materia":
            profesor_por_materia = Profesor_por_materia(db)
            profesor_por_materia.update_profesor_por_materia(id_materia=data[0],id_profesor=data[1],alumnos_esperados=data[2],tipo_clase=data[3],archivo=data[4])
        elif route == "/recursos":
            recurso = Recurso(db)
            recurso.update_recurso(id=data[0],nombre=data[1],descripcion=data[2])
        elif route == "/recursos_por_aula":
            recurso_por_aula=Recurso_por_aula(db)
            recurso_por_aula.update_recurso_por_aula(id_aula=data[0],id_recurso=data[1],cantidad=data[2])

        route_change(page)
        page.close_bottom_sheet()
        page.update()

    def delete_func(_):
        route = page.route
        data = page.session.get("actual_form").get_fields_data()
        if route == "/asignaciones":
            asignacion = Asignacion(db)
            asignacion.delete_asignacion(id=data[0])
        elif route == "/aulas":
            aula = Aula(db)
            aula.delete_aula(id=data[0])
        elif route == "/edificios":
            edificio = Edificio(db)
            edificio.delete_edificio(id=data[0])
        elif route == "/eventos":
            evento = Evento(db)
            evento.delete_evento(id=data[0])
        elif route == "/materias":
            materia = Materia(db)
            materia.delete_materia(id=data[0])
        elif route == "/profesores":
            profesor = Profesor(db)
            profesor.delete_profesor(id=data[0])
        elif route == "/profesores_por_materia":
            profesor_por_materia = Profesor_por_materia(db)
            profesor_por_materia.delete_profesor_por_materia(id_materia=data[0], id_profesor=data[1])
        elif route == "/recursos":
            recurso = Recurso(db)
            recurso.delete_recurso(id=data[0])
        elif route == "/recursos_por_aula":
            recurso_por_aula=Recurso_por_aula(db)
            recurso_por_aula.delete_recurso_por_aula(id_aula=data[0], id_recurso=data[1])

        route_change(page)
        page.close_bottom_sheet()
        page.update()

    def insert_func(_):
        route = page.route
        bottom_sheet = page.session.get("actual_form")
        data = bottom_sheet.get_fields_actual_data()
        if route == "/asignaciones":
            asignacion = Asignacion(db)
            asignacion.insert_asignacion(data[0], data[3], data[4], data[5], data[1], data[2])
        elif route == "/aulas":
            aula = Aula(db)
            aula.insert_aula(data[1],data[0],data[2])
        elif route == "/edificios":
            edificio = Edificio(db)
            edificio.insert_edificio(nombre=data[0], direccion=data[1], altura=data[2])
        elif route == "/eventos":
            evento = Evento(db)
            evento.insert_evento(nombre=data[0], descripcion=data[1], comienzo=data[2], fin=data[3])
        elif route == "/materias":
            materia = Materia(db)
            materia.insert_materia(codigo_guarani=data[0], carrera=data[1], nombre=data[2], anio=data[3], cuatrimestre=data[4], taxonomia=data[5], horas_semanales=data[6], comisiones=data[7], alumnos_esperados=data[8])
        elif route == "/profesores":
            profesor = Profesor(db)
            profesor.insert_profesor(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        elif route == "/profesores_por_materia":
            profesor_por_materia = Profesor_por_materia(db)
            profesor_por_materia.insert_profesor_por_materia(materia=data[0], profesor=data[1], cant_alumnos=data[2], tipo_clase=data[3], activo=data[4])
        elif route == "/recursos":
            recurso = Recurso(db)
            recurso.insert_recurso(nombre=data[0], descripcion=data[1])
        elif route == "/recursos_por_aula":
            recurso_por_aula = Recurso_por_aula(db)
            recurso_por_aula.insert_recurso_por_aula(id_aula=data[0], id_recurso=data[1], cantidad=data[2])

        route_change(page)
        page.close_bottom_sheet()

    def add_row_func(_):
        form = page.session.get("actual_form")
        form.build()
        textos_y_botones = form.get_fields_controls()
        if page.route != "/profesores_por_materia" and page.route != "/recursos_por_aula":
            textos_y_botones.pop(0) # remove id field
        textos_y_botones.append(
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="Guardar", bgcolor=ft.colors.BLUE_400, color=ft.colors.BLACK, icon=ft.icons.SAVE, on_click= insert_func),
                    ft.ElevatedButton(text="Cancelar", bgcolor=ft.colors.RED_400, color=ft.colors.BLACK, icon=ft.icons.CANCEL, on_click= dismiss_bottom_sheet_func),
                ]
            )
        )
        page.show_bottom_sheet(
            ft.BottomSheet(
                    ft.Container(
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls= textos_y_botones,
                            scroll=True,
                        ),
                        padding=ft.padding.only(top=10,left=10,right=10,bottom=20)
                    ),
                    dismissible= True,
                    on_dismiss= dismiss_bottom_sheet_func,
                    is_scroll_controlled=True
            )
        )
        page.update()

    def row_selected_func(data):
        delete_modify_form = page.session.get("actual_form")
        delete_modify_form.set_fields_data(data)
        delete_modify_form.build()
        id_field = delete_modify_form.get_fields_controls()[0]
        id_field.read_only = True

        textos_y_botones = delete_modify_form.get_fields_controls()
        textos_y_botones.append(
            ft.Row(
                controls=[
                    ft.ElevatedButton(text="Guardar cambios", bgcolor=ft.colors.AMBER_400, color=ft.colors.BLACK, icon=ft.icons.EDIT, on_click= update_func),
                    ft.ElevatedButton(text="Eliminar", bgcolor=ft.colors.RED_400, color=ft.colors.BLACK, icon=ft.icons.DELETE, on_click= delete_func),
                ]
            )
        )

        page.show_bottom_sheet(
            ft.BottomSheet(
                    ft.Container(
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls= textos_y_botones,
                            scroll=True,
                        ),
                        padding=ft.padding.only(top=10,left=10,right=10,bottom=20)
                    ),
                    dismissible= True,
                    on_dismiss= dismiss_bottom_sheet_func,
                    is_scroll_controlled=True
            )
        )
        page.update()

    def get_filter_tuple(_type):
        if _type == "number":
            return [ft.KeyboardType.NUMBER,ft.NumbersOnlyInputFilter()]
        elif _type == "textonly":
            return [ft.KeyboardType.TEXT,ft.TextOnlyInputFilter()]
        elif _type == "datetime":
            return [None,ft.InputFilter(allow=True, regex_string=r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", replacement_string="")]
        elif _type == "date":
            return [None,ft.InputFilter(allow=True, regex_string=r"\d{4}-\d{2}-\d{2}", replacement_string="")]
        else:
            return [None,None]

    def get_types():
        route = page.route
        types = []
        number = get_filter_tuple("number")
        text = get_filter_tuple(None)
        datetime = get_filter_tuple("datetime")
        if route == "/asignaciones":
            types = [number,number,number,number,text,number,number]
        elif route == "/aulas":
            types = [number,number,text,number]
        elif route == "/edificios":
            types = [number,text,text,number]
        elif route == "/eventos":
            types = [number,text,text,text,text]
        elif route == "/materias":
            types = [number,text,text,text,number,number,text,number,number,number]
        elif route == "/profesores":
            types = [number,number,text,text,text,text,text,text,text]
        elif route == "/profesore por materia":
            types = [number,number,number,text,text]
        elif route == "/recursos":
            types = [number,text,text]
        elif route == "/recursos por aula":
            types = [number,number,number]
        return types



    def route_change(e):
        route = e.route
        if route == "/":
            container_main_window.offset = ft.Offset(0, -0.05)
            container_main_window.content = column_main_text
            page.session.set("actual_form",None)
            page.update()
        elif route == "/asignaciones":
            container_main_window.offset = ft.Offset(0, 0)
            asignacion = Asignacion(conn= db)
            data_all_asignaciones = asignacion.get_asignaciones()
            bottom_sheet_asignaciones = DeleteModifyForm(
                fields_labels= data_all_asignaciones["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_asignaciones)
            dashboard_asignacion = Dashboard(
                dasboard_data= data_all_asignaciones,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_asignacion
            page.session.set("actual_data_table",dashboard_asignacion)
            page.update()
        elif route == "/aulas":
            container_main_window.offset = ft.Offset(0, 0)
            aula = Aula(conn= db)
            data_all_aulas = aula.get_aulas()
            bottom_sheet_aulas = DeleteModifyForm(
                fields_labels= data_all_aulas["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_aulas)
            dashboard_aula = Dashboard(
                dasboard_data= data_all_aulas,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_aula
            page.session.set("actual_data_table", dashboard_aula)
            page.update()
        elif route == "/edificios":
            container_main_window.offset = ft.Offset(0, 0)
            edificio = Edificio(conn= db)
            data_all_edificios = edificio.get_edificios()
            bottom_sheet_edificio = DeleteModifyForm(
                fields_labels= data_all_edificios["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_edificio)
            dashboard_edificio = Dashboard(
                dasboard_data= data_all_edificios,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_edificio
            page.session.set("actual_data_table", dashboard_edificio)
            page.update()
        elif route == "/eventos":
            container_main_window.offset = ft.Offset(0, 0)
            evento = Evento(conn= db)
            data_all_eventos = evento.get_eventos()
            bottom_sheet_evento = DeleteModifyForm(
                fields_labels= data_all_eventos["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_evento)
            dashboard_evento = Dashboard(
                dasboard_data= data_all_eventos,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_evento
            page.session.set("actual_data_table",dashboard_evento)
            page.update()
        elif route == "/materias":
            container_main_window.offset = ft.Offset(0, 0)
            materia = Materia(conn= db)
            data_all_materias = materia.get_materias()
            bottom_sheet_asignacion = DeleteModifyForm(
                fields_labels= data_all_materias["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_asignacion)
            dashboard_materia = Dashboard(
                dasboard_data= data_all_materias,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_materia
            page.session.set("actual_data_table", dashboard_materia)
            page.update()
        elif route == "/profesores":
            container_main_window.offset = ft.Offset(0, 0)
            profesor = Profesor(conn= db)
            data_all_profesores = profesor.get_profesores()
            bottom_sheet_profesor = DeleteModifyForm(
                fields_labels= data_all_profesores["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_profesor)
            dashboard_profesor = Dashboard(
                dasboard_data= data_all_profesores,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
            )
            container_main_window.content = dashboard_profesor
            page.session.set("actual_data_table",dashboard_profesor)
            page.window.width = 1000
            page.update()
        elif route == "/profesor por materia":
            container_main_window.offset = ft.Offset(0, 0)
            profesor_por_materia = Profesor_por_materia(conn= db)
            data_all_profesores_por_materias = profesor_por_materia.get_profesores_por_materia()
            bottom_sheet_profesor_por_materia = DeleteModifyForm(
                fields_labels= data_all_profesores_por_materias["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_profesor_por_materia)
            dashboard_profesor_por_materia = Dashboard(
                dasboard_data= data_all_profesores_por_materias,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_profesor_por_materia
            page.session.set("actual_data_table",dashboard_profesor_por_materia)
            page.update()
        elif route == "/recursos":
            container_main_window.offset = ft.Offset(0, 0)
            recurso = Recurso(conn= db)
            data_all_recursos = recurso.get_recursos()
            bottom_sheet_recursos = DeleteModifyForm(
                fields_labels= data_all_recursos["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_recursos)
            dashboard_recurso = Dashboard(
                dasboard_data= data_all_recursos,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_recurso
            page.session.set("actual_data_table",dashboard_recurso)
            page.update()
        elif route == "/recursos por aula":
            container_main_window.offset = ft.Offset(0, 0)
            recurso_por_aula = Recurso_por_aula(conn= db)
            data_all_recursos_por_aulas = recurso_por_aula.get_recursos_por_aula()
            bottom_sheet_recurso_por_aula = DeleteModifyForm(
                fields_labels= data_all_recursos_por_aulas["columns"],
                fields_types = get_types()
            )
            page.session.set("actual_form",bottom_sheet_recurso_por_aula)
            dashboard_recurso_por_aula = Dashboard(
                dasboard_data= data_all_recursos_por_aulas,
                rows_func=row_selected_func,
                button_add_func= add_row_func,
                expand=True,
                border_radius= 10,
                bgcolor= "#3A3A3A",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_recurso_por_aula
            page.session.set("actual_data_table",dashboard_recurso_por_aula)
            page.update()

        elif route == "/ver_horarios":
            listas_busquedas["search_bar_carrera"].clear()
            listas_busquedas["search_bar_edificio"].clear()
            listas_busquedas["search_bar_aula"].clear()
            load_search_bars()
            container_main_window.offset = ft.Offset(0, 0)
            crear_visualizacion_horarios()
            container_main_window.content = container_vista_horarios
            page.update()


    ###################################################################################
    #                                     HEADER                                      #
    ###################################################################################
    text_header_UNRN = ft.Text(
        value="UNRN",
        color="#FFFFFF",
        size=25,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        font_family="FabrikatNormalBlack",
    )

    text_header_UNRN_description = ft.Text(
        value="Universidad Nacional\nde Río Negro",
        color="#FFFFFF",
        size=10,
        weight=ft.FontWeight.W_500,
        text_align=ft.TextAlign.CENTER,
        font_family="DelaGothicOne",
    )

    row_header = ft.Row(
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            text_header_UNRN,
            text_header_UNRN_description
        ]
    )

    ###################################################################################
    #                              MAIN TEXT AND BUTTON                               #
    ###################################################################################

    text_main_sede_andina = ft.Text(
        value="SEDE ANDINA",
        color="#FFFFFF",
        size=10,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        font_family="FabrikatNormal",
    )

    text_main_AULA = ft.Text(
        value="AULA",
        color="#EB2141",
        size=60,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        font_family="FabrikatNormal",
    )

    text_main_AULA_description = ft.Text(
        value="Administración Unificada\nde Lugares Académicos",
        color="#C4C4C4",
        size=10,
        weight=ft.FontWeight.NORMAL,
        font_family="FabrikatNormal",
    )

    btn_main_horarios = ft.OutlinedButton(
        text="Ver Horarios",
        icon=ft.icons.CALENDAR_MONTH,
        height=50,
        width=200,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(
                radius=ft.border_radius.all(5)
            ),
            color="#C4C4C4",
            bgcolor=ft.colors.with_opacity(0.25,"#505050"),
        ),
        on_click=lambda _: page.go('/ver_horarios')
    )

    column_main_text = ft.Column(
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            row_header,
            text_main_sede_andina,
            ft.Container(
                content=text_main_AULA,
                border=ft.Border(
                    top=ft.BorderSide(width=1,color=ft.colors.with_opacity(0.5,"#C4C4C4")),
                    bottom=ft.BorderSide(width=1,color=ft.colors.with_opacity(0.5,"#C4C4C4"))
                ),
            ),
            text_main_AULA_description,
            btn_main_horarios
        ]
    )

    ###################################################################################
    #                                  VER HORARIOS                                   #
    ###################################################################################

    listas_busquedas = {
        "search_bar_carrera":[],
        "search_bar_edificio":[],
        "search_bar_aula":[]
    }

    btn_ordenar_auto = ft.ElevatedButton(
        text="Ordenar automaticamente",
        on_click=lambda _: print("Ordenar automaticamente [hacer funcion]")
    )

    search_bar_carrera = ft.SearchBar(
        data="search_bar_carrera",
        expand=True,
        expand_loose=True,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Carrera",
        view_hint_text="Seleccione una carrera para filtrar los datos",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=listas_busquedas["search_bar_carrera"],
    )

    search_bar_aula = ft.SearchBar(
        data="search_bar_aula",
        expand=True,
        expand_loose=True,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Aula",
        view_hint_text="Seleccione un aula para filtrar los datos",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=listas_busquedas["search_bar_aula"],
    )

    search_bar_edificio = ft.SearchBar(
        data="search_bar_edificio",
        expand=True,
        expand_loose=True,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Edificio",
        view_hint_text="Seleccione un edificio para filtrar los datos",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=listas_busquedas["search_bar_edificio"],
    )

    columns_search_bars = ft.Column(
        controls=[
            ft.Row(controls=[search_bar_carrera, btn_ordenar_auto]),
            ft.Row(controls=[search_bar_edificio, search_bar_aula])
        ]
    )

    container_horarios = ft.Container(
        expand=True,
        bgcolor=ft.colors.GREY_800,
    )

    container_vista_horarios = ft.Container(
        expand=True,
        bgcolor=ft.colors.with_opacity(0.75,"#3A3A3A"),
        padding=10,
        content=ft.Column(
            controls=[columns_search_bars,
            container_horarios]
        ),
    )

    ###################################################################################
    #                              CONTENEDOR PRINCIPAL                               #
    ###################################################################################

    container_main_window = ft.Container(
        content=column_main_text,
        alignment=ft.alignment.center,
        padding=ft.padding.all(10),
    )

    ###################################################################################
    #                                   NAVEGACION                                    #
    ###################################################################################
    custom_rail_bar = ft.NavigationRail(
        width=100,
        on_change= navigation_change,
        group_alignment=0,
        destinations=[
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.HOME_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.HOME),
                label="Inicio",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PEOPLE_OUTLINE),
                selected_icon_content=ft.Icon(ft.icons.PEOPLE),
                label="Profesores",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.CLASS_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.CLASS_),
                label="Materias",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.WORK_HISTORY_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.WORK_HISTORY),
                label="Profesor por materia",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.CALENDAR_MONTH),
                label="Eventos",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.MEETING_ROOM_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.MEETING_ROOM),
                label="Aulas",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.EDIT_CALENDAR_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.EDIT_CALENDAR),
                label="Asignaciones",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PRECISION_MANUFACTURING_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.PRECISION_MANUFACTURING),
                label="Recursos",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.WORKSPACES_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.WORKSPACES),
                label="Recursos por aula",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.LOCATION_CITY_OUTLINED),
                selected_icon_content=ft.Icon(ft.icons.LOCATION_CITY),
                label="Edificios",
            ),
        ]
    )
    ###################################################################################
    #                                   BACKGROUND                                    #
    ###################################################################################
    container_main_background_decorator = ft.Container(
        rotate= ft.transform.Rotate(angle=0.785),
        shadow=ft.BoxShadow(
            blur_radius=30,
            spread_radius=10,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.INNER,
            color="#EB2141",
        ),
        width=400,
        height=400,
        right=-200,
        bottom=-200,
    )

    main_stack = ft.Stack(
        expand=True,
        controls=[
            container_main_background_decorator,
            container_main_window,
        ],
    )

    main_container_page = ft.Container(
        alignment=ft.alignment.center,
        image_src="assets/Group_2.png",
        image_fit=ft.ImageFit.FILL,
        expand=True,
        content=ft.Row(
            controls=[
                custom_rail_bar,
                main_stack
            ]
        )
    )

    page.on_route_change = route_change
    page.go("/")
    page.add(main_container_page)

ft.app(main)
