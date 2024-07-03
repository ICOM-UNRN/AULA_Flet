import flet as ft

def main(page: ft.Page):

    page.add(
        ft.Container(
            border_radius=10,
            width=100,
            height=100,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.INNER,
            )
        )
    )

ft.app(target=main)