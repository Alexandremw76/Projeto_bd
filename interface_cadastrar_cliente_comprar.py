from tkinter import *
import tkinter as tk 
from tkinter import messagebox # importar a classe messagebox
from tkinter import ttk  # importar a classe ttk
from classe_banco import *

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




    Login = tk.Button(root, text="Fazer Login", command=lambda: ()) # botao para fazer login com email e senha
    Login.pack(pady=5)

    Cadastrar_cli = tk.Button(root, text="Fazer cadastro", command=lambda: ()) # botao para fazer cadastro de um novo cliente
    Cadastrar_cli.pack(pady=5)
root = Tk()
criar_interface(root)
root.mainloop()