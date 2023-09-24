class Cliente:
    def __init__(self):
        self._email = ""
        self._nome = ""
        self._senha = ""

    def get_email(self):
        return self._email
    
    def set_email(self, email):
        if isinstance(email, str) and len(email.strip()) > 0 and email.count('@') == 1 and email.count(".") ==1:
            self._email = email
        else:
            raise ValueError("O email deve ser uma string não vazia e conter exatamente um símbolo '@'.")

    
    def get_nome(self):
        return self._nome

    
    def set_nome(self, value):
        if isinstance(value, str) and len(value.strip()) > 0 and not any(char.isdigit() for char in value):
            self._nome = value
        else:
            raise ValueError("O nome deve ser uma string não vazia e não pode conter números.")

    
    def get_senha(self):
        return self._senha

    
    def set_senha(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._senha = value
        else:
            raise ValueError("A senha deve ser uma string não vazia.")
