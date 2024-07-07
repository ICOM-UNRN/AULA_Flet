from typing import Any, List, Tuple, Dict, Literal
import flet as ft
from flet_core.gradients import Gradient
# from Data_table import DataTableCustom  # Para probar el archivo, descomentar esta linea
from .Data_table import DataTableCustom


class Dashboard(ft.Container):
    def __init__(
        self,
        dasboard_data : Dict[Literal['columns', 'rows'], List[Any]] = {'columns': [], 'rows': []},
        form_fields : list[str] = [],
        form_text_color : str = "#000000",
        content: ft.Control | None = None,ref: ft.Ref | None = None,
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
        blend_mode: ft.BlendMode = ft.BlendMode.NONE,
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
        super().__init__(content, ref, key, width, height, left, top, right, bottom, expand, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data, padding, margin, alignment, bgcolor, gradient, blend_mode, border, border_radius, image_src, image_src_base64, image_repeat, image_fit, image_opacity, shape, clip_behavior, ink, animate, blur, shadow, url, url_target, theme, theme_mode, on_click, on_long_press, on_hover)
        self.expand = True
        self.dashboard_data = dasboard_data
        self.form_fields = form_fields
        self.form_text_color = form_text_color
        self.data_table = DataTableCustom(
            data_columns = self.dashboard_data["columns"],
            data_rows= self.dashboard_data["rows"]
        )
        self.content= ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
            controls=ft.Row(
                on_scroll=ft.ScrollMode.HIDDEN,
                controls=[self.data_table.build()]
            ),
        )
        self.create_textfield()

    def create_textfield(self):
        temp = self.content.controls.copy()[0]
        self.content.controls = []
        for text in self.form_fields:
            self.content.controls.append(ft.TextField(label=text, col=1, color=self.form_text_color, height=50))
        self.content.controls.append(temp)
            
        ...

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