from typing import Any, List, Tuple, Dict, Literal, Callable
import flet as ft
from flet_core.gradients import Gradient
# from Data_table import DataTableCustom  # Para probar el archivo, descomentar esta linea
from .Data_table import DataTableCustom


class Dashboard(ft.Container):
    def __init__(
        self,
        dasboard_data : Dict[Literal['columns', 'rows'], List[Any]] = {'columns': [], 'rows': []},
        rows_func : Callable = None,
        button_add_func : Callable = None,
        form_fields : list[str] = [],
        form_header_controls : list[ft.Control] = [],
        form_text_color : str = "#000000",
        content: ft.Control | None = None,
        ref: ft.Ref | None = None,
        key: str | None = None,
        width: None | int | float = None,
        height: None | int | float = None,
        left: None | int | float = None,
        top: None | int | float = None,
        right: None | int | float = None,
        bottom: None | int | float = None,
        expand: None | bool | int = None,
        col: Dict[str, int | float] | int | float | None = None,
        opacity: None | int | float = None,
        rotate: None | int | float | ft.Rotate = None,
        scale: None | int | float | ft.Scale = None,
        offset: None | ft.Offset | Tuple[float | int, float | int] = None,
        aspect_ratio: None | int | float = None,
        animate_opacity: None | bool | int | ft.Animation = None,
        animate_size: None | bool | int | ft.Animation = None,
        animate_position: None | bool | int | ft.Animation = None,
        animate_rotation: None | bool | int | ft.Animation = None,
        animate_scale: None | bool | int | ft.Animation = None,
        animate_offset: None | bool | int | ft.Animation = None,
        on_animation_end=None,
        tooltip: str | None = None,
        visible: bool | None = None,
        disabled: bool | None = None,
        data: Any = None,
        padding: None | int | float | ft.Padding = None,
        margin: None | int | float | ft.Margin = None,
        alignment: ft.Alignment | None = None,
        bgcolor: str | None = None,
        gradient: Gradient | None = None,
        blend_mode: ft.BlendMode = None,
        border: ft.Border | None = None,
        border_radius: None | int | float | ft.BorderRadius = None,
        image_src: str | None = None,
        image_src_base64: str | None = None,
        image_repeat: ft.ImageRepeat | None = None,
        image_fit: ft.ImageFit | None = None,
        image_opacity: None | int | float = None,
        shape: ft.BoxShape | None = None,
        clip_behavior: ft.ClipBehavior | None = None,
        ink: bool | None = None,
        animate: None | bool | int | ft.Animation = None,
        blur: None | float | int | Tuple[float | int,
        float | int] | ft.Blur = None,
        shadow: None | ft.BoxShadow | List[ft.BoxShadow] = None,
        url: str | None = None,
        url_target: str | None = None,
        theme: ft.Theme | None = None,
        theme_mode: ft.ThemeMode | None = None,
        on_click=None,
        on_long_press=None,
        on_hover=None):
        # Setting variables
        super().__init__(content=content, padding=padding, ref=ref, key=key, width=width, height=height, left=left, top=top, right=right, bottom=bottom, expand=expand, col=col, opacity=opacity, rotate=rotate, scale=scale, offset=offset, aspect_ratio=aspect_ratio, animate_opacity=animate_opacity, animate_size=animate_size, animate_position=animate_position, animate_rotation=animate_rotation, animate_scale=animate_scale, animate_offset=animate_offset, on_animation_end=on_animation_end, tooltip=tooltip, visible=visible, disabled=disabled, data=data, margin=margin, alignment=alignment, bgcolor=bgcolor, gradient=gradient, blend_mode=blend_mode, border=border, border_radius=border_radius, image_src=image_src, image_src_base64=image_src_base64, image_repeat=image_repeat, image_fit=image_fit, image_opacity=image_opacity, shape=shape, clip_behavior=clip_behavior, ink=ink, animate=animate, blur=blur, shadow=shadow, url=url, url_target=url_target, theme=theme, theme_mode=theme_mode, on_click=on_click, on_long_press=on_long_press, on_hover=on_hover)
        self.expand = True
        self.dashboard_data = dasboard_data
        self.form_fields = form_fields
        self.form_header_controls = form_header_controls
        self.form_text_color = form_text_color
        self.rows_func = rows_func
        self.button_add_func = button_add_func
        self.dashboard_search_input = ft.TextField(label="Search", col=1, color=self.form_text_color, height=50, expand=True, on_change=self.__input_changed)
        self.dashboard_buttond_add_row = ft.IconButton(icon=ft.icons.ADD, on_click= self.button_add_func, width=50, height=50)
        self.data_table = DataTableCustom(
            data_columns = self.dashboard_data["columns"],
            data_rows= self.dashboard_data["rows"],
            rows_func= self.rows_func
        )
        self.content= ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(controls=[self.dashboard_search_input, self.dashboard_buttond_add_row]),
                ft.Row(
                    #scroll=ft.ScrollMode.AUTO,
                    controls=[self.data_table.build()]
                ),
            ],
        )

    # TODO: Hacer que solo filtre las filas
    def __input_changed(self, e):
        # search_filter= e.control.value
        # filtered_rows = list(filter(lambda x: search_filter in x, self.data_table.getRows()))
        pass

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