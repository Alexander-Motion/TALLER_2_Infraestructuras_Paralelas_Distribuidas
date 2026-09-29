import os
import queue
import threading
import time

# Funciones para cada tarea (descomposición funcional)

def leer_archivo(ruta, cola_salida):
    try:
        with open(ruta, 'r', encoding='utf-8') as f_in:
            for linea in f_in:
                cola_salida.put(linea)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta}")
    
    # mandamos None para avisar a la siguiente cola que ya se acabo el texto
    cola_salida.put(None)


def quitar_espacios(cola_entrada, cola_salida):
    while True:
        linea = cola_entrada.get()
        if linea is None: 
            cola_salida.put(None) 
            break
        
        linea_limpia = linea.strip()
        cola_salida.put(linea_limpia)


def convertir_mayusculas(cola_entrada, cola_salida):
    while True:
        linea = cola_entrada.get()
        if linea is None:
            cola_salida.put(None)
            break
            
        linea_mayusculas = linea.upper()
        cola_salida.put(linea_mayusculas)


def escribir_archivo(ruta, cola_entrada):
    with open(ruta, 'w', encoding='utf-8') as f_out:
        while True:
            linea = cola_entrada.get()
            if linea is None:
                break 
            
            f_out.write(linea + '\n')


def procesar_con_pipeline(ruta_entrada, ruta_salida):
    # creacion de colas
    cola1 = queue.Queue()
    cola2 = queue.Queue()
    cola3 = queue.Queue()

    # creacion de hilos para cada tarea
    hilo_leer = threading.Thread(target=leer_archivo, args=(ruta_entrada, cola1))
    hilo_limpiar = threading.Thread(target=quitar_espacios, args=(cola1, cola2))
    hilo_mayus = threading.Thread(target=convertir_mayusculas, args=(cola2, cola3))
    hilo_escribir = threading.Thread(target=escribir_archivo, args=(ruta_salida, cola3))

    # inicio de los hilos antes creados
    hilo_leer.start()
    hilo_limpiar.start()
    hilo_mayus.start()
    hilo_escribir.start()

    # Espera de los hilos para que terminen 
    hilo_leer.join()
    hilo_limpiar.join()
    hilo_mayus.join()
    hilo_escribir.join()


if __name__ == '__main__':
    # Ubicacion del archivo de entrada y salida
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ruta_entrada = "texto_entrada.txt"
    ruta_salida = "texto_salida_pipeline.txt"

    inicio = time.time()
    procesar_con_pipeline(ruta_entrada, ruta_salida)
    fin = time.time()

    print(f"Tiempo total del pipeline: {fin - inicio:.2f} segundos")
    print(f"Archivo procesado guardado en {ruta_salida}")