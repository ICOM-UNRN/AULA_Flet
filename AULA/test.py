import re
import flet as ft
def main(page):

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

    listas_busquedas = {
        "search_bar_carrera":[
            ft.ListTile(title=ft.Text("Ingenieria en Computacion"), on_click=close_search_bar_carrera)
        ],
        "search_bar_edificio":[
            ft.ListTile(title=ft.Text("Anasagasti 2"), on_click=close_search_bar_edifico),
            ft.ListTile(title=ft.Text("Tacuari"), on_click=close_search_bar_edifico),
            ft.ListTile(title=ft.Text("Mitre"), on_click=close_search_bar_edifico)
        ],
        "search_bar_aula":[
            ft.ListTile(title=ft.Text("Aula 1"), on_click=close_search_bar_aula),
            ft.ListTile(title=ft.Text("Aula 2"), on_click=close_search_bar_aula),
            ft.ListTile(title=ft.Text("Aula 3"), on_click=close_search_bar_aula)
        ]
    }

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

    btn_ordenar_auto = ft.ElevatedButton(text="Ordenar automaticamente", on_click=lambda _: print("Ordenar automaticamente [hacer funcion]"))

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
        content=ft.Column(
            controls=[columns_search_bars,
            container_horarios]
        )
    )

    page.add(container_vista_horarios)

ft.app(target=main)
