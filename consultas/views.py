from django.shortcuts import render
import socket
import json


# Create your views here.
def home(request):
    return render(request, 'consultas/home.html')

def enviar_query(query, ip="127.0.0.1", port=5000):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((ip, port))
        cliente.send(query.encode())
        resposta = cliente.recv(4096).decode()
        cliente.close()
        return json.loads(resposta)  # converte JSON para dict
    except Exception as e:
        return {"node": "desconhecido", "data": [(f"Erro de conexão: {e}",)]}

def executar_query(request):
    resultado = None
    if request.method == "POST":
        query = request.POST.get("query")
        resultado = enviar_query(query)
    return render(request, "consultas/executar.html", {"resultado": resultado})