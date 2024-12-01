import socket
import threading
import random
from datetime import datetime

respostas_chatbot = {
    "oi": "Olá! Como posso ajudar você?",
    "tudo bem": "Estou bem, obrigado! E você?",
    "qual seu nome": "Eu sou o MiniChatBOT, sempre pronto para ajudar!",
    "ajuda": "Claro! Você pode perguntar sobre: aprendizado, frases motivacionais ou curiosidades.",
}

def chatbot_responder(mensagem):
    mensagem = mensagem.lower().strip()
    for chave in respostas_chatbot:
        if chave in mensagem:
            return respostas_chatbot[chave]
    return "Desculpe, não entendi. Você pode reformular?"

frases_motivacionais = [
    "Acredite em si mesmo e todo o resto virá naturalmente.",
    "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
    "Não pare quando estiver cansado, pare quando tiver terminado.",
    "A única forma de fazer um ótimo trabalho é amar o que você faz.",
    "Nunca é tarde demais para ser o que você poderia ter sido.",
    "Cada dia é uma nova chance para mudar sua vida.",
]

def gerar_frase_motivacional():
    return random.choice(frases_motivacionais)

def modo_aprendizado(tema, resposta_usuario=None):
    desafios = {
        "programação": {
            "pergunta": "Resolva este desafio: Escreva um programa que inverte uma string em Python!",
            "resposta_correta": "string[::-1]"
        },
        "matemática": {
            "pergunta": "Resolva: Qual é o resultado de 12 * 8 - 5?",
            "resposta_correta": "91"
        },
        "idiomas": {
            "pergunta": "Desafio de idiomas: Como se diz 'amigo' em inglês?",
            "resposta_correta": "friend"
        }
    }
    desafio = desafios.get(tema.lower())
    if not desafio:
        return "Tema não disponível. Tente: programação, matemática ou idiomas."
    if resposta_usuario:
        if str(resposta_usuario).strip().lower() == str(desafio["resposta_correta"]).lower():
            return "Parabéns! Sua resposta está correta!"
        else:
            return f"Resposta errada. A resposta correta é: {desafio['resposta_correta']}."
    return desafio["pergunta"]

def gerar_curiosidade():
    curiosidades = [
        "Sabia que o mel nunca estraga? Arqueólogos encontraram mel em tumbas antigas no Egito, e ele ainda estava bom para consumo.",
        "As zebras são pretas com listras brancas, e não o contrário como muitos pensam!",
        "O cérebro humano tem mais conexões do que todas as estrelas da Via Láctea juntas.",
        "O coração de um camarão está localizado em sua cabeça.",
        "As lulas têm três corações e o sangue azul.",
        "A água-viva é composta em 95% por água, tornando-a uma das criaturas mais transparentes do planeta.",
    ]
    return random.choice(curiosidades)


def registrar_conversa(mensagem_cliente, mensagem_servidor):
    with open("conversas_completo.txt", "a") as arquivo:
        arquivo.write(f"{datetime.now()} - Cliente: {mensagem_cliente}\n")
        arquivo.write(f"{datetime.now()} - Servidor: {mensagem_servidor}\n")

def handle_client(conn, addr):
    print(f"Conexão estabelecida com {addr}")
    conn.sendall("Bem-vindo ao MiniChatBOT! Diga 'ajuda' para ver as opções.".encode())
    estado = {"modo": None, "tema": None}

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Conexão encerrada pelo cliente {addr}")
                break

            mensagem_cliente = data.decode().strip()
            print(f"Cliente {addr}: {mensagem_cliente}")

            resposta = ""

            if estado["modo"] == "aprendizado" and estado["tema"]:
                resposta = modo_aprendizado(estado["tema"], mensagem_cliente)
                estado["modo"] = None
                estado["tema"] = None
            elif "aprendizado" in mensagem_cliente.lower():
                tema = mensagem_cliente.split("aprendizado")[-1].strip()
                pergunta = modo_aprendizado(tema)
                if "Tema não disponível" not in pergunta:
                    estado["modo"] = "aprendizado"
                    estado["tema"] = tema
                resposta = pergunta
            elif "curiosidade" in mensagem_cliente.lower():
                resposta = gerar_curiosidade()
            elif "frase motivacional" in mensagem_cliente.lower():
                resposta = gerar_frase_motivacional()
            else:
                resposta = chatbot_responder(mensagem_cliente)

      
            conn.sendall(resposta.encode())
            registrar_conversa(mensagem_cliente, resposta)

    except ConnectionResetError:
        print(f"Conexão com {addr} foi encerrada abruptamente.")
    finally:
        conn.close()
        print(f"Conexão fechada com {addr}")

HOST = '' 
PORT = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print(f"Servidor escutando na porta {PORT}...")

while True:
    conn, addr = servidor.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"Clientes ativos: {threading.active_count() - 1}")