import socket
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import time

HOST = 'localhost'
PORT = 6000

# Pool de hilos para simular el procesamiento de los Workers
executor = ThreadPoolExecutor(max_workers=5)

def procesar_tarea_worker(tarea_id, descripcion):
    """Simula el trabajo realizado por un Worker procesando en background."""
    print(f"[Worker] Procesando tarea ID {tarea_id}: '{descripcion}'...")
    time.sleep(3)  # Simula cómputo pesado o guardado distribuido
    resultado = f"Tarea {tarea_id} completada exitosamente por Worker."
    print(f"[Worker] {resultado}")
    return resultado

def manejar_cliente(cliente_socket, direccion):
    """Maneja la conexión con el cliente y distribuye la tarea."""
    print(f"[Servidor] Cliente conectado desde {direccion}")
    try:
        data = cliente_socket.recv(1024).decode('utf-8')
        if data:
            peticion = json.loads(data)
            tarea_id = peticion.get("id")
            descripcion = peticion.get("descripcion")

            print(f"[Servidor] Recibida tarea {tarea_id}. Enviando a pool de Workers...")
            
            # Enviar la tarea a ejecutar concurrentemente en el pool de hilos worker
            future = executor.submit(procesar_tarea_worker, tarea_id, descripcion)
            
            # Responder al cliente confirmando la recepción y encolamiento
            respuesta = {
                "status": "EN PROCESO",
                "mensaje": f"Tarea {tarea_id} distribuida a worker.",
                "id": tarea_id
            }
            cliente_socket.send(json.dumps(respuesta).encode('utf-8'))
    except Exception as e:
        error_res = {"status": "ERROR", "mensaje": str(e)}
        cliente_socket.send(json.dumps(error_res).encode('utf-8'))
    finally:
        cliente_socket.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(10)
    print(f"[Servidor Distribuido] Escuchando en {HOST}:{PORT}...")

    while True:
        cliente, addr = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(cliente, addr))
        hilo.start()

if __name__ == "__main__":
    iniciar_servidor()