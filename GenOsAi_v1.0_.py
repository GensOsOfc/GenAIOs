import sqlite3
from datetime import datetime
import re
import json
import os
from difflib import get_close_matches

# Configuración
DB_NAME = 'conversaciones.db'
CONOCIMIENTOS_FILE = 'conocimientos.json'

# Funciones principales
def cargar_conocimientos():
    def encontrar_archivo_insensible():
        nombre_base = CONOCIMIENTOS_FILE.lower()
        for archivo in os.listdir():
            if archivo.lower() == nombre_base:
                return archivo
        return None

    archivo_real = encontrar_archivo_insensible()
    conocimientos = {}
    
    if archivo_real and os.path.exists(archivo_real):
        try:
            with open(archivo_real, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                # Normalizar las claves al cargar
                for key, value in datos.items():
                    clave_normalizada = normalizar_texto(key)
                    conocimientos[clave_normalizada] = value
        except (json.JSONDecodeError, UnicodeDecodeError):
            print(f"Error: El archivo {archivo_real} está corrupto o mal formateado.")
    
    return conocimientos

def guardar_conocimientos(conocimientos):
    with open(CONOCIMIENTOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(conocimientos, f, ensure_ascii=False, indent=2)

def crear_conexion():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''CREATE TABLE IF NOT EXISTS conversaciones
                    (id INTEGER PRIMARY KEY, usuario TEXT, ia TEXT, timestamp TEXT)''')
    return conn

def guardar_conversacion(conn, usuario, ia):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conn:
        conn.execute("INSERT INTO conversaciones (usuario, ia, timestamp) VALUES (?, ?, ?)",
                     (usuario, ia, timestamp))

def extraer_numeros(texto):
    return [int(s) for s in re.findall(r'\b\d+\b', texto)]

def es_etico(lower_entrada):
    palabras_prohibidas = {'matar', 'robar', 'dañar', 'herir', 'ilegal', 'hackear'}
    return not any(palabra in lower_entrada for palabra in palabras_prohibidas)

def normalizar_texto(texto):
    # Eliminar signos de puntuación y convertir a minúsculas
    texto = re.sub(r'[^\w\s]', '', texto.lower())
    # Eliminar espacios adicionales
    return re.sub(r'\s+', ' ', texto).strip()

def buscar_coincidencias_conocimiento(entrada, conocimientos):
    entrada_normalizada = normalizar_texto(entrada)
    
    # 1. Búsqueda exacta
    if entrada_normalizada in conocimientos:
        return conocimientos[entrada_normalizada]
    
    # 2. Búsqueda por coincidencia parcial
    for clave, valor in conocimientos.items():
        if clave in entrada_normalizada:
            return valor
    
    # 3. Coincidencia aproximada con todo el contexto
    claves = list(conocimientos.keys())
    coincidencias = get_close_matches(entrada_normalizada, claves, n=1, cutoff=0.7)
    
    if coincidencias:
        return conocimientos[coincidencias[0]]
    
    # 4. Búsqueda por palabras clave importantes
    palabras_entrada = entrada_normalizada.split()
    for clave in claves:
        palabras_clave = clave.split()
        if len(set(palabras_clave) & set(palabras_entrada)) >= 2:
            return conocimientos[clave]
    
    return None

def procesar_entrada(entrada):
    lower_entrada = entrada.lower()
    if not es_etico(lower_entrada):
        return "Lo siento, no puedo ayudar con eso por razones éticas."
    
    # Operaciones matemáticas
    tokens = set(lower_entrada.split())
    numeros = extraer_numeros(entrada)
    
    operaciones = [
        ({'sumar', 'más'}, sum, None, "La suma es {}."),
        ({'restar', 'menos'}, lambda n: n[0]-n[1], 2, "La resta es {}."),
        ({'multiplicar', 'por'}, lambda n: n[0]*n[1], 2, "La multiplicación es {}."),
        ({'dividir', 'entre'}, lambda n: n[0]/n[1], 2, "La división es {}.")
    ]
    
    for keywords, funcion, req, mensaje in operaciones:
        if keywords & tokens:
            if req is None or len(numeros) == req:
                try:
                    return mensaje.format(funcion(numeros))
                except ZeroDivisionError:
                    return "No se puede dividir por cero."
            else:
                return f"Proporciona exactamente {req} números para esta operación."
    
    # Búsqueda en conocimientos
    respuesta_conocimiento = buscar_coincidencias_conocimiento(entrada, conocimientos)
    if respuesta_conocimiento:
        return respuesta_conocimiento
    
    return "No tengo una respuesta para eso. ¿Puedes enseñarme?"

def aprender(pregunta, respuesta):
    clave = normalizar_texto(pregunta)
    conocimientos[clave] = respuesta
    guardar_conocimientos(conocimientos)
    return f"Gracias por enseñarme sobre '{clave}'. Lo he guardado."

def conversar():
    print("¡Hola! Soy GenAIOs v1.0, tu IA asistente.")
    print("Puedo ayudarte con operaciones matemáticas, responder preguntas y aprender de ti.")
    print("Escribe 'salir' o 'adiós' para terminar.")

    conn = crear_conexion()
    
    while True:
        usuario = input("Tú: ").strip()
        if usuario.lower() in {'salir', 'adiós'}:
            print("GenAIOs: ¡Hasta luego!")
            break
        
        if usuario.lower().startswith('aprende:'):
            partes = usuario[8:].split('->', 1)
            if len(partes) == 2:
                ia = aprender(partes[0].strip(), partes[1].strip())
            else:
                ia = "Formato incorrecto. Usa: 'aprende: [pregunta] -> [respuesta]'"
        else:
            ia = procesar_entrada(usuario)
        
        print(f"GenAIOs: {ia}")
        guardar_conversacion(conn, usuario, ia)
    
    conn.close()


conocimientos = cargar_conocimientos()


if __name__ == "__main__":
    conversar()