# GenAIOs - Asistente de IA Conversacional

GenAIOs es un asistente de inteligencia artificial basado en Python que puede responder preguntas, realizar operaciones matemáticas y aprender de nuevas interacciones con el usuario.

## Características

- Responde preguntas basándose en una base de conocimientos.
- Aprende nuevas respuestas de manera interactiva.
- Realiza operaciones matemáticas básicas como suma, resta, multiplicación y división.
- Almacena conversaciones en una base de datos SQLite.
- Evita responder preguntas con contenido no ético.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/GenAIOs.git
   cd GenAIOs
   ```
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
   *(Actualmente, el proyecto solo usa módulos estándar de Python, por lo que no requiere paquetes adicionales.)*

## Uso

Ejecuta el asistente con el siguiente comando:

```bash
python main.py
```

El asistente responderá a tus preguntas y podrá aprender nuevas respuestas si usas el formato:

```
aprende: [pregunta] -> [respuesta]
```

Para salir, escribe "salir" o "adiós".

## Archivos principales

- `main.py` - Código principal del asistente.
- `conocimientos.json` - Archivo donde se almacenan los conocimientos aprendidos.
- `conversaciones.db` - Base de datos SQLite donde se guardan las conversaciones.

## Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, haz un fork, realiza tus cambios y envía un pull request.

## Licencia

Este proyecto está bajo la licencia MIT.

---

**Autor:** GenOs




