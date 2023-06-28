import tkinter as tk
import bcrypt
import mysql.connector

def tela_registro():
    nome_usuario = entry_usuario.get()
    senha = entry_senha.get()
    confirmar_senha = entry_confirmar_senha.get()
    
    if senha == confirmar_senha:
        # Meu database e conexão
        user_id = registrar_usuario(nome_usuario, senha)
        if user_id:
            label_status["text"] = "Usuário registrado com sucesso! ID do usuário: {}".format(user_id)
            label_status["bg"] = "green"
            limpar_campos()
        else:
            label_status["text"] = "Erro ao registrar usuário."
            label_status["bg"] = "red"
    else:
        label_status["text"] = "As senhas não correspondem. Tente novamente."
        label_status["bg"] = "red"

def tela_login():
    nome_usuario = entry_usuario.get()
    senha = entry_senha.get()
    
    if autenticar_usuario(nome_usuario, senha):
        label_status["text"] = "Login bem-sucedido! Bem-vindo ao sistema."
        label_status["bg"] = "green"
        limpar_campos()
    else:
        label_status["text"] = "Erro de autenticação. Nome de usuário ou senha inválidos."
        label_status["bg"] = "red"

def limpar_campos():
    entry_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_confirmar_senha.delete(0, tk.END)

def registrar_usuario(nome_usuario, senha):
    try:
        # Criptografar a senha
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="acesso123",
            database="cadstro_usuario"
        )
        cursor = conn.cursor()

        # Criar tabela users se ela ainda não existir
        query = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), senha VARCHAR(255))"
        cursor.execute(query)

        query = "INSERT INTO users (nome, senha) VALUES (%s, %s)"
        values = (nome_usuario, hashed_senha.decode('utf-8'))
        cursor.execute(query, values)

        user_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return user_id

    except mysql.connector.Error as error:
        print("Erro ao registrar usuário:", error)
        return None

def autenticar_usuario(nome_usuario, senha):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="acesso123",
            database="cadstro_usuario"
        )
        cursor = conn.cursor()

        query = "SELECT senha FROM users WHERE nome = %s"
        values = (nome_usuario,)
        cursor.execute(query, values)

        result = cursor.fetchone()
        
        conn.close()

        if result:
            # Verificar a senha criptografada
            hashed_senha = result[0].encode('utf-8')
            if bcrypt.checkpw(senha.encode('utf-8'), hashed_senha):
                return True
            else:
                return False
        else:
            return False

    except mysql.connector.Error as error:
        print("Erro ao autenticar usuário:", error)
        return False

window = tk.Tk()
window.title("Meu sistema")
window.configure(bg="lightgray")

label_usuario = tk.Label(window, text="Nome de Usuário:", bg="light green")
label_usuario.pack()
entry_usuario = tk.Entry(window)
entry_usuario.pack(pady=10)

label_senha = tk.Label(window, text="Senha:", bg="light green")
label_senha.pack()
entry_senha = tk.Entry(window, show="*")
entry_senha.pack(pady=10)

label_confirmar_senha = tk.Label(window, text="Confirmar Senha:", bg="light green")
label_confirmar_senha.pack(pady=10)
entry_confirmar_senha = tk.Entry(window, show="*")
entry_confirmar_senha.pack()

button_registrar = tk.Button(window, text="Cadastrar", command=tela_registro, bg="blue", fg="white")
button_registrar.pack(pady=40) 

button_login = tk.Button(window, text="Entrar", command=tela_login,  bg="green", fg="white")
button_login.pack(pady=50)

label_status = tk.Label(window, text="")
label_status.pack()

window.mainloop()
