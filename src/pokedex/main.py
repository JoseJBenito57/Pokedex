from pokedex.api_client import get_pokemon_data, get_pokemon_species_data
from pokedex.pokemon import Pokemon


def mostrar_encabezado() -> None:
    print("\n" + "=" * 50)
    print("           POKÉDEX INTERACTIVA")
    print("=" * 50)
    print("Escribe el nombre o número de un Pokémon.")
    print("Escribe 'salir' para cerrar la aplicación.")
    print("-" * 50)


def consultar_pokemon(termino_busqueda: str) -> None:
    print(f"\nConsultando información de '{termino_busqueda}'...")

    datos_pokemon = get_pokemon_data(termino_busqueda)
    if datos_pokemon is None:
        print("No se encontró información para el término indicado.")
        return

    datos_especie = get_pokemon_species_data(termino_busqueda)
    pokemon_instancia = Pokemon(data=datos_pokemon, species_data=datos_especie)

    # Mostramos la ficha de texto
    print("\n" + str(pokemon_instancia))

    # Preguntamos si desea ver la imagen
    opcion = input("\n¿Ver sprite? [1: Normal | 2: Shiny | Enter: Omitir] > ").strip()
    if opcion == "1":
        pokemon_instancia.mostrar_sprite(shiny=False)
    elif opcion == "2":
        pokemon_instancia.mostrar_sprite(shiny=True)


def ejecutar_pokedex() -> None:
    mostrar_encabezado()

    while True:
        entrada_usuario = input("\nIntroduce Pokémon o ID > ")
        termino_limpio = entrada_usuario.strip()

        # Condición de salida
        if termino_limpio.lower() in ("salir", "exit", "q"):
            print("\n¡Gracias por usar la Pokédex! Cerrando sesión...")
            break

        # Evitar búsquedas si el usuario solo pulsó Enter
        if termino_limpio == "":
            print("Por favor, introduce un nombre o número válido.")
            continue

        # Realizar la consulta
        consultar_pokemon(termino_limpio)


if __name__ == "__main__":
    ejecutar_pokedex()