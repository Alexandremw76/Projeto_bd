import sqlite3
from classe_produto import * 
from clase_cliente import *
class BancoDeDados:
    def __init__(self, nome_banco):
        self.conn = self.conectar_bd(nome_banco)
        if self.conn:
            self.criar_tabela_produto()
            self.criar_tabela_cliente()

    def conectar_bd(self, nome_banco):
        try:
            conn = sqlite3.connect(nome_banco)
            self.conn = conn
            return conn
        except Exception as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None
    def criar_tabela_produto(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50) NOT NULL,
                quantidade INT NOT NULL,
                preco REAL NOT NULL,
                tamanho VARCHAR(3) NOT NULL
            )
        """)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Erro ao criar tabela de produtos:", e)
    def inserir_produto(self, produto):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO produtos (nome, quantidade, preco, tamanho) VALUES (?, ?, ?, ?)",
                           (produto.get_nome(), produto.get_qtd(), produto.get_valor(), produto.get_tam()))
            self.conn.commit()
            print("Produto inserido com sucesso!")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao inserir produto:", e)

    def listar_produtos(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM produtos")
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
    def atualizar_produto(self, id, produto):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE produtos SET nome=?, quantidade=?, preco=?, tamanho=? WHERE id=?",
                           (produto.get_nome(), produto.get_qtd(), produto.get_valor(), produto.get_tam(), id))
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

    def criar_tabela_cliente(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                email VARCHAR(50) PRIMARY KEY NOT NULL,
                nome VARCHAR(50) NOT NULL,
                senha VARCHAR(50) NOT NULL
            )
        """)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("Erro ao criar tabela de clientes :", e)

    def casdastrar_cliente(self, Cliente):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO clientes (email, nome, senha) VALUES (?, ?, ?, ?)",
                           (Cliente.get_email(), Cliente.get_nome(), Cliente.get_senha()))
            self.conn.commit()
            print("Cliente cadastrado com sucesso!")
        except Exception as e:
            self.conn.rollback()
            print("Erro ao cadastrado Cliente:", e)

    def verificar_login(self, cliente):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM cliente WHERE email=? AND senha=?", (cliente.get_email(), cliente.get_senha()))
            resultado = cursor.fetchall()
            return resultado
        except Exception as e:
            print("Erro ao verificar login:", e)

