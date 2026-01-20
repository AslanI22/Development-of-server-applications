# client.py
import socket
import time


def main():
    host = "localhost"
    port = 1503

    try:
        # Подключаемся к промежуточному клиенту
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("Подключено к серверу")

        # Получаем историю сообщений
        data = sock.recv(4096)
        if data:
            print("История сообщений:")
            print(data.decode())

        print("\nОжидание новых сообщений...")

        # Получаем новые сообщения
        while True:
            data = sock.recv(1024)
            if data:
                message = data.decode()
                print(f"\nНовое сообщение: {message}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nКлиент остановлен")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
