from server import Servidor

HOST = "192.168.100.17"
PORT = 8080

SERVIDOR = Servidor(HOST, PORT)

try:
        while True:
            input("Presione Ctrl+C para cerrar el servidor...\n")
except KeyboardInterrupt:
    print("Cerrando servidor...")