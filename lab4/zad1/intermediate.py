# intermediate.py
import socket
import struct
import threading


class IntermediateClient:
    def __init__(self):
        self.multicast_group = "233.0.0.1"
        self.multicast_port = 1502
        self.tcp_port = 1503
        self.last_message = ""
        self.message_history = []
        self.tcp_clients = []

    def start_udp_receiver(self):
        """Принимает UDP multicast сообщения"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", self.multicast_port))

        # Вступаем в multicast группу
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("Ожидание multicast сообщений...")

        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode()

            if message != self.last_message:
                self.last_message = message
                self.message_history.append(message)

                # Храним только последние 5 сообщений
                if len(self.message_history) > 5:
                    self.message_history = self.message_history[-5:]

                print(f"Новое сообщение: {message}")

                # Уведомляем TCP клиентов
                for client in self.tcp_clients[:]:
                    try:
                        client.send(message.encode())
                    except:
                        self.tcp_clients.remove(client)

    def start_tcp_server(self):
        """Запускает TCP сервер для конечных клиентов"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("localhost", self.tcp_port))
        sock.listen(5)

        print(f"TCP сервер запущен на порту {self.tcp_port}")

        while True:
            client_socket, addr = sock.accept()
            print(f"Подключен клиент: {addr}")
            self.tcp_clients.append(client_socket)

            # Отправляем историю новому клиенту
            history = "\n".join(self.message_history)
            try:
                client_socket.send(history.encode())
            except:
                pass

            # Запускаем обработчик клиента
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()

    def handle_client(self, client_socket):
        """Обрабатывает TCP клиента"""
        try:
            while True:
                # Просто поддерживаем соединение
                data = client_socket.recv(1024)
                if not data:
                    break
        except:
            pass
        finally:
            if client_socket in self.tcp_clients:
                self.tcp_clients.remove(client_socket)
            client_socket.close()

    def start(self):
        """Запускает промежуточный клиент"""
        # Поток для UDP
        udp_thread = threading.Thread(target=self.start_udp_receiver)
        udp_thread.daemon = True
        udp_thread.start()

        # TCP сервер в основном потоке
        self.start_tcp_server()


if __name__ == "__main__":
    client = IntermediateClient()
    client.start()
