import flet as ft
import re
from Validation import Validation


class LogIn(ft.Container):
    def __init__(self):
        super().__init__()
        self.border_radius = 5
        self.padding = 20
        self.gradient = ft.RadialGradient(
            center=ft.alignment.top_center,
            radius=2.0,
            colors=["#1D2535","#010101"]
        )
        self.image_fit = ft.ImageFit.FILL
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls= [
                ft.Text("Sign In", size=25),
                ft.TextField(label="Email", hint_text="example@unrn.edu.ar", width=300),
                ft.TextField(label="Password", width=300, password=True, can_reveal_password=True),
                ft.ElevatedButton("LogIn", width=300),
            ]
        )
        

def __main__(page: ft.Page):
    page.title = "LogIn"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    login = LogIn()
    page.add(login)
     
    page.update()

if __name__ == "__main__":
    
    ft.app(target=__main__, assets_dir="assets")