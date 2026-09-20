import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon"

def get_pokemon_data(pokemon_identifier: str | int) -> dict | None:
    """
    Consulta la PokéAPI por nombre o número (ID).
    Devuelve el diccionario con los datos o None si hay error.
    """
    identifier = str(pokemon_identifier).strip().lower()
    endpoint = f"{BASE_URL}/{identifier}"

    try:
        response = requests.get(endpoint, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Aviso: El Pokémon '{pokemon_identifier}' no existe en la PokéAPI.")
            return None
        else:
            print(f"Aviso: Error en el servidor ({response.status_code}).")
            return None

    except requests.RequestException as error:
        print(f"Error de red: {error}")
        return None

SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species"

def get_pokemon_species_data(pokemon_identifier: str | int) -> dict | None:
    """
    Realiza una petición GET a la PokéAPI para obtener datos de la especie
    (textos narrativos, descripciones en varios idiomas, categoría, etc.).
    """
    identificador_limpio = str(pokemon_identifier).strip().lower()
    endpoint = f"{SPECIES_URL}/{identificador_limpio}"

    try:
        respuesta = requests.get(endpoint, timeout=5)

        if respuesta.status_code == 200:
            return respuesta.json()
        elif respuesta.status_code == 404:
            print(f"Aviso: La especie '{pokemon_identifier}' no existe.")
            return None
        else:
            print(f"Aviso: Error del servidor ({respuesta.status_code}).")
            return None

    except requests.RequestException as error:
        print(f"Error de red al consultar especie: {error}")
        return None

def get_ability_name_es(ability_url: str) -> str | None:
    """Consulta la URL de una habilidad y devuelve su nombre oficial en español."""
    try:
        respuesta = requests.get(ability_url, timeout=5)
        if respuesta.status_code != 200:
            return None

        datos_habilidad = respuesta.json()
        lista_nombres = datos_habilidad.get("names", [])

        for item_nombre in lista_nombres:
            codigo_idioma = item_nombre.get("language", {}).get("name")
            if codigo_idioma == "es":
                return item_nombre.get("name")

        return None

    except requests.RequestException as error:
        print(f"Error de red al traducir habilidad: {error}")
        return None