from typing import Any, List, Dict, Tuple
import flet as ft

class RailBarCustom(ft.NavigationRail):
    def __init__(
        self,
        rail_destinations : list[dict] = [],
        ref: ft.Ref | None = None,
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
        destinations: List[ft.NavigationRailDestination] | None = None,
        selected_index: int | None = None,
        extended: bool | None = None,
        label_type: ft.NavigationRailLabelType | None = None,
        bgcolor: str | None = None,
        leading: ft.Control | None = None,
        trailing: ft.Control | None = None,
        min_width: None | int | float = None,
        min_extended_width: None | int | float = None,
        group_alignment: None | int | float = None,
        on_change=None
    ):
        super().__init__(
            ref,
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
            destinations,
            selected_index,
            extended,
            label_type,
            bgcolor,
            leading,
            trailing,
            min_width,
            min_extended_width,
            group_alignment,
            on_change
        )
        self.rail_destinations : list = rail_destinations
        self.destinations : list = [
            ft.NavigationRailDestination(
                icon=new_destination['icon'],
                selected_icon=new_destination['selected_icon'],
                label=new_destination['label']
            )  for new_destination in self.rail_destinations
        ]
        pass
    
    def __create_destinations(self):
        if len(self.destinations) > 0:
            for destination in self.rail_destinations:
                new_destination = ft.NavigationRailDestination(
                    icon=destination['icon'],
                    selected_icon=destination['selected_icon'],
                    label=destination['label']
                )
                self.destinations.append(destination)
    def build(self):
        self.__create_destinations()
    
def main(page: ft.Page):
    custom_rail_bar = RailBarCustom(
        expand=True,
        rail_destinations=[
            {
                'label': 'Home',
                'icon': ft.icons.HOME,
                'selected_icon': ft.icons.HOME
            },
            {
                'label': 'Settings',
                'icon': ft.icons.SETTINGS,
                'selected_icon': ft.icons.SETTINGS
            },
            {
                'label': 'Help',
                'icon': ft.icons.HELP,
                'selected_icon': ft.icons.HELP
            }
        ]
    )
    page.add(custom_rail_bar)

if __name__ == '__main__':
    ft.app(target=main)