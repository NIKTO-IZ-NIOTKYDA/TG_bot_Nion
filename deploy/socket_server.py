import os
import socket
import socket_config
try:
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
                    script = open('script.sh', 'rw')
                    script.write(socket_config.CAMMAND)
                    script.close()
                    os.system('bash script.sh')
                    print('Successfully')
                except Exception as Error:
                    conn.sendall(f'ERROR: {Error}'.encode('utf-8'))
        except BrokenPipeError:
            pass
except Exception as Error:
    print(Error)