from tkinter import *
import tkinter as tk 
from tkinter import messagebox # importar a classe messagebox
from tkinter import ttk  # importar a classe ttk
from classe_banco import *
from datetime import datetime

nome_bd = "dados.db"
meu_banco = BancoDeDados(nome_bd)
    
def Carregar_dados_tabela(tabela,usuario): # carregar dados do bd para tabela
    meu_banco.conectar_bd(nome_bd)
    try:
        meu_banco.conectar_bd(nome_bd)
        lista_de_produtos = meu_banco.produtos_geral()
        tabela.delete(*tabela.get_children())

        for produto in lista_de_produtos:
            if(str(produto[2])!="0"):
                tabela.insert("", "end", values=(str(produto[0]), str(produto[1]), str(produto[2]), str(produto[3]), str(produto[4])))
    except Exception as e:
        print("Erro ao carregar dados para a tabela:", e)
    finally:
        meu_banco.fechar_conexao()


def get_id_produto_selecionado(tabela): # pegar do bd a id do produto selecionado na tabela
    selecao = tabela.selection()  # Obtém a seleção atual
    if selecao:  # Se houver uma seleção
        for item in selecao:
            Produto_ = tabela.item(item, "values")  # Obtém os valores do item
            return int(Produto_[0]) # retornar id do produto na selecionado atual

def get_produto_selecionado_do_bd(tabela): # retorna os dados do produto selecioando(dados vem do banco de dados)
    selecao = tabela.selection()  # Obtém a seleção atual
    if selecao:  # Se houver uma seleção
        for item in selecao:
            Produto_ = tabela.item(item, "values")  # Obtém os valores do item
            return list(Produto_) # retornar produto selecionado atual

def Atualizar_item_qtd_banco(root,tabela, qtd_comprada, usuario, metodo_pag):
    selecao = tabela.selection()  # Item selecionado na tabela

    if not selecao:
        messagebox.showerror("Erro", "Nenhum item selecionado")
        return  # Nenhum item selecionado, sair

    id_produto = get_id_produto_selecionado(tabela)  # ID do produto selecionado
    dados_produto = get_produto_selecionado_do_bd(tabela)  # Dados do produto selecionado

    produto = Produto()
    produto_id = int(dados_produto[0])

    produto.set_nome(dados_produto[1])
    produto.set_qtd(dados_produto[2])
    produto.set_valor(dados_produto[3])
    produto.set_tam(dados_produto[4])

    quantidade_comprada = int(qtd_comprada.get())
    if quantidade_comprada > produto.qtd:
        messagebox.showerror("Erro", "Você está tentando comprar mais do que o disponível!")
    else:
        produto.qtd -= quantidade_comprada

        try:
            meu_banco.conectar_bd(nome_bd)
            meu_banco.atualizar_produto(id_produto, produto, usuario)
            data_compra = datetime.now()
            mostra_compra(root,usuario,produto,quantidade_comprada)
            meu_banco.cadastra_compra(usuario, produto_id, quantidade_comprada,data_compra,str(metodo_pag.get()))
            messagebox.showinfo("sucesso","Produto comprado com sucesso!!!")
            Carregar_dados_tabela(tabela, usuario)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            meu_banco.fechar_conexao()

def calcular_desconto(usuario, produto, qtd):
    valor_total = produto.get_valor() * qtd

    desconto = 0
    dados_usuario = meu_banco.cliente_eh_flamengo(usuario.get_email())
    if dados_usuario[0][3] == 1 and dados_usuario[0][4] == 1:
        # Se o usuário torce para o Flamengo e gosta de One Piece, aplicar 20% de desconto (10% + 10%)
        desconto = 0.2
    elif dados_usuario[0][3] == 1 or dados_usuario[0][4] == 1:
        desconto = 0.1
    
    # Apply the discount correctly by multiplying it with the total value
    valor_total = valor_total - (desconto * valor_total)
    
    return valor_total
def mostra_compra(root,usuario,produto,qtd):
    meu_banco.conectar_bd(nome_bd)
    janela_secundaria = tk.Toplevel(root)
    janela_secundaria.geometry("400x400")
    janela_secundaria.title("Compra")
    tabela = ttk.Treeview(janela_secundaria, columns=(0,1))
    tabela.heading(0, text="Quantidade")
    tabela.heading(1, text="Valor total dos produtos com desconto")
    tabela.column("#0", width=0)
    valor_total = calcular_desconto(usuario,produto,qtd)
    tabela.insert("", "end", values=(qtd,valor_total))
    tabela.pack()
    botao_fechar = tk.Button(janela_secundaria, text="Fechar", command=janela_secundaria.destroy)
    botao_fechar.pack()
    meu_banco.fechar_conexao

def criar_interface_vender(root,usuario):
    # Cria a janela principal
    root.title("Crud")
    root.geometry("600x650")

    tabela = ttk.Treeview(root, columns=(0, 1, 2, 3, 4))
    tabela.heading(0, text="ID")
    tabela.heading(1, text="Nome")
    tabela.heading(2, text="Quantidade")
    tabela.heading(3, text="Preço")
    tabela.heading(4, text="Tamanho")

    tabela.column("#0", width=0)
    tabela.column("#1", width=100)
    tabela.column("#2", width=100)
    tabela.column("#3", width=100)
    tabela.column("#4", width=100)
    tabela.pack()


    qtd = tk.Label(root, text="Quantidade", font=("Arial", 10))
    qtd.pack()

    entrada_qtd = tk.Entry(root)
    entrada_qtd.pack(pady=5, padx=10)  


    metodo_pag = tk.StringVar(root)
    metodo_pag.set("Pix")  # Define o valor padrão como p
    # Opções de tamanho
    opcoes_meotodo = ["Pix", "Boleto", "Cartao"]
    # Menu suspenso (OptionMenu) para seleção do tamanho
    menu_metodo = tk.OptionMenu(root, metodo_pag, *opcoes_meotodo)
    menu_metodo.pack(pady=20)


    

    botao_comprar = tk.Button(root, text="Comprar Produto", command=lambda: Atualizar_item_qtd_banco(root,tabela, entrada_qtd,usuario,metodo_pag,)) # botao para adicionar produto
    botao_comprar.pack(pady=5)
    Carregar_dados_tabela(tabela,usuario) # quando iniciar carregar dados do bd na tabela

