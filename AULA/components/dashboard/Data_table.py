from asyncio.windows_events import INFINITE
from flet import *

class DataTableCustom():
    def __init__(self, data_columns : list = [], data_rows : list = []):
        self.data_columns : list = data_columns
        self.data_rows : list = data_rows
        self.delete_icon : IconButton = IconButton(icons.DELETE, on_click=lambda e: print(f"Deleted: {e}"))
        self.__nextRow : DataRow = DataRow()
        self.__row_iterator= None
        self.__rowData : dict = {}
        self.extra_info : dict = {}
        self.DataTableCustom = None
        self.rowsSelected : bool = False

    def __row_selected(self, e, func = None):
        self.deselectAll()
        e.control.selected = False if e.control.selected else True

        if e.control.selected:
            e.control.color = "#003E79"
        else:
            if e.control in self.__rowData.keys():
                e.control.color = (self.__rowData[e.control])["Color"]
            else:
                e.control.color = "transparent"
        
        if func is not None:
           values = []
           for cell in e.control.cells:
               values.append(cell.content.value)
           e.control.update()
           func(values)
        e.control.update()

    def setVisible(self, value : bool):
        self.DataTableCustom.visible = value
        self.DataTableCustom.update()
    
    def update(self):
        self.DataTableCustom.update()
        
    def selectAll(self):
        for row in self.data_rows:
            row.selected = True
            row.color = "#003E79"
            row.update()

    def deselectAll(self):
        for row in self.data_rows:
            row.selected = False
            row.color = "transparent"
            row.update()

    def changeStatus_inOrder(self, cell_status : str):
        if self.__row_iterator is not None:
            self.__nextRow = next(self.__row_iterator)
            row = self.__nextRow

            row.cells[1].content.value = cell_status
            row.update()

    def have_rowsSelected(self):
        rows_selected = [row for index, row in enumerate(self.data_rows) if row.selected]
        if len(rows_selected) > 0:
            return True, rows_selected   # Todos son True
        else:
            return False, rows_selected # Todos son False

    def changeContent(self, row: DataRow, cell_content : str):
        status = row.cells[1].content
        status.value = cell_content
        row.update()

    def getInfo(self):
        return self.extra_info

    def getRows(self):
        return self.data_rows
    
    def getColumns(self):
        return self.data_columns

    def setExtraInfo(self, key : str = None, value = None, dicc  : dict = None):
        if key is not None:
            self.extra_info[key] = value
        else:
            self.extra_info = dict(self.extra_info, **dicc)

    def setColor(self, row, color):
        row.color = color
        self.__rowData[row] = {"Color" : color}
        row.update()

    def setColums(self, headers: list[str]):
        for header in headers:
            self.data_columns.append(
                DataColumn(
                    label=Text(
                        value=header,
                        weight="bold",
                        size=20,
                        color= "#C4C4C4",
                        expand=True,
                    ),
                )
            )

    def __createRow(self, list):
        cells = [DataCell(content=Text(value=row,weight="bold",size=16,color="#A6A6A6",expand=True,)) for row in list]
        return cells

    def setRows(self, rows, especial_func):
        for row in rows:
            self.data_rows.append(
                DataRow(
                    on_select_changed= lambda e: self.__row_selected(e, especial_func),
                    cells=self.__createRow(row),
                )
            )
        self.__row_iterator = iter(self.data_rows)

    def deleteAll(self):
        self.data_rows.clear()
        self.__row_iterator = None
        self.__nextRow = None

    def deleteSelected(self, rows):
        for row in rows:
            self.data_rows.remove(row)
            self.extra_info.pop(row.cells[0].content.value)
            self.__rowData.pop(row, None)
        self.__row_iterator = iter(self.data_rows)
        self.__nextRow = self.__row_iterator

    def build(self):
        self.DataTableCustom= DataTable(
            width=INFINITE,
            border_radius=15,
            heading_row_color = {
                "" : colors.with_opacity(0.5, "#7D7D7D"),
            },
            data_row_color={
                MaterialState.DEFAULT : colors.with_opacity(0, "#000000"),
            },
            expand=True,
            border=border.all(1, "#000000"),
            horizontal_lines=border.BorderSide(0.5, "#000000"),
            vertical_lines=border.BorderSide(0.5, "#000000"),
            show_bottom_border=True,
            columns=self.data_columns,
            rows=self.data_rows,
        )
        return self.DataTableCustom