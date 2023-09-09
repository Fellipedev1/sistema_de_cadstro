import tkinter as tk
import bcrypt
import mysql.connector

COR_BRANCO = "#FFFFFF"
COR_PRETO = "#000000"
COR_VERMELHO = "#FF0000"
COR_VERDE = "#00FF00"
COR_AZUL = "#0000FF"
COR_AMARELO = "#FFFF00"
COR_LARANJA = "#FFA500"
COR_ROXO = "#800080"
COR_ROSA = "#FFC0CB"
COR_CINZA = "#808080"

def tela_registro():
    nome_usuario = entry_usuario.get()
    senha = entry_senha.get()
    confirmar_senha = entry_confirmar_senha.get()
    
    if senha == confirmar_senha:
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
        tela_login_sucesso()
    else:
        label_status["text"] = "Erro de autenticação. Nome de usuário ou senha inválidos."
        label_status["bg"] = "red"

def tela_login_sucesso():
    window.withdraw()
    success_screen = tk.Toplevel()
    success_screen.title("Login Bem-Sucedido")
    success_screen.geometry("400x300")
    label_success = tk.Label(success_screen, text="Este é o software dos colaboradores do ABC")
    label_success.pack(pady=50)

    def voltar_para_login():
        success_screen.destroy()
        window.deiconify()

    button_voltar = tk.Button(success_screen, text="Voltar para o Login", command=voltar_para_login)
    button_voltar.pack()

    def listar_informacoes_funcionarios():
        informacoes = [
            "Funcionário 1 - Cargo 1",
            "Funcionário 2 - Cargo 2",
            "Funcionário 3 - Cargo 3",
            # Adicione mais informações fictícias aqui
        ]
        info_label["text"] = "\n".join(informacoes)

    button_listar_funcionarios = tk.Button(success_screen, text="Listar Funcionários", command=listar_informacoes_funcionarios)
    button_listar_funcionarios.pack(pady=10)

    def mostrar_regras_empresa():
        regras_window = tk.Toplevel()
        regras_window.title("Regras da Empresa")
        regras_window.geometry("400x300")
        regras_label = tk.Label(regras_window, text="Aqui estão as regras da empresa:")
        regras_label.pack(pady=20)
        regras_text = tk.Text(regras_window, height=10, width=40)
        regras_text.pack()
        regras_text.insert(tk.END, "1. Cumprir rigorosamente os horários de trabalho estabelecidos.")
        regras_text.insert(tk.END, "\n2. Tratar todos os colegas de trabalho com respeito e cortesia.")
        regras_text.insert(tk.END, "\n3. Manter a confidencialidade de informações sensíveis da empresa.")
        regras_text.insert(tk.END, "\n4. Utilizar os recursos da empresa de forma responsável e econômica.")
        regras_text.insert(tk.END, "\n5. Relatar imediatamente qualquer problema ou irregularidade ao supervisor.")
        regras_text.insert(tk.END, "\n6. Não é permitido o uso de dispositivos pessoais durante o horário de trabalho, exceto em casos autorizados.")
        regras_text.insert(tk.END, "\n7. Seguir todas as políticas de segurança no local de trabalho.")
        regras_text.insert(tk.END, "\n8. Não é permitido o assédio de qualquer tipo, incluindo assédio sexual.")
        regras_text.insert(tk.END, "\n9. Cumprir todas as políticas de saúde e segurança no trabalho.")
        regras_text.insert(tk.END, "\n10. Participar ativamente de treinamentos e programas de desenvolvimento profissional oferecidos pela empresa.")
        regras_text.insert(tk.END, "\n11. Respeitar a propriedade intelectual e os direitos autorais de terceiros.")
        regras_text.insert(tk.END, "\n12. Cumprir todas as leis e regulamentos aplicáveis relacionados ao trabalho.")
        regras_text.insert(tk.END, "\n13. Evitar conflitos de interesse e divulgar qualquer possível conflito ao departamento de recursos humanos.")
        regras_text.insert(tk.END, "\n14. Manter um ambiente de trabalho limpo e organizado.")
        regras_text.insert(tk.END, "\n15. Promover a diversidade e a inclusão no local de trabalho.")
        regras_text.config(state=tk.DISABLED)

    button_mostrar_regras = tk.Button(success_screen, text="Mostrar Regras da Empresa", command=mostrar_regras_empresa)
    button_mostrar_regras.pack()

    info_label = tk.Label(success_screen, text="", font=("Times New Roman", 12))
    info_label.pack()

def limpar_campos():
    entry_usuario.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_confirmar_senha.delete(0, tk.END)

def registrar_usuario(nome_usuario, senha):
    try:
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        conn = mysql.connector.connect(host="localhost", user="root", password="acesso123", database="cadstro_usuario")
        cursor = conn.cursor()
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
        conn = mysql.connector.connect(host="localhost", user="root", password="acesso123", database="cadstro_usuario")
        cursor = conn.cursor()
        query = "SELECT senha FROM users WHERE nome = %s"
        values = (nome_usuario,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.close()
        if result:
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
window.title("Sistema")
window.configure(bg=COR_LARANJA)

button_grafico = tk.Label(window, text="Sistema de cadastro do ABC", bg=COR_AMARELO, font=("Times New Roman", 16, "bold"))
button_grafico.pack(pady=10)

label_usuario = tk.Label(window, text="Nome de Usuário:", bg=COR_VERDE, fg=COR_PRETO, font=("Arial", 12, "bold"))
label_usuario.pack(pady=10)
entry_usuario = tk.Entry(window, bg=COR_BRANCO, fg=COR_PRETO, font=("Arial", 12))
entry_usuario.pack(pady=5, padx=20)

label_senha = tk.Label(window, text="Senha:", bg=COR_VERDE, fg=COR_PRETO, font=("Arial", 12, "bold"))
label_senha.pack(pady=10)
entry_senha = tk.Entry(window, show="*", bg=COR_BRANCO, fg=COR_PRETO, font=("Arial", 12))
entry_senha.pack(pady=5, padx=20)

label_confirmar_senha = tk.Label(window, text="Confirmar Senha:", bg=COR_VERDE, fg=COR_PRETO, font=("Arial", 12, "bold"))
label_confirmar_senha.pack(pady=10)
entry_confirmar_senha = tk.Entry(window, show="*", bg=COR_BRANCO, fg=COR_PRETO, font=("Arial", 12))
entry_confirmar_senha.pack(pady=5, padx=20)

button_frame = tk.Frame(window, bg=COR_LARANJA)
button_frame.pack(pady=10)

button_registrar = tk.Button(button_frame, text="Cadastrar", command=tela_registro, bg=COR_AZUL, fg=COR_BRANCO, font=("Arial", 12, "bold"))
button_registrar.pack(side=tk.LEFT, padx=10)

button_login = tk.Button(button_frame, text="Entrar", command=tela_login, bg=COR_VERMELHO, fg=COR_BRANCO, font=("Arial", 12, "bold"))
button_login.pack(side=tk.LEFT, padx=10)

label_status = tk.Label(window, text="", font=("Times New Roman", 12))
label_status.pack(pady=10)

button_esqueci_senha = tk.Button(window, text="Esqueci minha senha", command=tela_login, bg=COR_ROSA, fg=COR_PRETO, font=("Times New Roman", 12, "underline"))
button_esqueci_senha.pack(pady=20)

window.mainloop()
