import flet as ft
#from AULA.api.materia.materia import Materia
from components.dashboard.Dashboard import Dashboard
from components.RailBar.Railbar import RailBarCustom
from api.db import get_db
from api.aula.aula import Aula
from api.materia.materia import Materia
from api.asignacion.asignacion import Asignacion
from api.edificio.edificio import Edificio
from api.evento.evento import Evento
from api.materia.materia import Materia
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
    
    AULA_DB = get_db()
    
    ###################################################################################
    #                                  CAMBIO DE RUTAS                                #
    ###################################################################################
    def navigation_change(e):
        destination = e.control.destinations[int(e.data)].label
        if destination == "Inicio":
            page.go("/")
        else:
            page.go(f"/{destination.lower()}")
    def route_change(e):
        route = e.route
        if route == "/":
            container_main_window.offset = ft.Offset(0, -0.05)
            container_main_window.content = column_main_text
            page.update()
        elif route == "/asignaciones":
            container_main_window.offset = ft.Offset(0, 0)
            asignacion = Asignacion(conn= AULA_DB)
            data_all_asignaciones = asignacion.get_asignaciones()
            dashboard_asignacion = Dashboard(
                dasboard_data= data_all_asignaciones,
                expand=True,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_asignacion
            page.update()
        elif route == "/aulas":
            container_main_window.offset = ft.Offset(0, 0)
            aula = Aula(conn= AULA_DB)
            data_all_aulas = aula.get_aulas()
            dashboard_aula = Dashboard(
                dasboard_data= data_all_aulas,
                expand=True,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_aula
            page.update()
        elif route == "/edificios":
            container_main_window.offset = ft.Offset(0, 0)
            edificio = Edificio(conn= AULA_DB)
            data_all_edificios = edificio.get_edificios()
            dashboard_edificio = Dashboard(
                dasboard_data= data_all_edificios,
                expand=True,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_edificio
            page.update()
        elif route == "/eventos":
            container_main_window.offset = ft.Offset(0, 0)
            evento = Evento(conn= AULA_DB)
            data_all_eventos = evento.get_eventos()
            dashboard_evento = Dashboard(
                dasboard_data= data_all_eventos,
                width= 600,
                height= 600,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_evento
            page.update()
        elif route == "/materias":
            container_main_window.offset = ft.Offset(0, 0)
            materia = Materia(conn= AULA_DB)
            data_all_materias = materia.get_materias()
            dashboard_materia = Dashboard(
                dasboard_data= data_all_materias,
                expand=True,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_materia
            page.update()
        elif route == "/profesores":
            container_main_window.offset = ft.Offset(0, 0)
            profesor = Profesor(conn= AULA_DB)
            data_all_profesores = profesor.get_profesores()
            dashboard_profesor = Dashboard(
                dasboard_data= data_all_profesores,
                expand=True,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_profesor
            page.update()
        elif route == "/profesores_por_materia":
            container_main_window.offset = ft.Offset(0, 0)
            profesor_por_materia = Profesor_por_materia(conn= AULA_DB)
            data_all_profesores_por_materias = profesor_por_materia.get_profesores_por_materia()
            dashboard_profesor_por_materia = Dashboard(
                dasboard_data= data_all_profesores_por_materias,
                expand=True,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_profesor_por_materia
            page.update()
        elif route == "/recursos":
            container_main_window.offset = ft.Offset(0, 0)
            recurso = Recurso(conn= AULA_DB)
            data_all_recursos = recurso.get_recursos()
            dashboard_recurso = Dashboard(
                dasboard_data= data_all_recursos,
                expand=True,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_recurso
            page.update()
        elif route == "/recursos_por_aula":
            container_main_window.offset = ft.Offset(0, 0)
            recurso_por_aula = Recurso_por_aula(conn= AULA_DB)
            data_all_recursos_por_aulas = recurso_por_aula.get_recursos_por_aula()
            dashboard_recurso_por_aula = Dashboard(
                dasboard_data= data_all_recursos_por_aulas,
                expand=True,
                border_radius= 10,
                bgcolor= "#E6E6E6",
                padding= 10,
                form_fields=["Search"],
            )
            container_main_window.content = dashboard_recurso_por_aula
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
        top=0,
        left=20,
        expand=True,
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
        on_click=lambda _: page.go('/profesores'),
    )

    column_main_text = ft.Column(
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
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
    custom_rail_bar = RailBarCustom(
        width=80,
        on_change=lambda e: navigation_change(e),
        rail_destinations=[
            {
                'label': 'Inicio',
                'icon': ft.icons.HOME_OUTLINED,
                'selected_icon': ft.icons.HOME
            },
            {
                'label': 'Profesores',
                'icon': ft.icons.PEOPLE_OUTLINE,
                'selected_icon': ft.icons.PEOPLE
            },
            {
                'label': 'Materias',
                'icon': ft.icons.CLASS_OUTLINED,
                'selected_icon': ft.icons.CLASS_
            },
            {
                'label': 'Aulas',
                'icon': ft.icons.MEETING_ROOM_OUTLINED,
                'selected_icon': ft.icons.MEETING_ROOM
            }
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
            row_header,
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