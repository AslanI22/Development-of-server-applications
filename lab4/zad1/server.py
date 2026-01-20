# server.py
import socket
import time
import struct


def load_message():
    """Читает сообщение из файла"""
    try:
        with open("weather.txt", "r") as f:
            return f.read().strip()
    except:
        return "Погода: солнечно, +20°C"


def main():
    group = "233.0.0.1"
    port = 1502

    # Создаем UDP сокет для multicast
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack("b", 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    print(f"Сервер запущен. Multicast: {group}:{port}")

    last_message = ""

    while True:
        try:
            message = load_message()

            # Отправляем только если сообщение изменилось
            if message != last_message:
                sock.sendto(message.encode(), (group, port))
                print(f"Отправлено: {message}")
                last_message = message

            time.sleep(10)

        except KeyboardInterrupt:
            print("Сервер остановлен")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()
