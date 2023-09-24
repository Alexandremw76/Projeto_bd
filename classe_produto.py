class Produto:
    def __init__(self):
        self.nome = "invalido"
        self.valor = "invalido"
        self.qtd = "invalido"
        self.tam = "invalido"
    def set_nome(self, nome): 
        max_length=50
        if nome == ""  or nome.strip()=="" or len(nome)>max_length or e_numero(nome) == True:
            raise Exception("nome invalido")

        else:
            self.nome = nome
    
    def get_nome(self):
        return self.nome
    def set_valor(self, valor):
        if valor == "" or valor.isspace() or e_numero_float(valor) == False:
            raise Exception("valor invalido")
        else:
            self.valor = float(valor)
    
    def get_valor(self):
        return self.valor
        
    def set_qtd(self, qtd):
        if qtd == "" or qtd.isspace() or e_numero(qtd) == False:
            raise Exception("qtd invalido")
        else:
            self.qtd = int(qtd)
    def get_qtd(self):
        return self.qtd
    def set_tam(self,tam):
        if(validar_tam(tam)):
            self.tam = tam
        else:
            raise Exception("tam invalido")
    def get_tam(self):
        return self.tam
    
def e_numero(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
def e_numero_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
def validar_tam(tam):
    opcoes_tamanho = ["P", "M", "G", "GG"]
    if tam in opcoes_tamanho:
        return True
    else:
        return False 