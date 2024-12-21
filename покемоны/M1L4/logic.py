from random import randint
import requests
from random import randint, choices
import json

class Pokemon:
    pokemons = {}
    LEVEL_UP_XP = {1: 100, 2:200, 3: 400, 4:800, 5:1600} # Пример кривой опыта
    RARITY_WEIGHTS = [0.9, 0.09, 0.01]  # Вероятности: обычный, редкий, легендарный


    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.fetch_pokemon_data()
        self.level = 1
        self.xp = 0
        self.achievements = []
        self.fed = False # Добавлено свойство, показывающее кормили ли покемона


        Pokemon.pokemons[pokemon_trainer] = self

    def fetch_pokemon_data(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            self.name = data['name']
            self.img = data["sprites"]["front_default"]
            self.types = [type_data['type']['name'] for type_data in data['types']]
            self.abilities = [ability_data['ability']['name'] for ability_data in data['abilities']]
            self.height = data['height']
            self.weight = data['weight']
            self.base_stats = {stat_data['stat']['name']: stat_data['base_stat'] for stat_data in data['stats']}
            self.rarity = choices(["common", "rare", "legendary"], weights=Pokemon.RARITY_WEIGHTS)[0]

        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
            self.handle_api_error()

        except KeyError as e:
            print(f"Ошибка в данных API: {e}, pokemon_number: {self.pokemon_number}")
            self.handle_api_error()

    def handle_api_error(self):
        self.name = "Pikachu"
        self.img = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
        self.types = ["Electric"]
        self.abilities = ["Static"]
        self.height = 4
        self.weight = 60
        self.base_stats = {"hp": 35, "attack": 55, "defense": 40, "special-attack": 50, "special-defense": 50, "speed": 90}
        self.rarity = "common"


    def get_name(self):
        return self.name

    # ... (другие геттеры и сеттеры остаются без изменений) ...

    def feed(self, amount=10): # Добавлено: кормление покемона
        self.xp += amount
        self.fed = True
        self.level_up()
        return f"Покемон {self.name} поел!  XP + {amount}"


    def level_up(self):
        next_level_xp = Pokemon.LEVEL_UP_XP.get(self.level + 1, float('inf')) #получаем нужное кол-во очков опыта для повышения уровня,  float('inf') -  максимальное значение
        if self.xp >= next_level_xp:
            self.level += 1
            self.xp -= next_level_xp
            self.achievements.append(f"Достижение: Достигнут уровень {self.level}!")
            print(f"Покемон {self.name} достиг уровня {self.level}!")

    def get_level(self):
        return self.level

    def get_xp(self):
        return self.xp

    def get_achievements(self):
        return self.achievements

    def get_rarity(self):
        return self.rarity

    def get_bonus(self): #получение бонуса за редкого покемона
        if self.rarity == "rare":
            return "Вы получили редкий предмет!"
        elif self.rarity == "legendary":
            return "Вы получили легендарный предмет!"
        else:
            return ""


    def info(self):
        stats_str = "\n".join([f"{stat}: {value}" for stat, value in self.base_stats.items()])
        return f"Тренер: {self.pokemon_trainer}\nИмя покемона: {self.name}\nРедкость: {self.rarity}\nТипы: {', '.join(self.types)}\nСпособности: {', '.join(self.abilities)}\nРост: {self.height}\nВес: {self.weight}\nСтаты:\n{stats_str}\nУровень: {self.level}\nОпыт: {self.xp}\nДостижения: {', '.join(self.achievements)}\nБонус: {self.get_bonus()}"

    def show_img(self):
        if self.img:
            return self.img
        else:
            return "Изображение не найдено."

class Pokemon:
    pokemons = {} # { username : pokemon}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()

        self.power = randint(30, 60)
        self.hp = randint(200, 400)

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']["other"]['official-artwork']["front_default"])
        else:
            return "https://static.wikia.nocookie.net/anime-characters-fight/images/7/77/Pikachu.png/revision/latest/scale-to-width-down/700?cb=20181021155144&path-prefix=ru"

    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    # Метод класса для получения информации
    def info(self):
        return f"""Имя твоего покеомона: {self.name}
Cила покемона: {self.power}
Здоровье покемона: {self.hp}"""

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img

    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1,5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"""Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}
Здоровье @{enemy.pokemon_trainer} теперь {enemy.hp}"""
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

class Wizard(Pokemon):

    def info(self): # доп. задание
        return "У тебя покемон-волшебник \n\n" + super().info()

class Fighter(Pokemon):
    def attack(self, enemy):
        super_power = randint(5,15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой:{super_power} "

    def info(self): # доп. задание
        return "У тебя покемон-боец \n\n" + super().info()
