import socket
import json

HOST = 'localhost'
PORT = 6000

def enviar_tarea(tarea_id, descripcion):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))

        payload = {
            "id": tarea_id,
            "descripcion": descripcion
        }

        # Enviar tarea serializada en JSON
        cliente.send(json.dumps(payload).encode('utf-8'))

        # Recibir confirmación/resultado
        respuesta = cliente.recv(1024).decode('utf-8')
        print(f"[Cliente] Respuesta del Servidor: {respuesta}")

        cliente.close()
    except Exception as e:
        print(f"[Cliente] Error al conectar con el servidor: {e}")

if __name__ == "__main__":
    print("--- CLIENTE DE SISTEMA DISTRIBUIDO ---")
    enviar_tarea(101, "Procesamiento de imagen HD")
    enviar_tarea(102, "Generación de reporte PDF")