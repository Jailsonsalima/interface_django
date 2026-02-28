import socket

def enviar_mensagem(mensagem, ip="127.0.0.1", port=5000):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((ip, port))
    cliente.send(mensagem.encode())
    resposta = cliente.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")
    cliente.close()

if __name__ == "__main__":
    enviar_mensagem("Olá servidor!")