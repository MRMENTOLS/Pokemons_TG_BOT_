class Car: # Инициализация объекта (конструктор) 
    def __init__(self, make, model, year): 
        self.make = make # Поле или атрибут класса 
        self.model = model # Поле или атрибут класса 
        self.year = year # Поле или атрибут класса
         # Метод класса для получения информации о машине 
        def info(self):
            return f"{self.year} {self.make} {self.model}" 
        # Создаем объекты класса Car 
        car1 = Car("Toyota", "Camry", 2020)
        car2 = Car("Honda", "Civic", 2022) 
        # Используем методы и атрибуты print(car1.info())
        # Выводит: "2020 Toyota Camry" print(car2.info()) # Выводит: "2022 Honda Civic"