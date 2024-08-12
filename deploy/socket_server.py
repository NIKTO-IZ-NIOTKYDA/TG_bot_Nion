import os
import socket
import socket_config

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket_config.SERVER_IP, socket_config.SERVER_PORT)) # Привязываем серверный сокет к socket_config.SERVER_IP и socket_config.SERVER_PORT порту.
s.listen(1) # Начинаем прослушивать входящие соединения

while True: # Создаем вечный цикл.
    conn, addr = s.accept() # Метод который принимает входящее соединение.
    try:
        data = conn.recv(1024) # Получаем данные из сокета.

        print('Data: ' + data.decode('utf-8')) # Выводим информацию в stdout.

        if data.decode('utf-8') != socket_config.STRING:
            conn.sendall('ValueError'.encode('utf-8'))
        else:
            try:
                os.system(command=socket_config.CAMMAND_COPY)
                os.system(command=socket_config.CAMMAND_UPDATE)
                os.system(command=socket_config.CAMMAND_REMOVE)
                os.system(command=socket_config.CAMMAND_PASTE)
                os.system(command=socket_config.CAMMAND_RESTART)
                conn.sendall('Successfully'.encode('utf-8'))
            except Exception as Error:
                conn.sendall(f'ERROR: {Error}'.encode('utf-8'))
    except BrokenPipeError:
        pass