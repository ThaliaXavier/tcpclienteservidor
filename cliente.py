import socket
from datetime import datetime

HOST = 'localhost'
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def registrar_conversa(mensagem):
    with open("conversas_completo.txt", "a") as arquivo:
        arquivo.write(f"{datetime.now()} - {mensagem}\n")

try:
    cliente.connect((HOST, PORT))
    print('Conectado ao servidor.')
except ConnectionRefusedError:
    print('Não foi possível conectar ao servidor.')
    exit()

try:
    while True:
        try:
            cliente.settimeout(0.5) 
            while True:
                data = cliente.recv(1024)
                if data:
                    resposta_servidor = data.decode()
                    print(f"Servidor: {resposta_servidor}")
                    
              
                    registrar_conversa(f"Servidor: {resposta_servidor}")
                else:
                    break
        except socket.timeout:
            pass
        finally:
            cliente.settimeout(None)  

        mensagem = input('Você (cliente): ')
        if mensagem.lower() == 'sair':
            print('Encerrando conexão.')
            break

        cliente.sendall(mensagem.encode())

        registrar_conversa(f"Cliente: {mensagem}")

except KeyboardInterrupt:
    print('\nConexão interrompida pelo usuário.')
finally:
    cliente.close()
    print('Conexão fechada.')