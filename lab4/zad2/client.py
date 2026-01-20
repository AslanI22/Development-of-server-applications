
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext


class SimpleChatClient:
    def __init__(self):
        self.server_host = "localhost"
        self.server_port = 1501
        self.receive_port = 1503
        self.send_socket = None
        self.receive_socket = None
        self.running = False
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Простой чат")
        self.root.geometry("500x400")

        # Область чата
        self.chat_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, height=20, state=tk.DISABLED
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Фрейм ввода
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.message_entry = tk.Entry(input_frame, width=40)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = tk.Button(
            input_frame, text="Отправить", command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Кнопка подключения
        self.connect_button = tk.Button(
            self.root,
            text="Подключиться",
            command=self.toggle_connection,
            bg="lightgreen",
        )
        self.connect_button.pack(fill=tk.X, padx=10, pady=5)

        # Статус
        self.status_label = tk.Label(self.root, text="Не подключено", fg="red")
        self.status_label.pack()

    def toggle_connection(self):
        """Подключается или отключается"""
        if not self.running:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        """Подключается к серверу"""
        try:
            # Сокет для отправки
            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_socket.connect((self.server_host, self.server_port))

            # Сокет для получения
            self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.receive_socket.connect((self.server_host, self.receive_port))

            self.running = True
            self.connect_button.config(text="Отключиться", bg="lightcoral")
            self.status_label.config(text="Подключено", fg="green")
            self.display_message("=== ПОДКЛЮЧЕНО К ЧАТУ ===")

            # Запускаем прием сообщений
            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            self.display_message(f"Ошибка подключения: {e}")

    def disconnect(self):
        """Отключается от сервера"""
        self.running = False
        if self.send_socket:
            self.send_socket.close()
        if self.receive_socket:
            self.receive_socket.close()

        self.connect_button.config(text="Подключиться", bg="lightgreen")
        self.status_label.config(text="Не подключено", fg="red")
        self.display_message("=== ОТКЛЮЧЕНО ===")

    def send_message(self):
        """Отправляет сообщение"""
        if not self.running:
            self.display_message("Сначала подключитесь к серверу!")
            return

        message = self.message_entry.get().strip()
        if message:
            try:
                self.send_socket.send(message.encode())
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.display_message(f"Ошибка отправки: {e}")

    def receive_messages(self):
        """Принимает сообщения от сервера"""
        buffer = ""
        while self.running:
            try:
                data = self.receive_socket.recv(4096)
                if not data:
                    break

                buffer += data.decode("utf-8")

                # Обрабатываем полные сообщения
                if "\n" in buffer:
                    lines = buffer.split("\n")
                    for line in lines[:-1]:
                        if line.strip():
                            self.display_message(line)
                    buffer = lines[-1]

            except:
                break

    def display_message(self, message):
        """Показывает сообщение в чате"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{message}\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def run(self):
        """Запускает приложение"""
        self.root.mainloop()
        self.running = False


if __name__ == "__main__":
    client = SimpleChatClient()
    client.run()
