class BankAccount:

    def __init__(self, number, balance=0):
        self.number = number
        self.balance = balance
        self.is_blocked = False

    def deposit(self, amount):
        if not self.is_blocked and amount > 0:
            self.balance += amount
            print(f"На счет {self.number} внесено: {amount}")
        else:
            print("Ошибка внесения средств")

    def withdraw(self, amount):
        if not self.is_blocked and amount > 0 and self.balance >= amount:
            self.balance -= amount
            print(f"Со счета {self.number} снято: {amount}")
        else:
            print("Ошибка снятия средств")

    def block(self):
        self.is_blocked = True
        print(f"Счет {self.number} заблокирован")

    def unblock(self):
        self.is_blocked = False
        print(f"Счет {self.number} разблокирован")

    def __str__(self):
        status = "заблокирован" if self.is_blocked else "активен"
        return f"Счет {self.number}: {self.balance} руб. ({status})"


class Client:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def add_account(self, account_number, initial_balance=0):
        new_account = BankAccount(account_number, initial_balance)
        self.accounts.append(new_account)
        print(f"Добавлен счет {account_number} для {self.name}")

    def get_total_balance(self):
        total = sum(account.balance for account in self.accounts)
        return total

    def get_positive_balance(self):
        positive = sum(acc.balance for acc in self.accounts if acc.balance > 0)
        return positive

    def get_negative_balance(self):
        negative = sum(acc.balance for acc in self.accounts if acc.balance < 0)
        return negative

    def sort_accounts_by_balance(self):
        self.accounts.sort(key=lambda acc: acc.balance, reverse=True)
        print("Счета отсортированы по балансу")

    def show_all_accounts(self):
        print(f"\ Счета клиента {self.name} ")
        for account in self.accounts:
            print(account)
        print(f"Общий баланс: {self.get_total_balance()} руб.")
        print(f"Положительный баланс: {self.get_positive_balance()} руб.")
        print(f"Отрицательный баланс: {self.get_negative_balance()} руб.")


def main():
    client = Client("Иван Иванов")

    client.add_account("1001", 5000)
    client.add_account("1002", -2000)
    client.add_account("1003", 3000)

    client.show_all_accounts()

    client.sort_accounts_by_balance()
    client.show_all_accounts()
    print("\n Операции ")
    client.accounts[0].deposit(1000)
    client.accounts[1].withdraw(500)

    client.accounts[2].block()
    client.accounts[2].deposit(500)

    client.show_all_accounts()


if __name__ == "__main__":
    main()
