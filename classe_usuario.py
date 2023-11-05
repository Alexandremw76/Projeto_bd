class Usuario:
    def __init__(self):
        self._email = ""
        self._nome = ""
        self._senha = ""
        self.flamengo = False
        self.onepiece = False

    def get_email(self):
        return self._email
    
    def set_email(self, email):
        if isinstance(email, str) and len(email.strip()) > 0 and email.count('@') == 1 and email.count(".") ==1:
            self._email = email
        else:
            raise ValueError("O email deve ser uma string não vazia e conter exatamente um símbolo '@'.")

    
    def get_nome(self):
        return self._nome

    
    def set_nome(self, nome):
        if isinstance(nome, str) and len(nome.strip()) > 0 and not any(char.isdigit() for char in nome):
            self._nome = nome
        else:
            raise ValueError("O nome deve não vazio e não pode conter números.")

    
    def get_senha(self):
        return self._senha

    
    def set_senha(self, senha):
        if isinstance(senha, str) and len(senha.strip()) > 0:
            self._senha = senha
        else:
            raise ValueError("A senha deve ser não vazia.")

    def set_flamengo(self, flamengo):
        if flamengo == "Nao":
            self.flamengo = False
        elif flamengo == "Sim":
            self.flamengo = True
        else:
            raise Exception("Valor inválido")
    def get_flamengo(self):
        return self.flamengo
    
    def set_onepiece(self,onepiece):
        if(onepiece == "Nao"):
            self.onepiece = False
        elif(onepiece == "Sim"):
            self.onepiece = True
        else:
            raise Exception("valor invalido")
    def get_onepiece(self):
        return self.onepiece
