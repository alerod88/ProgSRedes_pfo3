# PFO 3 - Rediseño como Sistema Distribuido (Cliente-Servidor)

## Arquitectura del Sistema
El sistema implementa una arquitectura distribuida basada en Sockets TCP, distribuyendo el procesamiento de tareas hacia workers mediante pools de hilos concurrentes.

### Diagrama de Bloques
- **Clientes (Web/Móviles):** Envían peticiones de tareas al sistema.
- **Balanceador de Carga (Nginx/HAProxy):** Distribuye el tráfico entrante de manera equitativa.
- **Servidor Principal (Python Sockets):** Recibe las solicitudes TCP y las gestiona.
- **Cola de Mensajes (RabbitMQ) / Workers:** Procesan las tareas de forma asincrónica mediante pools de hilos (`ThreadPoolExecutor`).
- **Almacenamiento Distribuido:** PostgreSQL (para datos estructurados y estado de tareas) y Amazon S3 (para archivos/assets pesados).

```text
[ Clientes Web / Móviles ]
           │
           ▼
[ Balanceador de Carga (Nginx / HAProxy) ]
           │
           ▼
[ Servidor Principal / API Server (Python Sockets / TCP) ]
           │
           ▼
[ Cola de Mensajes (RabbitMQ) ]
      ┌────┴────┐
      ▼         ▼
[ Worker 1 ] [ Worker 2 ]  (Pool de hilos con ThreadPoolExecutor)
      │         │
      └────┬────┘
           ▼
[ Almacenamiento Distribuido ]
  ├── PostgreSQL (Datos estructurados / Estado de Tareas)
  └── Amazon S3 (Archivos / Assets pesados)