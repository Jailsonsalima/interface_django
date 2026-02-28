import socket
import mysql.connector
import json   # para enviar resposta em formato JSON

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 5000))  # escuta em todas as interfaces
    servidor.listen()
    print("Servidor ativo em 0.0.0.0:5000")

    while True:
        conn, addr = servidor.accept()
        query = conn.recv(1024).decode()

        try:
            # Conexão com MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",   # ajuste conforme sua senha
                database="ddb"     # ajuste conforme seu banco
            )
            cursor = db.cursor()
            cursor.execute(query)

            if query.strip().lower().startswith("select"):
                resultado = cursor.fetchall()
            else:
                db.commit()
                resultado = [(f"{cursor.rowcount} linha(s) afetadas",)]

            resposta = {
                "node": addr[0],   # IP do nó que respondeu
                "data": resultado
            }
        except Exception as e:
            resposta = {
                "node": addr[0],
                "data": [(f"Erro ao executar query: {e}",)]
            }

        # envia resposta em JSON para facilitar parsing no Django
        conn.send(json.dumps(resposta).encode())
        conn.close()

if __name__ == "__main__":
    iniciar_servidor()