from tkinter import *
import tkinter as tk 
from tkinter import messagebox # importar a classe messagebox
from tkinter import ttk  # importar a classe ttk
from classe_banco import *
from interface_cadastrar_produto import * 
nome_bd = "dados.db"
meu_banco = BancoDeDados(nome_bd)

def fazer_login(email,senha,root):
    cliente = Usuario()
    if(email.get() and senha.get()): # campos nao vazios
        try:
            cliente.set_email(email.get()) # verifica se é um email valido
            cliente.set_senha(senha.get()) #verifica se é uma senha valida
            meu_banco.conectar_bd(nome_bd)
            if(meu_banco.verificar_login(cliente)):
                messagebox.showinfo("login","login sucesso")
                janela_secundaria = tk.Toplevel(root)
                janela_secundaria.geometry("400x400")
                janela_secundaria.title("Cadastro_produtos")
                criar_interface_vender(janela_secundaria,cliente)
                root.withdraw()
            else:
                messagebox.showerror("login","login invalido")
        except Exception as e:
            messagebox.showerror("error",str(e))     
        finally:
            meu_banco.fechar_conexao()
    else:
        messagebox.showerror("error","Login invalido")   

def interface_cadastrar_cliente():                        

    janela_secundaria = tk.Toplevel(root)
    janela_secundaria.geometry("400x400")
    janela_secundaria.title("Cadastro")

    nome_texto= tk.Label(janela_secundaria, text="Nome", font=("Arial", 10))
    nome_texto.pack()

    entrada_nome = tk.Entry(janela_secundaria)
    entrada_nome.pack(pady=5, padx=10) 

    email_texto= tk.Label(janela_secundaria, text="Email", font=("Arial", 10))
    email_texto.pack()

    entrada_email = tk.Entry(janela_secundaria)
    entrada_email.pack(pady=5, padx=10)

    Senha_texto= tk.Label(janela_secundaria, text="Senha", font=("Arial", 10))
    Senha_texto.pack()

    entrada_Senha = tk.Entry(janela_secundaria)
    entrada_Senha.pack(pady=5, padx=10)

    Flamengo_texto= tk.Label(janela_secundaria, text="Torce para o Flamengo ?", font=("Arial", 10))
    Flamengo_texto.pack(pady=5, padx=10)

    Torce_fla = tk.StringVar(janela_secundaria)
    Torce_fla.set("Sim")
    Resposta = ["Sim", "Não"]

    flamengo_menu = tk.OptionMenu(janela_secundaria, Torce_fla, *Resposta)
    flamengo_menu.pack()

    one_texto= tk.Label(janela_secundaria, text="Assiste One piece ?", font=("Arial", 10))
    one_texto.pack(pady=5, padx=10)

    one_assist = tk.StringVar(janela_secundaria)
    one_assist.set("Sim")

    one_menu = tk.OptionMenu(janela_secundaria, one_assist, *Resposta)
    one_menu.pack()

    Cadastrar_cli = tk.Button(janela_secundaria, text="Fazer cadastro", command=lambda: (cadastra_cliente(entrada_nome,entrada_email,entrada_Senha,Torce_fla,one_assist,janela_secundaria))) # botao para fazer cadastro de um novo cliente
    Cadastrar_cli.pack(pady=5)

def cadastra_cliente(entrada_nome,entrada_email,entrada_senha,entrada_flamengo,entrada_one,janela): 
    if(entrada_email.get() and entrada_nome.get() and entrada_senha.get()):
        try:
            cliente1 = Usuario()
            cliente1.set_email(entrada_email.get())
            cliente1.set_nome(entrada_nome.get())
            cliente1.set_senha(entrada_senha.get())
            cliente1.set_flamengo(entrada_flamengo.get())
            cliente1.set_onepiece(entrada_one.get())
            meu_banco.conectar_bd(nome_bd)
            meu_banco.casdastrar_cliente(cliente1)
            messagebox.showinfo("Sucesso","Cliente cadastrado!")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Error",str(e))
        finally:
            meu_banco.fechar_conexao()

def criar_interface(root):
    root.title("Crud")
    root.geometry("600x650")

    email_texto= tk.Label(root, text="Email", font=("Arial", 10))
    email_texto.pack()
    entrada_email = tk.Entry(root)
    entrada_email.pack(pady=5, padx=10) 


    Senha_texto= tk.Label(root, text="Senha", font=("Arial", 10))
    Senha_texto.pack()
    entrada_Senha = tk.Entry(root)
    entrada_Senha.pack(pady=5, padx=10) 

    Login = tk.Button(root, text="Fazer Login", command=lambda: (fazer_login(entrada_email,entrada_Senha,root))) # botao para fazer login com email e senha
    Login.pack(pady=5)

    Cadastrar_cli = tk.Button(root, text="Fazer cadastro", command=lambda: (interface_cadastrar_cliente())) # botao para fazer cadastro de um novo cliente
    Cadastrar_cli.pack(pady=5)
root = Tk()
criar_interface(root)
root.mainloop()