import socket
import socket_config

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print('Connection . . .')
    s.connect((socket_config.SERVER_IP, socket_config.SERVER_PORT)) # Подключаемся к нашему серверу.
    print('Connection: OK')
except Exception as Error:
    print(f'[Errno 111] Connection refused\nlog: {Error}')
    exit(1)
try:
    s.sendall(socket_config.STRING.encode('utf-8')) # Отправляем фразу.
    data = s.recv(1024) #Получаем данные из сокета.
    print(data.decode('utf-8'))
except Exception as Error:
    print(f'! ERROR: {Error}')
    exit(1)