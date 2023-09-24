from tkinter import *
import tkinter as tk 
from tkinter import messagebox # importar a classe messagebox
from tkinter import ttk  # importar a classe ttk
from classe_banco import *

nome_bd = "dados.db"
meu_banco = BancoDeDados(nome_bd)

def fazer_login(email,senha):
    cliente = Cliente()
    if(email.get() and senha.get()): # campos nao vazios
        try:
            cliente.set_email(email.get()) # verifica se é um email valido
            cliente.set_senha(senha.get()) #verifica se é uma senha valida
            if(meu_banco.verificar_login(cliente)):
                messagebox.showinfo("login","login sucesso")
            else:
                messagebox.showerror("login","login invalido")
        except Exception as e:
            messagebox.showerror("error",str(e))     
    else:
        messagebox.showerror("error","Login invalido")   



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




    Login = tk.Button(root, text="Fazer Login", command=lambda: (fazer_login(entrada_email,entrada_Senha))) # botao para fazer login com email e senha
    Login.pack(pady=5)

    Cadastrar_cli = tk.Button(root, text="Fazer cadastro", command=lambda: ()) # botao para fazer cadastro de um novo cliente
    Cadastrar_cli.pack(pady=5)
root = Tk()
criar_interface(root)
root.mainloop()