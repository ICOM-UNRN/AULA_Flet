from typing import Any, List, Dict, Tuple
import flet as ft

class DeleteModifyForm(ft.UserControl):
    def __init__(
        self,
        fields_labels : List[str],
        fields_types : List[str],
        fields_data : List[int | str | float] = [],
        controls: List[ft.Control] | None = None,
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
        visible: bool | None = None,
        disabled: bool | None = None,
        data: Any = None,
        clip_behavior: ft.ClipBehavior | None = None
    ):
        super().__init__(
            controls,
            ref,
            key,
            width,
            height,
            left,
            top,
            right,
            bottom,
            expand,
            col,
            opacity,
            rotate,
            scale,
            offset,
            aspect_ratio,
            animate_opacity,
            animate_size,
            animate_position,
            animate_rotation,
            animate_scale,
            animate_offset,
            on_animation_end,
            visible,
            disabled,
            data,
            clip_behavior
        )
        self.fields_labels : List[str] = fields_labels
        self.fields_controls : List[ft.TextField] = []
        self.fields_data : List[int | str | float] = fields_data
        self.fields_types : List[str] = fields_types

# Terminar de armar la logica para obtener los textos pasados y
# devolver un BottomSheet para la Modificacion y Baja de los registros.
    def build(self):
        """Funcion que construye el BottomSheet"""
        if len(self.fields_labels)>0:
            if len(self.fields_data)>0:
                for label, data, _type in zip(self.fields_labels, self.fields_data, self.fields_types):
                    if _type[0] == "id":
                        self.fields_controls.append(
                            ft.Dropdown(
                                label= label,
                                value= data
                            )
                        )
                    else:
                        self.fields_controls.append(
                            ft.TextField(
                                label= label,
                                col={"md": 1},
                                value=data,
                                keyboard_type=_type[0],
                                input_filter=_type[1]
                            )
                    )
            else:
                for label, _type in zip(self.fields_labels,self.fields_types):
                    if _type[0] == "id":
                        self.fields_controls.append(
                            ft.Dropdown(
                                label= label
                            )
                        )
                    else:
                        self.fields_controls.append(
                            ft.TextField(
                                label= label,
                                col={"md": 1},
                                keyboard_type=_type[0],
                                input_filter=_type[1]
                            )
                    )
        return self.fields_controls

    def get_fields_controls(self):
        """Returns a list of TextField controls"""
        return self.fields_controls

    def get_fields_data(self):
        """Returns a list of TextField data"""
        return self.fields_data
    
    def get_fields_actual_data(self):
        """Returns a list of each control updated TextField data"""
        result = []
        for field in self.fields_controls:
            if field.__class__ == ft.TextField:
                if field.data == None:
                    result.append(field.value)
                else:
                    result.append(field.data)
            elif field.__class__ == ft.Dropdown:
                result.append(field.value)
        return result


    def get_fields_labels(self):
        """Returns a list of TextField labels"""
        return self.fields_labels

    def set_fields_data(self, data : List[int | str | float]):
        """
        Set the data of the fields.
        
        Args:
            data (List[int | str | float]): The data to be set.
        """
        self.fields_data = data
    
    def clear_fields(self):
        self.fields_controls.clear()
        self.fields_data.clear()
