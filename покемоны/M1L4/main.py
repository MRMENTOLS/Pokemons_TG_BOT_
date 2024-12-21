import telebot
from config import token
import requests
from random import randint

class Pokemon:
    pokemons = {}  # {username: pokemon}

    def __init__(self, pokemon_trainer, pokemon_type="normal"):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.type = pokemon_type  # Added pokemon type
        self.power = randint(30, 60)
        self.hp = randint(200, 400)
        self.base_stats = {'Attack': randint(10, 30), 'Defense': randint(10, 30), 'Speed': randint(10, 30)}
        self.rarity = self.get_rarity()
        self.types = [self.type] #simple type for now
        self.abilities = ["Basic Attack"]
        self.height = randint(10,100) # cm
        self.weight = randint(10, 100) #kg
        self.level = 1
        self.xp = 0
        self.achievements = []

        Pokemon.pokemons[pokemon_trainer] = self


    def get_rarity(self):
        return ["Common", "Uncommon", "Rare", "Epic", "Legendary"][randint(0,4)]

    def get_img(self):
        try:
            url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
            response = requests.get(url)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            return data['sprites']["other"]['official-artwork']["front_default"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image: {e}")
            return "https://static.wikia.nocookie.net/anime-characters-fight/images/7/77/Pikachu.png/revision/latest/scale-to-width-down/700?cb=20181021155144&path-prefix=ru"


    def get_name(self):
        try:
            url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['forms'][0]['name']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching name: {e}")
            return "Pikachu"

    def info(self):
        stats_str = "\n".join([f"{stat}: {value}" for stat, value in self.base_stats.items()])
        return f"Тренер: {self.pokemon_trainer}\nИмя покемона: {self.name}\nРедкость: {self.rarity}\nТипы: {', '.join(self.types)}\nСпособности: {', '.join(self.abilities)}\nРост: {self.height} см\nВес: {self.weight} кг\nСтаты:\n{stats_str}\nУровень: {self.level}\nОпыт: {self.xp}\nДостижения: {', '.join(self.achievements)}"

    def show_img(self):
        return self.img

    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            if randint(1, 5) == 1:
                return "Покемон-волшебник применил щит в сражении"
        damage = min(self.power, enemy.hp)  # Ensure you don't go below 0 hp
        enemy.hp -= damage
        return f"""Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}
Здоровье @{enemy.pokemon_trainer} теперь {enemy.hp}"""


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer, "magic")
        self.abilities.append("Magic Shield")

    def info(self):
        return "У тебя покемон-волшебник \n\n" + super().info()

    def attack(self, enemy):
        if randint(1, 5) == 1:
            return "Покемон-волшебник применил щит в сражении!"
        return super().attack(enemy)



class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer, "fighting")
        self.abilities.append("Super Attack")

    def attack(self, enemy):
        super_power = randint(5, 15)
        original_power = self.power
        self.power += super_power
        result = super().attack(enemy)
        self.power = original_power #reset power
        return result + f"\nБоец применил супер-атаку силой: {super_power} "

    def info(self):
        return "У тебя покемон-боец \n\n" + super().info()
