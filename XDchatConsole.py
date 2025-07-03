import socket
import threading
import time

 
# Настройки подключения
SERVER = "irc.libera.chat"
PORT = 6667
CHANNEL = "#XDchatOnly"
NICKNAME = "XDchatUser"  # Можешь поменять на свой ник
USERNAME = "simpleuser"
REALNAME = "Simple IRC Client"

def receive_messages(irc_socket):
    while True:
        try:
            data = irc_socket.recv(2048).decode('utf-8', errors='ignore')
            if not data:
                break
            print(data.strip())
            
            # Отвечаем на PING (обязательно для поддержания соединения)
            if data.startswith("PING"):
                irc_socket.send(("PONG " + data.split()[1] + "\r\n").encode())
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            break

def send_message(irc_socket, message):
    try:
        irc_socket.send(f"PRIVMSG {CHANNEL} :{message}\r\n".encode())
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

def main():
    irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        irc_socket.connect((SERVER, PORT))
    except Exception as e:
        print(f"Не удалось подключиться: {e}")
        return
    
    # Регистрируемся на сервере
    irc_socket.send(f"NICK {NICKNAME}\r\n".encode())
    irc_socket.send(f"USER {USERNAME} 0 * :{REALNAME}\r\n".encode())
    
    # Ждем, пока сервер обработает регистрацию
    time.sleep(2)
    
    # Входим в канал
    irc_socket.send(f"JOIN {CHANNEL}\r\n".encode())
    
    # Запускаем поток для приема сообщений
    recv_thread = threading.Thread(target=receive_messages, args=(irc_socket,))
    recv_thread.daemon = True
    recv_thread.start()
    
    print(f"Подключено к {SERVER}, канал: {CHANNEL}")
    print("Вводи сообщения (или 'exit' для выхода):")
    
    try:
        while True:
            message = input().strip()
            if message.lower() == 'exit':
                break
            if message:
                send_message(irc_socket, message)
    except KeyboardInterrupt:
        print("\nВыход...")
    finally:
        irc_socket.send(f"PART {CHANNEL}\r\n".encode())
        irc_socket.send("QUIT :Goodbye!\r\n".encode())
        irc_socket.close()

if __name__ == "__main__":
    main()
