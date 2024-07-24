import logging
import flet as ft
from flet import (
    ScrollMode,
    Page,
    DragTarget,
    Draggable,
    Container,
    Column,
    Row,
    Text,
    TextButton,
    Icon,
    TextField,
    UserControl,
    Card,
    icons,
    border_radius,
    border,
    alignment,
    colors,
    padding,
)

class ItemList(UserControl):

    def __init__(self, page, list_name, color = "black"):
        super().__init__()
        self.page = page
        self.list_name: str = list_name
        self.list_color = color
        self.items = Column(controls=[], tight=True, spacing=5, wrap=True)
        self.end_indicator = Container(
            bgcolor=colors.BLACK26,
            border_radius=border_radius.all(30),
            height=3,
            width=100,
            opacity=0.0
        )
        self.item_name = TextField(
            label="New Item Name", width=100, height=50, bgcolor=colors.WHITE, on_submit=self.add_item_handler)

    def build(self):
        self.view = Container(#Draggable(
            #group="lists",
            content=DragTarget(
                group="items",
                content=DragTarget(
                    group="lists",
                    content=Container(
                        content=Column([
                            self.item_name,
                            TextButton("Add Item", icon=icons.ADD, on_click=self.add_item_handler),
                            TextButton("Delete Items on this list", icon=icons.DELETE_FOREVER, on_click=self.delete_items_handler),
                            TextButton("Modify item on this list", icon=icons.SCREEN_ROTATION_ALT, on_click=self.modify_items_handler),
                            self.items,
                            self.end_indicator
                        ], spacing=4, tight=True, expand=True),
                        border=border.all(2, colors.BLACK12),
                        border_radius=border_radius.all(15),
                        bgcolor=self.list_color,
                        padding=padding.all(20),
                    ),
                    data=self,
                    on_accept=self.drag_accept,
                    on_will_accept=self.drag_will_accept,
                    on_leave=self.drag_leave
                ),
                data=self,
                on_accept=self.item_drag_accept,
                on_will_accept=self.item_drag_will_accept,
                on_leave=self.item_drag_leave
            )
        )
        return self.view

    def add_item_handler(self, e):
        self.add_item()

    def delete_items_handler(self, e):
        self.items.controls = []
        self.view.update()

    def modify_items_handler(self, e):
        if len(self.items.controls) == 0:
            print("mcnvcmnvmcvnmcnvmcc")
        else:
            print(self.items.controls[0])
        self.view.update()


    def add_item(self, item: str = None, chosen_control: Draggable = None, swap_control: Draggable = None):
        controls_list = [x.controls[1] for x in self.items.controls]
        to_index = controls_list.index(
            swap_control) if swap_control in controls_list else None
        from_index = controls_list.index(
            chosen_control) if chosen_control in controls_list else None
        control_to_add = Column([
            Container(
                bgcolor=colors.BLACK26,
                border_radius=border_radius.all(30),
                height=3,
                alignment=alignment.center_right,
                width=100,
                opacity=0.0
            )
        ])

        # rearrange (i.e. drag drop from same list)
        if ((from_index is not None) and (to_index is not None)):
            print("rearrange: ", to_index, from_index)
            self.items.controls.insert(
                to_index, self.items.controls.pop(from_index))
            self.set_indicator_opacity(swap_control, 0.0)

        # insert (drag from other list to middle of this list)
        elif (to_index is not None):
            print("insert: ", to_index)
            new_item = Item(self, item)
            control_to_add.controls.append(new_item.view)
            self.items.controls.insert(to_index, control_to_add)

        # add new (drag from other list to end of this list, or use add item button)
        else:
            print("add new: ", item)
            new_item = Item(self, item) if item else Item(
                self, self.item_name.value) #self, self.item_name.value)
            control_to_add.controls.append(new_item.view)
            self.items.controls.append(control_to_add)
            self.item_name.value = ""

        print("self.items: ", self.items.controls)
        self.view.update()
        self.page.update()

    def set_indicator_opacity(self, item, opacity):
        controls_list = [x.controls[1] for x in self.items.controls]
        self.items.controls[controls_list.index(
            item)].controls[0].opacity = opacity
        self.view.update()

    def remove_item(self, item):
        controls_list = [x.controls[1] for x in self.items.controls]
        del self.items.controls[controls_list.index(item)]
        self.view.update()

    def drag_accept(self, e):
        src = self.page.get_control(e.src_id)
        l = self.page.item_lists.controls
        to_index = l.index(e.control.data)
        from_index = l.index(src.content.data)
        l[to_index], l[from_index] = l[from_index], l[to_index]
        self.end_indicator.opacity = 0.0
        # self.update()
        self.page.update()

    def drag_will_accept(self, e):
        self.end_indicator.opacity = 0.0
        self.page.update()

    def drag_leave(self, e):
        self.end_indicator.opacity = 0.0
        self.page.update()

    def item_drag_accept(self, e):
        src = self.page.get_control(e.src_id)
        self.add_item(src.data.item_text)
        src.data.list.remove_item(src)
        self.end_indicator.opacity = 0.0
        self.update()

    def item_drag_will_accept(self, e):
        self.end_indicator.opacity = 1.0
        self.update()

    def item_drag_leave(self, e):
        self.end_indicator.opacity = 0.0
        self.update()

class ItemList_Days(ItemList):
    def __init__(self, page, list_name, color=None):
        super().__init__(page, list_name, color)
        self.items = Column([], tight=True, spacing=5)
        self.item_name = Text(f"")

    def build(self):
        self.view = Container(#Draggable(
                #group="lists",
                content=DragTarget(
                    group="items",
                    content=DragTarget(
                        group="lists",
                        content=Container(
                            content=Column([
                                self.items,
                                self.end_indicator
                            ], spacing=4, tight=True, expand=True),
                            border=border.all(2, colors.BLACK12),
                            border_radius=border_radius.all(10),
                            bgcolor=self.list_color,
                            padding=padding.all(5),
                        ),
                        data=self,
                        on_accept=self.drag_accept,
                        on_will_accept=self.drag_will_accept,
                        on_leave=self.drag_leave
                    ),
                    data=self,
                    on_accept=self.item_drag_accept,
                    on_will_accept=self.item_drag_will_accept,
                    on_leave=self.item_drag_leave
                )
            )
        return self.view    

class Item():

    def __init__(self, list: ItemList, item_text: str = None):

        profesor = Text(value=list.item_name.value)
        horario = Text(value=f"* Horario: *", size=10)
        #datos = Text(value=f"* [insertar mas elementos...] *")
        #mas_datos = Text(value=f"* {datos.value} :: {len(datos.value)} *")

        #longer_length = max(len(profesor.value), len(datos.value))

        self.list = list
        self.item_text = item_text
        self.card_item = Card(
            content=Container(
                content=Column([
                    Row([
                        Icon(name=icons.HOURGLASS_BOTTOM),
                        Text(value=f"{self.item_text}"),
                    ]),
                    horario,
                    #datos,
                    #mas_datos,
                ],
                    alignment="start",
                ),
                width= 110, #100 + longer_length,
                padding=7
            ),
            elevation=1,
            data=self.list
        )
        self.view = Draggable(
            group="items",
            content=DragTarget(
                group="items",
                content=self.card_item,
                on_accept=self.drag_accept,
                on_leave=self.drag_leave,
                on_will_accept=self.drag_will_accept,
            ),
            data=self

        )

    def drag_accept(self, e):
        # this is the item picked up (Draggable control)
        src = self.list.page.get_control(e.src_id)

        # e.control is the DragTarget, i.e. This (self) Item in the list
        # skip if item is dropped on itself
        if (src.content.content == e.control.content):
            e.control.content.elevation = 1
            self.list.set_indicator_opacity(self.view, 0.0)
            e.control.update()
            return

        # item dropped within same list but not on self
        if (src.data.list == self.list):
            self.list.add_item(chosen_control=src,
                               swap_control=self.view)
            self.list.set_indicator_opacity(self.view, 0.0)
            e.control.content.elevation = 1
            e.control.update()
            return

        # item added to different list
        self.list.add_item(src.data.item_text, swap_control=self.view)
        # remove from the list to which draggable belongs
        src.data.list.remove_item(src)
        self.list.set_indicator_opacity(self.view, 0.0)
        e.control.content.elevation = 1
        e.control.update()

    def drag_will_accept(self, e):
        self.list.set_indicator_opacity(self.view, 1.0)
        e.control.content.elevation = 20 if e.data == "true" else 1
        e.control.update()

    def drag_leave(self, e):
        self.list.set_indicator_opacity(self.view, 0.0)
        e.control.content.elevation = 1
        e.control.update()


def create_calendar_table_headers_first_row(headers : list):
    encabezados = []
    for i in headers:
        encabezados.append(ft.DataColumn(ft.Text(f"{i}")))
    return encabezados

def create_calendar_rows(rows, columns, page, color="white"):
    filas = []
    for i in range(0, len(rows)):
        celdas = []
        celdas.append(ft.DataCell(ft.Text(f"{rows[i]}")))
        for j in range(1, len(columns)):
            celdas.append(ft.DataCell(ItemList_Days(page, f"A{i}{j}", color)))
        filas.append(ft.DataRow(cells=celdas))
    return filas

def create_calendar_hours_intervals(inicio : int, final : int):
    columna = []
    for i in range(inicio, final):
        columna.append(f"{i} -> {i+1}")
    return columna

def main(page: ft.Page):
    dias = ["_________", "_Lunes_", "_Martes_", "_Miercoles_", "_Jueves_", "_Viernes_", "_Sabado_", "_Domingo_"]
    intervalos_horarios = create_calendar_hours_intervals(8, 23)

    item1 = ItemList(page, "Primer_ItemList")

    page.add(Column([
            Row([
                Container(item1),
                Column([ft.DataTable(
                    columns=create_calendar_table_headers_first_row(dias),
                    rows=create_calendar_rows(intervalos_horarios,dias,page),
                    data_row_min_height = 50,
                    data_row_max_height = float("inf"),
                    bgcolor='#ffffff',),
                    ],
                scroll=ScrollMode.ADAPTIVE,
                expand=True,
                alignment="start",)
            ], 
            vertical_alignment="start",
            scroll=ScrollMode.ALWAYS,)
        ], expand=True,
           alignment="start",
           scroll=ScrollMode.ALWAYS,))
    

ft.app(target=main)