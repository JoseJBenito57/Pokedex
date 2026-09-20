import io
from PIL import Image
import requests
from pokedex.api_client import get_ability_name_es

TRADUCCION_TIPOS: dict[str, str] = {
    "normal": "Normal",
    "fire": "Fuego",
    "water": "Agua",
    "electric": "Eléctrico",
    "grass": "Planta",
    "ice": "Hielo",
    "fighting": "Lucha",
    "poison": "Veneno",
    "ground": "Tierra",
    "flying": "Volador",
    "psychic": "Psíquico",
    "bug": "Bicho",
    "rock": "Roca",
    "ghost": "Fantasma",
    "dragon": "Dragón",
    "steel": "Acero",
    "fairy": "Hada",
    "dark": "Siniestro",
    "stellar": "Astral",
    "unknown": "Desconocido",
}



class Pokemon:
    def __init__(self, data: dict, species_data: dict | None = None):
        # 1. Identificación básica
        self.id: int = data["id"]
        nombre_crudo = data["name"]
        self.name: str = nombre_crudo.capitalize()

        # 2. Extracción desarrollada de tipos traducidos
        self.types: list[str] = []
        for elemento_tipo in data["types"]:
            nombre_en_ingles = elemento_tipo["type"]["name"].lower()
            # Buscamos en el diccionario. Si por alguna razón no existiera, dejamos el original capitalizado
            nombre_espanol = TRADUCCION_TIPOS.get(
                nombre_en_ingles, nombre_en_ingles.capitalize()
            )
            self.types.append(nombre_espanol)

        # 3. Extracción desarrollada de habilidades traducidas
        self.abilities: list[str] = []
        for elemento_habilidad in data["abilities"]:
            info_habilidad = elemento_habilidad["ability"]
            nombre_en_ingles = info_habilidad["name"]
            url_habilidad = info_habilidad["url"]

            # Consultamos la traducción oficial
            nombre_en_espanol = get_ability_name_es(url_habilidad)

            # Si encontramos el nombre en español lo usamos; si no, dejamos el nombre en inglés
            if nombre_en_espanol is not None:
                self.abilities.append(nombre_en_espanol)
            else:
                self.abilities.append(nombre_en_ingles.capitalize())

        # 4. Extracción desarrollada de estadísticas base
        self.stats: dict[str, int] = {}
        for elemento_stat in data["stats"]:
            nombre_stat = elemento_stat["stat"]["name"]
            valor_stat = elemento_stat["base_stat"]
            self.stats[nombre_stat] = valor_stat

        # 5. Conversión de medidas físicas
        altura_decimetros = data["height"]
        peso_hectogramos = data["weight"]
        self.height_m: float = round(altura_decimetros * 0.1, 2)
        self.weight_kg: float = round(peso_hectogramos * 0.1, 2)

        # 6. Extracción de audio (cries)
        diccionario_cries = data.get("cries")
        if diccionario_cries is not None:
            self.cry_url: str | None = diccionario_cries.get("latest")
        else:
            self.cry_url = None

        # 7. Extracción de sprites
        diccionario_sprites = data.get("sprites")
        if diccionario_sprites is not None:
            self.sprite_default: str | None = diccionario_sprites.get("front_default")
            self.sprite_shiny: str | None = diccionario_sprites.get("front_shiny")
        else:
            self.sprite_default = None
            self.sprite_shiny = None

        # 8. Extracción de datos narrativos en español (desde species_data)
        self.category: str = "Categoría desconocida"
        self.description: str = "Descripción no disponible en español."

        if species_data is not None:
            # Buscar categoría en español (ej: "Pokémon Ratón")
            lista_generos = species_data.get("genera", [])
            for genero in lista_generos:
                idioma = genero.get("language", {}).get("name")
                if idioma == "es":
                    self.category = genero.get("genus", "")
                    break

            # Buscar descripción en español
            entradas_texto = species_data.get("flavor_text_entries", [])
            for entrada in entradas_texto:
                idioma = entrada.get("language", {}).get("name")
                if idioma == "es":
                    texto_crudo = entrada.get("flavor_text", "")
                    # Limpieza de saltos de línea molestos
                    self.description = (
                        texto_crudo.replace("\n", " ")
                        .replace("\x0c", " ")
                        .replace("\f", " ")
                    )
                    break

    def __str__(self) -> str:
        tipos_texto = ", ".join(self.types)
        habilidades_texto = ", ".join(self.abilities)

        lista_stats = []
        for clave, valor in self.stats.items():
            lista_stats.append(f"{clave.upper()}: {valor}")
        stats_texto = " | ".join(lista_stats)

        separador = "=" * 55
        return (
            f"{separador}\n"
            f"#{self.id:03d} - {self.name} ({self.category})\n"
            f"{separador}\n"
            f"Descripción:  {self.description}\n"
            f"Tipos:        {tipos_texto}\n"
            f"Habilidades:  {habilidades_texto}\n"
            f"Altura/Peso:  {self.height_m} m / {self.weight_kg} kg\n"
            f"Stats:        {stats_texto}\n"
            f"Audio Cry:    {self.cry_url}\n"
            f"Sprite:       {self.sprite_default}\n"
            f"Sprite Shiny: {self.sprite_shiny}\n"
            f"{separador}"
        )

    def mostrar_sprite(self, shiny: bool = False) -> None:
        """
        Descarga el sprite en memoria usando requests y lo abre
        en una ventana emergente usando Pillow.
        Si shiny=True, muestra la versión variocolor.
        """
        url_imagen = self.sprite_shiny if shiny else self.sprite_default

        if url_imagen is None:
            print("No hay imagen disponible para este Pokémon.")
            return

        try:
            # 1. Descargamos los bytes de la imagen
            respuesta = requests.get(url_imagen, timeout=5)

            if respuesta.status_code == 200:
                # 2. Convertimos los bytes crudos en un flujo legible en memoria
                flujo_bytes = io.BytesIO(respuesta.content)

                # 3. Pillow procesa los datos
                imagen = Image.open(flujo_bytes)

                # 4. Abre la imagen en una ventana de Windows
                tipo_version = "Shiny" if shiny else "Normal"
                print(f"Abriendo sprite ({tipo_version})...")
                imagen.show()
            else:
                print(f"Error al descargar la imagen: Código {respuesta.status_code}")

        except requests.RequestException as error:
            print(f"Error de red al descargar el sprite: {error}")