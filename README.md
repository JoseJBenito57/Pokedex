# Pokédex Interactiva en Python

Aplicación de consola interactiva construida en Python para consultar información, narrativa y multimedia de Pokémon utilizando la [PokéAPI](https://pokeapi.co/).

El proyecto destaca por desacoplar la arquitectura en capas (cliente de red, modelo de datos y capa de presentación), traducir dinámicamente el contenido al español y procesar imágenes directamente en memoria volátil sin persistencia en disco.

---

## Características

- **Consulta interactiva en consola:** Búsqueda continua por nombre o ID numérico de la Pokédex Nacional, con manejo de errores y salida limpia.
- **Localización oficial al español:**
  - Categoría de la especie (ej. *Pokémon Ratón* para Pikachu) extraída de `/pokemon-species/`.
  - Descripción de la Pokédex oficial en español depurada de saltos de control retro (`\n`, `\f`, `\x0c`).
  - Nombres de habilidades traducidos mediante consultas específicas al endpoint `/ability/`.
  - Tipos traducidos mediante mapeo controlado.
- **Métricas normalizadas:** Altura en metros y peso en kilogramos con conversión matemática y redondeo seguro.
- **Estadísticas base estructuradas:** Diccionario con los 6 stats base del Pokémon (*HP, Attack, Defense, Special-Attack, Special-Defense, Speed*).
- **Procesamiento de imágenes en memoria:** Descarga de sprites (normal y variocolor/shiny) usando `requests`, flujo de bytes en RAM mediante `io.BytesIO` y apertura en visor nativo con `Pillow`.
- **Registro de audio:** Enlace directo al sonido clásico o moderno (*cries*) listo para reproducir.

---

## Arquitectura del Proyecto

El código está estructurado siguiendo principios de código limpio, modularidad y alta legibilidad:

```text
pokedex/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
└── src/
    └── pokedex/
        ├── __init__.py      # Marca el paquete Python
        ├── api_client.py    # Capa de consumo HTTP y gestión de endpoints
        ├── pokemon.py       # Modelo de datos, normalización y Pillow
        └── main.py          # Interfaz de usuario interactiva por CLI
Requisitos Previos
Python 3.10 o superior.

Gestor de paquetes y entornos uv.

Instalación y Configuración
Clonar el repositorio:

Bash
git clone [https://github.com/TU_USUARIO/pokedex.git](https://github.com/TU_USUARIO/pokedex.git)
cd pokedex
Sincronizar el entorno virtual y dependencias con uv:

Bash
uv sync
Uso
Para iniciar el menú interactivo, ejecuta:

Bash
uv run python -m pokedex.main
Ejemplo de uso en terminal:
Plaintext
==================================================
           POKÉDEX INTERACTIVA
==================================================
Escribe el nombre o número de un Pokémon.
Escribe 'salir' para cerrar la aplicación.
--------------------------------------------------

Introduce Pokémon o ID > psyduck

Consultando información de 'psyduck'...

=======================================================
#054 - Psyduck (Pokémon Pato)
=======================================================
Descripción:  Padece continuamente dolores de cabeza. Cuando son muy fuertes, empieza a usar misteriosos poderes.
Tipos:        Agua
Habilidades:  Humedad, Aclimatación, Nado Rápido
Altura/Peso:  0.8 m / 19.6 kg
Stats:        HP: 50 | ATTACK: 52 | DEFENSE: 48 | SPECIAL-ATTACK: 65 | SPECIAL-DEFENSE: 50 | SPEED: 55
Audio Cry:    [https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/54.ogg](https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/54.ogg)
Sprite:       [https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/54.png](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/54.png)
Sprite Shiny: [https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/54.png](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/54.png)
=======================================================

¿Ver sprite? [1: Normal | 2: Shiny | Enter: Omitir] > 1
Abriendo sprite (Normal)...
Dependencias Principales
requests: Consumo y descarga de datos HTTP/REST.

Pillow: Procesamiento y apertura de imágenes en memoria.

uv: Gestión de entorno, dependencias y empaquetado.

Próximos Pasos (Roadmap)
[ ] Transición de interfaz de consola hacia una API web interactiva con FastAPI.

[ ] Renderizado de tarjeta Pokédex dinámica con HTML/CSS nativo.

[ ] Reproductor directo del audio .ogg de los cries en el navegador.
