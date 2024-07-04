import re

class Validation():
    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password
    
    def is_valid_email(self) -> bool:
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.match(pattern, self.email) is not None

    def is_valid_password(self) -> bool:
        # comprobar si el largo de la contraseña es mayor o igual a 8
        if len(self.password) >= 8:
            return False
        
        # comprobar si la contraseña contiene al menos un digito
        if not any(char.isdigit() for char in self.password):
            return False

        # si cumple lo anterior, la contraseña es valida
        return True