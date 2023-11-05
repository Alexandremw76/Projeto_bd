from tkinter import *
import tkinter as tk 
from tkinter import messagebox # importar a classe messagebox
from tkinter import ttk  # importar a classe ttk
from classe_banco import *

nome_bd = "dados.db"
meu_banco = BancoDeDados(nome_bd)
    
def Carregar_dados_tabela(tabela,usuario): # carregar dados do bd para tabela
    meu_banco.conectar_bd(nome_bd)
    try:
        meu_banco.conectar_bd(nome_bd)
        lista_de_produtos = meu_banco.listar_produtos(usuario)
        tabela.delete(*tabela.get_children())

        for produto in lista_de_produtos:
            tabela.insert("", "end", values=(str(produto[0]), str(produto[1]), str(produto[2]), str(produto[3]), str(produto[4])))
    except Exception as e:
        print("Erro ao carregar dados para a tabela:", e)
    finally:
        meu_banco.fechar_conexao()

def adicionar_item_banco(tabela, nome, qtd, preco, tamanho,usuario):
    # Input validation
    nome_value = nome.get()
    preco_value = preco.get()
    qtd_value = qtd.get()

    if not (nome_value and preco_value and qtd_value):
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return
    try:
        float(preco_value) 
        int(qtd_value)       
    except ValueError:
        messagebox.showerror("Erro", "Preço e quantidade devem ser números válidos.")
        return
    try:
        produto_ = Produto()
        produto_.set_nome(nome_value)
        produto_.set_valor(preco_value)
        produto_.set_qtd(qtd_value)
        produto_.set_tam(tamanho.get())
        meu_banco.conectar_bd(nome_bd)
        meu_banco.inserir_produto(produto_,usuario)
        Carregar_dados_tabela(tabela,usuario)
        nome.delete(0, tk.END)
        qtd.delete(0, tk.END)
        preco.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        meu_banco.fechar_conexao()

def remover_item_banco(tabela):
    selecao = tabela.selection()
    if not selecao:
        messagebox.showerror("Erro","Nenhum item selecionado")
        return
    for item in selecao:
        id_prod = get_id_produto_selecionado(tabela)
        tabela.delete(item)
        meu_banco.conectar_bd(nome_bd)
        meu_banco.remover_produto(id_prod)  # remover produto do banco de dados
        meu_banco.fechar_conexao()

def get_id_produto_selecionado(tabela): # pegar do bd a id do produto selecionado na tabela
    selecao = tabela.selection()  # Obtém a seleção atual
    if selecao:  # Se houver uma seleção
        for item in selecao:
            Produto_ = tabela.item(item, "values")  # Obtém os valores do item
            print(int(Produto_[0]))
            return int(Produto_[0]) # retornar id do produto na selecionado atual

def get_produto_selecionado_do_bd(tabela): # retorna os dados do produto selecioando(dados vem do banco de dados)
    selecao = tabela.selection()  # Obtém a seleção atual
    if selecao:  # Se houver uma seleção
        for item in selecao:
            Produto_ = tabela.item(item, "values")  # Obtém os valores do item
            return list(Produto_) # retornar produto selecionado atual

def Atualizar_item_banco(tabela, nome, qtd, preco, tam,usuario):
    selecao = tabela.selection()  # Item selecionado na tabela

    if not selecao:
        messagebox.showerror("Erro","Nenhum item selecionado")
        return  # Nenhum item selecionado, sair

    id_prod = get_id_produto_selecionado(tabela)  # ID do produto selecionado
    dados_prod = get_produto_selecionado_do_bd(tabela)  # Dados do produto selecionado

    produto_ = Produto()
    produto_.set_nome(dados_prod[1])
    produto_.set_qtd(dados_prod[2])
    produto_.set_valor(dados_prod[3])
    produto_.set_tam(dados_prod[4])

    novo_nome = nome.get()
    novo_qtd = qtd.get()
    novo_preco = preco.get()
    novo_tam = tam.get()


    # Verifique se há alterações nos campos e atualize o objeto Produto com os novo dados
    if novo_nome and novo_nome != dados_prod[1]:
        try:
            produto_.set_nome(novo_nome)
            nome.delete(0, tk.END)
        except Exception as e:
            nome.delete(0, tk.END)
            messagebox.showerror("Erro","Nome invalido")

    if novo_preco and novo_preco != dados_prod[3]:
        try:
            produto_.set_valor(novo_preco)
            nome.delete(0, tk.END)
        except Exception as e:
            preco.delete(0, tk.END)
            messagebox.showerror("Erro","Valor invalido")

    if novo_qtd and (novo_qtd) != dados_prod[2]:
        try:
            produto_.set_qtd(novo_qtd)
            nome.delete(0, tk.END)
        except Exception as e:
            qtd.delete(0, tk.END)
            messagebox.showerror("Erro","QTD invalido")

    if novo_tam and novo_tam != dados_prod[4]:
        try:
            produto_.set_tam(novo_tam)
        except Exception as e:
            tam.delete(0, tk.END)
            messagebox.showerror("Erro","Tamanho invalido")
    try:
        meu_banco.conectar_bd(nome_bd)
        meu_banco.atualizar_produto(id_prod, produto_,usuario)
        Carregar_dados_tabela(tabela,usuario)
    except Exception as e:
        messagebox.showerror("Erro",str(e))
    finally:
        meu_banco.fechar_conexao()

def pesquisar_por_nome(tabela,nome,botao):
    nome_do_botao = botao.cget("text")
    if(nome_do_botao == "Filtrar Produto por nome" and nome.get()):
        try:
            meu_banco.conectar_bd(nome_bd)
            lista_de_produtos = meu_banco.listar_produtos_por_nome(str(nome.get()))
            if(len(lista_de_produtos)) == 0:
                raise Exception("Nenhum produto foi encontrado!")
            tabela.delete(*tabela.get_children()) # excluir dados da tabela
            for produto in lista_de_produtos: # insere na tabeças da interface
                    tabela.insert("", "end", values=(str(produto[0]),str(produto[1]),str(produto[2]),str(produto[3]),str(produto[4])))
            botao.config(text="Remover filtro")
        except Exception as e:
            messagebox.showerror("Erro",str(e))
        finally:
            meu_banco.fechar_conexao()
    elif(nome_do_botao == "Remover filtro" and nome.get()):
        try:
            meu_banco.conectar_bd(nome_bd)
            lista_de_produtos = meu_banco.listar_produtos()
            tabela.delete(*tabela.get_children()) # excluir dados da tabela
            for produto in lista_de_produtos: # insere na tabeças da interface
                    tabela.insert("", "end", values=(str(produto[0]),str(produto[1]),str(produto[2]),str(produto[3]),str(produto[4])))
            botao.config(text="Filtrar Produto por nome")
        except Exception as e:
            messagebox.showerror("Erro",str(e))
        finally:
            meu_banco.fechar_conexao()
    else:
        messagebox.showerror("Erro","Campo nome esta vazio")

def gerar_relatorio(root,usuario):
    meu_banco.conectar_bd(nome_bd)
    estoque = meu_banco.listar_produtos(usuario)
    if estoque:
        janela_secundaria = tk.Toplevel(root)
        janela_secundaria.geometry("400x400")
        janela_secundaria.title("Relatorio")
        tabela = ttk.Treeview(janela_secundaria, columns=(0,1))
        tabela.heading(0, text="Quantidade total de produtos")
        tabela.heading(1, text="Valor total estoque")
        tabela.column("#0", width=0)
        valor_total = 0
        qtd_total = 0
        for iten in estoque:
            valor_total +=  iten[3] * iten[2]
            qtd_total += iten[2]
        tabela.insert("", "end", values=(qtd_total,valor_total))
        tabela.pack()

        botao_fechar = tk.Button(janela_secundaria, text="Fechar", command=janela_secundaria.destroy)
        botao_fechar.pack()
        meu_banco.fechar_conexao
    else:
        messagebox.showerror("error","banco vazio")
        meu_banco.fechar_conexao

def atualizar_tabela_vendas(vendas,tabela1):
    tabela1.delete(*tabela1.get_children())
    for item in vendas:
            tabela1.insert("", "end", values=(str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6])))
            tabela1.pack()
       
def efetivar_venda(tabela1,vendas):
    selecao = tabela1.selection()  # Obtém a seleção atual
    meu_banco.conectar_bd(nome_bd)
    if selecao:
        for item in selecao:
            Produto_ = tabela1.item(item, "values")  # Obtém os valores do item
            id_venda = int(Produto_[0])  # Obtém o ID da venda como um númeroa
    meu_banco.efetivar_venda(id_venda)
    atualizar_tabela_vendas(vendas,tabela1)

def gerar_relatorio_vendas(root, usuario):
    meu_banco.conectar_bd(nome_bd)
    vendas = meu_banco.vendas_por_vendedor(usuario.get_email())
    if vendas:
        janela_secundaria = tk.Toplevel()
        janela_secundaria.geometry("1000x300")
        janela_secundaria.title("Relatorio")
        tabela1 = ttk.Treeview(janela_secundaria, columns=(0, 1, 2, 3, 4, 5, 6))
        tabela1.heading(0, text="ID venda")
        tabela1.heading(1, text="Nome do produto vendido")
        tabela1.heading(2, text="QTD de produtos vendidos")
        tabela1.heading(3, text="Data da venda")
        tabela1.heading(4, text="Metodo de pagamento")
        tabela1.heading(5, text="Email do Comprador")
        tabela1.heading(6, text="Compra foi efetivada ? ")
        tabela1.column("#0", width=0)

        atualizar_tabela_vendas(vendas,tabela1)

        efitvar_venda = tk.Button(janela_secundaria, text="Efetivar venda", command=lambda: efetivar_venda(tabela1,vendas))
        efitvar_venda.pack()

        janela_secundaria.update()
        botao_fechar = tk.Button(janela_secundaria, text="Fechar", command=janela_secundaria.destroy)
        botao_fechar.pack()

        meu_banco.fechar_conexao()
    else:
        messagebox.showerror("error", "Não há vendas")
        meu_banco.fechar_conexao()

def criar_interface_vender(root,usuario):
    # Cria a janela principal
    root.title("Crud")
    root.geometry("600x650")

    tabela = ttk.Treeview(root, columns=(0, 1, 2, 3,4))
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

    nome = tk.Label(root, text="Nome", font=("Arial", 10))
    nome.pack()
    entrada_nome = tk.Entry(root)
    entrada_nome.pack(pady=5, padx=10) 

    qtd = tk.Label(root, text="Quantidade", font=("Arial", 10))
    qtd.pack()

    entrada_qtd = tk.Entry(root)
    entrada_qtd.pack(pady=5, padx=10)  

    valor = tk.Label(root, text="Preço", font=("Arial", 10))
    valor.pack()
    entrada_valor = tk.Entry(root)
    entrada_valor.pack(pady=5, padx=10) 
    
    tamanho = tk.Label(root, text="Tamanho", font=("Arial", 10))
    tamanho.pack()


    tamanho_var = tk.StringVar(root)
    tamanho_var.set("P")  # Define o valor padrão como p
    # Opções de tamanho
    opcoes_tamanho = ["P", "M", "G", "GG"]
    # Menu suspenso (OptionMenu) para seleção do tamanho
    tamanho_menu = tk.OptionMenu(root, tamanho_var, *opcoes_tamanho)
    tamanho_menu.pack(pady=20)




    adicionar_botao = tk.Button(root, text="Inserir Produto", command=lambda: adicionar_item_banco(tabela, entrada_nome,entrada_qtd,entrada_valor,tamanho_var,usuario)) # botao para adicionar produto
    adicionar_botao.pack(pady=5)

    remover_botao = tk.Button(root, text="Remover Produto Selecionado", command=lambda: remover_item_banco(tabela)) # botao para reomver produto
    remover_botao.pack(pady=5)

    atualizar_botao = tk.Button(root, text="Atualizar Produto Selecionado", command=lambda: Atualizar_item_banco(tabela,entrada_nome,entrada_qtd,entrada_valor,tamanho_var,usuario)) # atualiza produtos
    atualizar_botao.pack(pady=5)

    pesquisar_por_nome_botao = tk.Button(root, text="Filtrar Produto por nome", command=lambda: pesquisar_por_nome(tabela,entrada_nome,pesquisar_por_nome_botao)) # atualiza produtos
    pesquisar_por_nome_botao.pack(pady=5)

    gerar_relatorio_botao = tk.Button(root, text="Gerar relatiro de estoque", command=lambda: gerar_relatorio(root,usuario)) # atualiza produtos
    gerar_relatorio_botao.pack(pady=5)

    gerar_relatorio_vendas_botao = tk.Button(root, text="Gerar relatiro de vendas", command=lambda: gerar_relatorio_vendas(root,usuario)) # atualiza produtos
    gerar_relatorio_vendas_botao.pack(pady=5)

    Carregar_dados_tabela(tabela,usuario) # quando iniciar carregar dados do bd na tabela

