
import socket
import threading
import time
import struct
from datetime import datetime


class SimpleChatServer:
    def __init__(self):
        self.host = "localhost"
        self.tcp_port = 1501
        self.multicast_group = "233.0.0.1"
        self.multicast_port = 1502
        self.messages = []
        self.new_messages = []
        self.running = True
        self.clients = []

    def start_tcp_server(self):
        """TCP сервер для приема сообщений"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.tcp_port))
        server_socket.listen(5)

        print(f"TCP сервер на {self.host}:{self.tcp_port}")

        while self.running:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Новый клиент: {addr}")
                self.clients.append(client_socket)

                # Отправляем историю
                if self.messages:
                    history = "\n".join(self.messages[-10:])
                    client_socket.send(history.encode())

                # Обработчик клиента
                threading.Thread(
                    target=self.handle_client, args=(client_socket,), daemon=True
                ).start()

            except Exception as e:
                if self.running:
                    print(f"Ошибка: {e}")

    def handle_client(self, client_socket):
        """Обрабатывает клиента"""
        try:
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode()
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted = f"[{timestamp}] {message}"

                print(f"Новое сообщение: {formatted}")
                self.new_messages.append(formatted)
                self.messages.append(formatted)

                # Храним последние 50 сообщений
                if len(self.messages) > 50:
                    self.messages = self.messages[-50:]

        except:
            pass
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()

    def start_multicast(self):
        """Рассылка сообщений каждые 10 секунд"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ttl = struct.pack("b", 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

        print(f"Multicast на {self.multicast_group}:{self.multicast_port}")

        while self.running:
            time.sleep(10)

            if self.new_messages:
                messages_to_send = self.new_messages.copy()
                self.new_messages = []

                broadcast_data = "\n".join(messages_to_send)

                try:
                    sock.sendto(
                        broadcast_data.encode(),
                        (self.multicast_group, self.multicast_port),
                    )
                    print(f"Разослано {len(messages_to_send)} сообщений")
                except Exception as e:
                    print(f"Ошибка рассылки: {e}")
            else:
                print("Нет новых сообщений")

        sock.close()

    def start(self):
        """Запускает сервер"""
        print("Сервер чата запущен")

        # TCP в отдельном потоке
        threading.Thread(target=self.start_tcp_server, daemon=True).start()

        # Multicast в основном
        self.start_multicast()

    def stop(self):
        """Останавливает сервер"""
        self.running = False
        for client in self.clients:
            client.close()


if __name__ == "__main__":
    server = SimpleChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
