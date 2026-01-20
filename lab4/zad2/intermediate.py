
import socket
import struct
import threading


class SimpleIntermediate:
    def __init__(self):
        self.multicast_group = "233.0.0.1"
        self.multicast_port = 1502
        self.tcp_port = 1503
        self.tcp_clients = []
        self.running = True

    def start_multicast_receiver(self):
        """Принимает multicast"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", self.multicast_port))

        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print(f"Multicast прием на порту {self.multicast_port}")

        while self.running:
            try:
                data, addr = sock.recvfrom(4096)
                message_batch = data.decode()

                print(f"Получено сообщений: {len(message_batch.splitlines())}")

                # Пересылаем TCP клиентам
                for client in self.tcp_clients[:]:
                    try:
                        client.send(message_batch.encode())
                    except:
                        self.tcp_clients.remove(client)

            except Exception as e:
                if self.running:
                    print(f"Ошибка: {e}")

        sock.close()

    def start_tcp_server(self):
        """TCP сервер для клиентов"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("localhost", self.tcp_port))
        server_socket.listen(5)

        print(f"TCP сервер на порту {self.tcp_port}")

        while self.running:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Подключен клиент: {addr}")
                self.tcp_clients.append(client_socket)

                # Обработчик
                threading.Thread(
                    target=self.handle_client, args=(client_socket,), daemon=True
                ).start()

            except Exception as e:
                if self.running:
                    print(f"Ошибка: {e}")

        server_socket.close()

    def handle_client(self, client_socket):
        """Обрабатывает TCP клиента"""
        try:
            while self.running:
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
        threading.Thread(target=self.start_multicast_receiver, daemon=True).start()
        self.start_tcp_server()


if __name__ == "__main__":
    intermediate = SimpleIntermediate()
    try:
        intermediate.start()
    except KeyboardInterrupt:
        intermediate.running = False
