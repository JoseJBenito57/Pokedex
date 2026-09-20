from pokedex.api_client import get_pokemon_data, get_pokemon_species_data
from pokedex.pokemon import Pokemon

def test_pokemon_completo():
    pokemon_a_buscar = "pikachu"
    print(f"Obteniendo información completa de {pokemon_a_buscar}...")

    datos_mecanicos = get_pokemon_data(pokemon_a_buscar)
    datos_especie = get_pokemon_species_data(pokemon_a_buscar)

    if datos_mecanicos:
        pokemon = Pokemon(data=datos_mecanicos, species_data=datos_especie)
        print(pokemon)
    else:
        print("No se pudieron cargar los datos.")

if __name__ == "__main__":
    test_pokemon_completo()