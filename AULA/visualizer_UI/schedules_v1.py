import logging
import flet as ft
from flet import (
    Margin,
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
    def __init__(self, page, list_name, color="red"):
        super().__init__()
        self.page = page
        self.list_name = list_name
        self.list_color = color
        self.items = Column(
            controls=[],
            tight=True,
            spacing=5,
            wrap=True,
            run_spacing=10,
            width=250
        )
        self.items_info_pura = []
        self.end_indicator = self.create_end_indicator()
        self.item_name = self.create_item_name_field()
        self.view = ft.Container()
        self.init_controls()

    def create_end_indicator(self):
        return Container(
            bgcolor=colors.BLACK26,
            border_radius=border_radius.all(30),
            height=1,
            width=100,
            opacity=0.0,
        )

    def create_item_name_field(self):
        return [
            TextField(
                label="Nuevo nombre de Item",
                width=100,
                height=50,
                bgcolor=colors.WHITE,
                on_submit=self.add_item_handler
            ),
        ]

    def init_controls(self):
        self.controls = []
        for i in self.item_name:
            self.controls.append(i)
        self.controls.append(TextButton("Agregar Elemento", icon=icons.ADD, on_click=self.add_item_handler))
        self.controls.append(TextButton("Eliminar elementos de esta lista", icon=icons.DELETE_FOREVER, on_click=self.delete_items_handler))
        self.controls.append(TextButton("Modificar elemento de esta lista", icon=icons.SCREEN_ROTATION_ALT, on_click=self.modify_items_handler))
        self.controls.append(self.items)
        self.controls.append(self.end_indicator)

    def build(self):
        self.view = Container(
            content=DragTarget(
                group="items",
                content=DragTarget(
                    group="lists",
                    content=Container(
                        content=Column(self.controls, spacing=1, tight=True, expand=True),
                        border=border.all(2, colors.BLACK12),
                        border_radius=border_radius.all(15),
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

    def get_items(self):
        print(self.items_info_pura)

    def add_item_handler(self, e):
        self.add_item()

    def delete_items_handler(self, e):
        self.items.controls = []
        self.view.update()

        self.items_info_pura = []

    def modify_items_handler(self, e):
        self.modify_item()

    def modify_item(self):
        if len(self.items.controls) == 0:
            print("No hay elemento para modificar")
        elif len(self.items.controls) == 1:
            print("Numero correcto de elementos para modificar")
            print("pero... metodo incorrecto xd")
        else:
            print("Demasiados elementos en la lista")
        self.view.update()

    def add_item(self, item_texts: list = None, chosen_control: Draggable = None, swap_control: Draggable = None, color=""):
        controls_list = [x.controls[1] for x in self.items.controls]
        to_index = controls_list.index(swap_control) if swap_control in controls_list else None
        from_index = controls_list.index(chosen_control) if chosen_control in controls_list else None
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
            #print("reordenamiento: ", to_index, from_index)
            self.items.controls.insert(to_index, self.items.controls.pop(from_index))
            self.set_indicator_opacity(swap_control, 0.0)

        # insert (drag from other list to middle of this list)
        elif (to_index is not None):
            #print("insertado: ", to_index)
            new_item = Item(self, item_texts, color)
            control_to_add.controls.append(new_item.view)
            self.items.controls.insert(to_index, control_to_add)

            self.items_info_pura.append(item_texts)

        # add new (drag from other list to end of this list, or use add item button)
        else:
            # print("creado")
            new_item = Item(self, item_texts, color)
            control_to_add.controls.append(new_item.view)
            self.items.controls.append(control_to_add)

            self.items_info_pura.append(item_texts)

    def set_indicator_opacity(self, item, opacity):
        controls_list = [x.controls[1] for x in self.items.controls]
        self.items.controls[controls_list.index(item)].controls[0].opacity = opacity
        self.view.update()

    def remove_item(self, item):
        controls_list = [x.controls[1] for x in self.items.controls]
        del self.items.controls[controls_list.index(item)]
        self.view.update()

        found = False
        for i in range(len(self.items_info_pura)):
            if (not found) and self.items_info_pura[i] == item.data.item_texts:
                self.items_info_pura.pop(i)
                found = True


    def drag_accept(self, e):
        src = self.page.get_control(e.src_id)
        l = self.page.item_lists.controls
        to_index = l.index(e.control.data)
        from_index = l.index(src.content.data)
        l[to_index], l[from_index] = l[from_index], l[to_index]
        self.end_indicator.opacity = 0.0
        self.view.update()
        self.page.update()

    def drag_will_accept(self, e):
        self.end_indicator.opacity = 0.0
        self.page.update()

    def drag_leave(self, e):
        self.end_indicator.opacity = 0.0
        self.page.update()

    def item_drag_accept(self, e):
        src = self.page.get_control(e.src_id)
        self.add_item(src.data.item_texts)
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
    def create_item_name_field(self):
        return [Text("")]

    def init_controls(self):
        self.controls = [
            self.items,
            self.end_indicator
        ]

class ItemList_Creator(ItemList):
    def create_item_name_field(self):
        aux = []
        aux.append(TextField(label="Materia", width=250, height=50, bgcolor=colors.WHITE))
        aux.append(TextField(label="Horario", width=250, height=50, bgcolor=colors.WHITE))
        aux.append(TextField(label="Profesor", width=250, height=50, bgcolor=colors.WHITE))
        aux.append(TextField(label="Tipo de clase", width=250, height=50, bgcolor=colors.WHITE))
        return aux

    def init_controls(self):
        self.controls = []
        self.controls.append(self.item_name[0])
        self.controls.append(self.item_name[1])
        self.controls.append(self.item_name[2])
        self.controls.append(self.item_name[3])
        self.controls.append(TextButton("Agregar elemento", icon=icons.ADD, on_click=self.add_item_handler))
        self.controls.append(self.items)
        self.controls.append(self.end_indicator)

    def add_item(self, item_texts: list = None, chosen_control: Draggable = None, swap_control: Draggable = None, color=""):
        controls_list = [x.controls[1] for x in self.items.controls]
        to_index = controls_list.index(swap_control) if swap_control in controls_list else None
        from_index = controls_list.index(chosen_control) if chosen_control in controls_list else None
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
            #print("reordenamiento GENERAL: ", to_index, from_index)
            self.items.controls.insert(to_index, self.items.controls.pop(from_index))
            self.set_indicator_opacity(swap_control, 0.0)

        # insert (drag from other list to middle of this list)
        elif (to_index is not None):
            #print("insertado GENERAL: ", to_index)
            new_item = Item(self, item_texts, color)
            control_to_add.controls.append(new_item.view)
            self.items.controls.insert(to_index, control_to_add)

            self.items_info_pura.append(item_texts)

        # add new (drag from other list to end of this list, or use add item button)
        else:
            #print("nuevo elemento GENERAL: ", item_texts)
            if ((item_texts is not None) and (item_texts != [])):
                new_item = Item(self, item_texts, color)
            else:
                aux = []
                for i in range(0, len(self.item_name)):
                    aux.append(self.item_name[i].value)
                    self.item_name[i].value = ""
                new_item = Item(self, aux, color)
            control_to_add.controls.append(new_item.view)
            self.items.controls.append(control_to_add)

            self.items_info_pura.append(item_texts)

        self.view.update()
        self.page.update()

class ItemList_Remover(ItemList):
    def init_controls(self):
        self.controls = [
            TextButton("Eliminar elementos de esta lista", icon=icons.DELETE_FOREVER, on_click=self.delete_items_handler, width=250),
            self.items,
            self.end_indicator
        ]

class ItemList_Modifier(ItemList):
    def create_item_name_field(self):
        aux = []
        aux.append(TextField(label="Materia", width=250, height=50, bgcolor=colors.WHITE))
        aux.append(TextField(label="Horario", width=250, height=50, bgcolor=colors.WHITE))
        aux.append(TextField(label="Profesor", width=250, height=50, bgcolor=colors.WHITE))
        aux.append(TextField(label="Tipo de clase", width=250, height=50, bgcolor=colors.WHITE))
        aux.append(Text("------------"))
        return aux
    
    def init_controls(self):
        self.controls = []
        self.controls.append(self.item_name[0])
        self.controls.append(self.item_name[1])
        self.controls.append(self.item_name[2])
        self.controls.append(self.item_name[3])
        self.controls.append(TextButton("Modificar elemento de esta lista", icon=icons.SCREEN_ROTATION_ALT, on_click=None, width=250, disabled=True)),
        self.controls.append(TextButton("Confirmar Modificacion", icon=icons.SCREEN_ROTATION_ALT, on_click=self.modify_items_handler, width=250)),
        self.controls.append(self.item_name[4])
        self.controls.append(self.items),
        self.controls.append(self.end_indicator)

    def modify_item(self):
        if len(self.items.controls) == 0:
            #print("No hay elementos para modificar")
            self.item_name[4].value = "No hay elementos para modificar"
        elif len(self.items.controls) == 1:
            #print("Numero correcto de elementos para modificar")
            #print("y... metodo correcto xd")
            # self.item_name[0].value = self.items.controls[0].controls
            # self.item_name[1].value = self.items.controls[0].controls[1].content.content.content.content.controls[1].value
            # self.item_name[2].value = self.items.controls[0].controls[1].content.content.content.content.controls[2].value
            # self.item_name[3].value = self.items.controls[0].controls[1].content.content.content.content.controls[3].value
            self.items.controls = []
            self.view.update()
            self.add_item([
                        self.item_name[0].value,
                        self.item_name[1].value,
                        self.item_name[2].value,
                        self.item_name[3].value,
            ])
            self.item_name[0].value = ""
            self.item_name[1].value = ""
            self.item_name[2].value = ""
            self.item_name[3].value = ""
            self.item_name[4].value = "Se ha modificado exitosamente"
        else:
            #print("Demasiados elementos en la lista")
            self.item_name[4].value = "Demasiados elementos en la lista"
        self.view.update()



class ItemList_Cell(ItemList):
    def init_controls(self):
        self.controls = [
            Container(self.items, width=110, padding=padding.all(0), margin=0),
            self.end_indicator
        ]


class Item():
    def __init__(self, list: ItemList, item_texts: list = [], color: ft.colors = ""):
        textos = ["Aula","Materia","Horario","Profesor"]
        if (item_texts is None) or (item_texts == []):
            item_texts = [""] * len(textos)
        elif len(item_texts) < len(textos):
            item_texts += [""] * (len(textos) - len(item_texts))
        
        self.list = list
        self.item_texts = item_texts
        self.color = color

        self.card_item = Card(
            content=Container(
                content=Column([
                    Row([
                        Icon(name=icons.HOURGLASS_BOTTOM),
                        Text(value=f"{self.item_texts[0]}"),
                    ]),
                    Text(value=f"{textos[1]}: {self.item_texts[1]}", size=10),
                    Text(value=f"{textos[2]}: {self.item_texts[2]}", size=10),
                    Text(value=f"{textos[3]}: {self.item_texts[3]}", size=10),
                ],
                    alignment="start",
                ),
                height=150,
                width=100,
                padding=7,
            ),
            elevation=0,
            data=self.list,
            color=color,
        )

        self.view = Draggable(
            group="items",
            content=DragTarget(
                group="items",
                content=self.card_item,
                #on_accept=self.drag_accept,
                #on_leave=self.drag_leave,
                #on_will_accept=self.drag_will_accept,
            ),
            data=self
        )

    def drag_accept(self, e):
        src = self.list.page.get_control(e.src_id)
        self.list.add_item(src.data.item_texts, src, self.view, self.color)
        self.set_indicator_opacity(0.0)

    def drag_leave(self, e):
        self.set_indicator_opacity(0.0)

    def drag_will_accept(self, e):
        self.set_indicator_opacity(1.0)

    def set_indicator_opacity(self, opacity):
        self.list.set_indicator_opacity(self.view, opacity)


def create_calendar_hours_intervals(inicio : int, final : int):
    columna = []
    for i in range(inicio, final):
        columna.append(f"{i} -> {i+1}")
    return columna

def create_calendar_table_headers_first_row(headers : list):
    encabezados = []
    for header in headers:
        encabezados.append(ft.DataColumn(label=ft.Text(f"{header}", color=colors.BLACK, bgcolor="",expand=True)))
    return encabezados

def create_calendar_rows(rows, columns, page, color="white"):
    filas = []
    for i, row in enumerate(rows):
        celdas = []
        celdas.append(ft.DataCell(ft.Text(f"{row}", expand=True,color=colors.BLACK, bgcolor=colors.GREY_50)))
        for j in range(1, len(columns)):
            celdas.append(ft.DataCell(ItemList_Cell(page, f"A-{'{:02d}'.format(i)}-{'{:02d}'.format(j)}", color)))
        filas.append(ft.DataRow(cells=celdas))
    return filas


def main(page: ft.Page):
    page.window.width = 1500

    dias = [" ", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    intervalos_horarios = create_calendar_hours_intervals(8, 23)

    creador = ItemList_Creator(page, "ItemList_creador")
    removedor = ItemList_Remover(page, "ItemList_removedor")
    modificador = ItemList_Modifier(page, "ItemList_modoficador")

    def get_items_viernes(page):
        for i in range(len(page.controls[0].controls[0].controls[1].controls[0].rows)):
            page.controls[0].controls[0].controls[1].controls[0].rows[i].cells[5].content.get_items()
        print("###########################################")

    btn_tester = TextButton("JUST DO IT... please :^/", on_click=lambda _:get_items_viernes())

    page.add(
            Column([
                Row([
                    Column([btn_tester, creador, removedor, modificador]),
                    Column([
                        ft.DataTable(
                            columns=create_calendar_table_headers_first_row(dias),
                            rows=create_calendar_rows(intervalos_horarios,dias,page),
                            data_row_min_height = 130,
                            data_row_max_height = float("inf"),
                            bgcolor='#3A3A3A',
                            column_spacing=5,
                            heading_row_color= colors.GREY_300
                            ),
                    ],
                    scroll=ScrollMode.ADAPTIVE,
                    expand=False,
                    alignment="start",)
                ], 
                vertical_alignment="start",
                scroll=ScrollMode.ALWAYS,
                )
            ], 
            expand=True,
            alignment="start",
            scroll=ScrollMode.ALWAYS,
            )
        )
    
    creador.add_item(["hola", "buenas", "bonjeur"])
    creador.add_item(["Mate 2", "18 -> 17", "Victor Tilla"])
    creador.add_item(["Fisica 3", "hoy -> mañana", "Juan Topo"])
    creador.add_item(["ILEA", "nunca -> ayer", "Din Jarin"])

    mate1 = [["Mate1", "13 -> 14", "Din Djarin"], "white"]
    mate2 = [["Mate2", "13 -> 14", "Grogu"], ""]
    mate3 = [["Mate3", "13 -> 14", "R2-D2"], "white"]
    fis1  = [["Fis1" , "13 -> 14", "Newton Pascal"], ""]
    fis2  = [["Fis2" , "13 -> 14", "Euler Faraday"], "green"]
    nada  = [[""], "red"]

    items = [mate1, mate2, nada, nada, mate3, nada, nada, fis1, fis1, nada, fis2, mate2, nada, nada, nada]

    print(page.controls[0].controls[0].controls[1].controls[0].rows)
    for i in range(len(page.controls[0].controls[0].controls[1].controls[0].rows)):
        print(page.controls[0].controls[0].controls[1].controls[0].rows[i].cells[5].content.list_name)
        if items[i][0] != [""]:
            page.controls[0].controls[0].controls[1].controls[0].rows[i].cells[5].content.add_item(items[i][0], color=items[i][1])
        page.controls[0].controls[0].controls[1].controls[0].rows[i].cells[5].content.view.update()
        # for j in i.cells:
        #     if type(j.content) == ItemList_Cell:
        #         print(j.content.list_name)
        #     else:
        #         print(j.content.value)
        print("-----------------------")
    
    page.controls[0].controls[0].controls[1].controls[0].rows[1].cells[5].content.add_item(items[1][0], color=items[1][1])
    page.controls[0].controls[0].controls[1].controls[0].rows[1].cells[5].content.view.update()

    for i in range(len(page.controls[0].controls[0].controls[1].controls[0].rows)):
        if items[i][0] != [""]:
            page.controls[0].controls[0].controls[1].controls[0].rows[i].cells[5].content.get_items()
    print("###########################################")


if __name__ == "__main__":
    ft.app(target=main)
