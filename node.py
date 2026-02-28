import socket
import mysql.connector
import json

def iniciar_nodo(ip, port):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip, port))
    servidor.listen()
    print(f"Nó ativo em {ip}:{port}")

    while True:
        conn, addr = servidor.accept()
        query = conn.recv(1024).decode()
        print(f"Recebido: {query}")

        # Executa query no MySQL local
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="ddb"
        )
        cursor = db.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        db.commit()

        conn.send(str(resultado).encode())
        conn.close()