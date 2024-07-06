import flet as ft
from components.dashboard.Dashboard import Dashboard
from api.db import get_db
from api.profesor.profesor import Profesor

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
    
    def route_change(e):
        route = e.route
        if route == "/":
            container_main_window.content = column_main_text
            page.update()
        elif route == "/profesores":
            profesor = Profesor(conn= AULA_DB)
            all_profesores = profesor.get_profesores()
            dashboard_profesor = Dashboard(all_profesores)
            container_main_window.content = dashboard_profesor
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
        offset=ft.Offset(0, -0.05),
        alignment=ft.alignment.center,
        padding=ft.padding.all(10),
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
    
    container_main_background = ft.Container(
        expand=True,
        image_src="assets/Group_2.png",
        image_fit=ft.ImageFit.FILL,
    )
    
    main_stack = ft.Stack(
        expand=True,
        controls=[
            container_main_background,
            container_main_background_decorator,
            container_main_window,
            row_header,
        ],
    )
    page.on_route_change = route_change
    page.go("/")
    page.add(main_stack)

ft.app(main)