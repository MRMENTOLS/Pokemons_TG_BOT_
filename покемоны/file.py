import requests
import json

def get_name(pokemon_number):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return (data['forms'][0]['name'])
    else:
        return "Pikachu"
    
print(get_name(1))