import sqlite3
from classe_produto import * 
from classe_usuario import *

class BancoDeDados:
    def __init__(self, nome_banco):
        self.conn = self.conectar_bd(nome_banco)
        if self.conn:
            self.criar_tabela_produtos()
            self.criar_tabela_usuarios()
            self.criar_tabela_compras()
            self.criar_indices()
            self.criar_view()
            self.adicionar_restricoes_referenciais()

    def conectar_bd(self, nome_banco):
        try:
            conn = sqlite3.connect(nome_banco)
            self.conn = conn
            return conn
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)
            return False
    def criar_tabela_produtos(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL,
                quantidade INT NOT NULL,
                preco REAL NOT NULL,
                tamanho VARCHAR(1) NOT NULL,
                vendedor_email VARCHAR(50) NOT NULL,
                FOREIGN KEY (vendedor_email) REFERENCES clientes (email)
            )
        """)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback() # desfaz todas as alterações
            print("Erro ao criar tabela de produtos:", e)
    def produtos_geral(self): # todos os produtos registrados no banco
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()
            return produtos
        except Exception as e:
            print(e)
    def inserir_produto(self, produto,usuario):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO produtos (nome, quantidade, preco, tamanho,vendedor_email) VALUES (?, ?, ?, ?, ?)",
                           (produto.get_nome(), produto.get_qtd(), produto.get_valor(), produto.get_tam(),usuario.get_email()))
            self.conn.commit()
            print("Produto inserido com sucesso!")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir produto:", e)

    def listar_produtos(self,Usuario): # retorna os produtos de determiando vendedor
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM produtos WHERE vendedor_email=?",(Usuario.get_email(),))
            produtos = cursor.fetchall()
            return produtos
        except Exception as e:
            print("Erro ao listar produtos:", e)
    
    def listar_produtos_por_nome(self,nome):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM produtos WHERE nome=?",(nome,))
            produtos = cursor.fetchall()
            return produtos
        except Exception as e:
            print("Nenhum produto encontrado:", e)
    def atualizar_produto(self, id, produto, Usuario):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE produtos SET nome=?, quantidade=?, preco=?, tamanho=?, vendedor_email=? WHERE id=?",
                           (produto.get_nome(), produto.get_qtd(), produto.get_valor(), produto.get_tam(),Usuario.get_email(), id))
            self.conn.commit()
            print("Produto atualizado com sucesso!")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao atualizar produto:", e)

    def remover_produto(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id=?", (id,))
            self.conn.commit()
            print("Produto removido com sucesso!")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao remover produto:", e)
    def fechar_conexao(self):
        if self.conn:
            self.conn.close()

    def criar_tabela_usuarios(self):
        try:
            cursor = self.conn.cursor() ## restriçao que cada email dever ser unico
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes( 
                email VARCHAR(50) PRIMARY KEY NOT NULL UNIQUE, 
                nome VARCHAR(50) NOT NULL,
                senha VARCHAR(50) NOT NULL,
                flamengo BOOLEAN NOT NULL,
                assisti_one BOOLEAN NOT NULL
            )
        """)
                # Adiciona a restrição de chave única 
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Erro ao criar tabela de clientes :", e)

    def casdastrar_cliente(self, Cliente):
        try:
            print((Cliente.get_email(), Cliente.get_nome(), Cliente.get_senha(),Cliente.get_flamengo(),Cliente.get_onepiece()))
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO clientes (email, nome, senha,flamengo,assisti_one) VALUES (?, ?, ?, ?, ?)",
                           (Cliente.get_email(), Cliente.get_nome(), Cliente.get_senha(),Cliente.get_flamengo(),Cliente.get_onepiece()))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise Exception("error a cadastrar cliente")
        
    def cliente_eh_flamengo(self, email):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE email = ?", (email,))
            result = cursor.fetchall()
            if result is not None:
                return result  # Retorna o valor da coluna 
            else:
                raise Exception("Cliente não encontrado")
        except Exception as e:
            print("Erro ao verificar se o cliente é flamengo:", e)
            return None 

 

    def verificar_login(self, cliente): # se contem um usuario com os dados do cliente
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE email=? AND senha=?", (cliente.get_email(), cliente.get_senha()))
            resultado = cursor.fetchall()
            if (resultado):
                return True
            else:
                return False
        except Exception as e:
            print("Erro ao verificar login:", e)

    def criar_tabela_compras(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER,
                cliente_email VARCHAR(50),
                quantidade INT NOT NULL,
                data_compra DATETIME NOT NULL,
                metodo_pag VARCHAR(50),
                compra_efetivada BOOLEAN,
                FOREIGN KEY (produto_id) REFERENCES produtos (id),
                FOREIGN KEY (cliente_email) REFERENCES clientes (email)
            )
        """)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Erro ao criar tabela de compras:", e)
            
    def cadastra_compra(self, Usuario, Produto_id, qtd,data_compra,metodo_pag):
        compra_efetivada = False
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO compras (produto_id, cliente_email, quantidade,data_compra,metodo_pag,compra_efetivada) VALUES (?, ?, ?, ?, ?, ?)",
                        (Produto_id, Usuario.get_email(), qtd,data_compra,metodo_pag,compra_efetivada))
            self.conn.commit()
            return True
        except ValueError as ve:
            self.conn.rollback()
            raise ve
        except Exception as e:
            self.conn.rollback()
            raise Exception("Erro ao cadastrar compra:", e)
        
    def vendas_por_vendedor(self, email_vendedor):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT c.id, p.nome, c.quantidade, c.data_compra, c.metodo_pag, c.cliente_email, c.compra_efetivada FROM compras c "
                        "INNER JOIN produtos p ON c.produto_id = p.id "
                        "WHERE p.vendedor_email = ?", (email_vendedor,))
            vendas = cursor.fetchall()
            return vendas
        except Exception as e:
            print("Erro ao buscar vendas por vendedor:", e)
            return None
    def efetivar_venda(self, id_venda):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE compras SET compra_efetivada=? WHERE id=?", (True, id_venda))
            self.conn.commit()
        except Exception as e:
            print("Erro ao efetivar_venda", e)
            return None
        
    def criar_view(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE VIEW IF NOT EXISTS venda_detalhada AS
            SELECT c.id AS id_compra, p.nome AS nome_produto, c.quantidade, c.data_compra, c.metodo_pag, u.email AS email_cliente
            FROM compras c
            JOIN produtos p ON c.produto_id = p.id
            JOIN clientes u ON c.cliente_email = u.email;
            """)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Erro ao criar a view 'venda_detalhada':", e)

    def criar_indices(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendedor_email ON produtos (vendedor_email);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cliente_email ON compras (cliente_email);")
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Erro ao criar índices:", e)

    def adicionar_restricoes_referenciais(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;") 
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Erro ao ativar suporte a chave estrangeira:", e)