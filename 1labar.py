# Класс дом 1
class House:
    def __init__(
        self,
        id,
        apartment_number,
        area,
        floor,
        rooms_count,
        street,
        building_type,
        lifetime,
    ):
        self.id = id
        self.apartment_number = apartment_number
        self.area = area
        self.floor = floor
        self.rooms_count = rooms_count
        self.street = street
        self.building_type = building_type
        self.lifetime = lifetime

    def __str__(self):
        return (
            f"Квартира №{self.apartment_number}, {self.rooms_count}-комн., "
            f"{self.area} м², {self.floor} этаж, ул. {self.street}, "
            f"{self.building_type}, срок экспл. {self.lifetime} лет"
        )


def create_houses_array():
    """Создание массива объектов квартир"""
    houses = [
        House(1, 15, 45.5, 2, 2, "Ленина", "Панельный", 50),
        House(2, 28, 65.0, 5, 3, "Пушкина", "Кирпичный", 75),
        House(3, 7, 32.0, 1, 1, "Советская", "Панельный", 45),
        House(4, 42, 85.0, 9, 4, "Центральная", "Монолитный", 100),
        House(5, 19, 55.0, 3, 2, "Ленина", "Кирпичный", 60),
        House(6, 33, 72.5, 6, 3, "Гагарина", "Панельный", 55),
        House(7, 8, 38.0, 2, 1, "Садовая", "Кирпичный", 70),
        House(8, 51, 95.0, 10, 4, "Проспект Мира", "Монолитный", 90),
        House(9, 22, 48.0, 4, 2, "Победы", "Панельный", 50),
        House(10, 36, 68.0, 7, 3, "Ленинградская", "Кирпичный", 65),
    ]
    return houses


def filter_by_rooms(houses, target_rooms):
    """Список квартир с заданным числом комнат"""
    return [house for house in houses if house.rooms_count == target_rooms]


def filter_by_rooms_and_floor_range(houses, target_rooms, min_floor, max_floor):
    """Список квартир с заданным числом комнат и этажом в промежутке"""
    return [
        house
        for house in houses
        if house.rooms_count == target_rooms and min_floor <= house.floor <= max_floor
    ]


def filter_by_area(houses, min_area):
    """Список квартир с площадью, превосходящей заданную"""
    return [house for house in houses if house.area > min_area]


def print_houses_list(houses, title):
    """Вывод списка квартир"""
    print(f"\n{title}:")
    print("-" * 80)
    if not houses:
        print("Квартиры не найдены")
    else:
        for house in houses:
            print(house)
    print()


def interactive_mode():
    """Интерактивный режим с вводом параметров от пользователя"""
    houses = create_houses_array()

    while True:
        print("\n" + "=" * 60)
        print("СИСТЕМА ПОИСКА КВАРТИР")
        print("=" * 60)
        print("1 - Список квартир с заданным числом комнат")
        print("2 - Список квартир с комнатами на этажах в промежутке")
        print("3 - Список квартир с площадью больше заданной")
        print("4 - Показать все квартиры")
        print("0 - Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            try:
                rooms = int(input("Введите количество комнат: "))
                result = filter_by_rooms(houses, rooms)
                print_houses_list(result, f"Квартиры с {rooms} комнатами")
            except ValueError:
                print("Ошибка: введите целое число!")

        elif choice == "2":
            try:
                rooms = int(input("Введите количество комнат: "))
                min_f = int(input("Введите минимальный этаж: "))
                max_f = int(input("Введите максимальный этаж: "))
                result = filter_by_rooms_and_floor_range(houses, rooms, min_f, max_f)
                print_houses_list(
                    result, f"Квартиры с {rooms} комнатами на этажах {min_f}-{max_f}"
                )
            except ValueError:
                print("Ошибка: введите целые числа!")

        elif choice == "3":
            try:
                area = float(input("Введите минимальную площадь: "))
                result = filter_by_area(houses, area)
                print_houses_list(result, f"Квартиры с площадью больше {area} м²")
            except ValueError:
                print("Ошибка: введите число!")

        elif choice == "4":
            print_houses_list(houses, "Все квартиры")

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный выбор!")


# Точка входа
if __name__ == "__main__":
    interactive_mode()
