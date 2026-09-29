from PIL import Image
import os
import time
from multiprocessing import Process, cpu_count

def convertir_a_gris(ruta_imagen):
    """Convierte una imagen a escala de grises."""
    try:
        imagen = Image.open(ruta_imagen)
        imagen_gris = imagen.convert('L')  # 'L' representa escala de grises
        nombre_archivo, extension = os.path.splitext(ruta_imagen)
        ruta_gris = nombre_archivo + "_gris" + extension
        imagen_gris.save(ruta_gris)
        print(f"Imagen convertida: {ruta_imagen} -> {ruta_gris}")
    except FileNotFoundError:
        print(f"Error: No se encontró la imagen {ruta_imagen}")
    except Exception as e:
        print(f"Error al procesar {ruta_imagen}: {e}")

# DESCOMPOSICION POR DOMINIO 
def procesar_bloque(sublista_imagenes):
    for ruta_imagen in sublista_imagenes:
        convertir_a_gris(ruta_imagen)

def procesar_imagenes_paralelo_dominio(lista_imagenes, num_procesos):
    """
    Divide el dominio (la lista total de imágenes)
    """
    if not lista_imagenes:
        print("La lista de imágenes esta vacia.")
        return

    #Calcular el tamaño de cada subdominio
    tamano_bloque = len(lista_imagenes) // num_procesos
    procesos = []

    print(f"Dividiendo {len(lista_imagenes)} imágenes entre {num_procesos} procesos...")

    # Se divide las listas en bloques y se asignan en cada proceso
    for i in range(num_procesos):
        inicio_idx = i * tamano_bloque
        
        # El ultimo proceso se queda con el sobrante de la división si no es exacta
        if i == num_procesos - 1:
            fin_idx = len(lista_imagenes)
        else:
            fin_idx = (i + 1) * tamano_bloque
        
        sublista = lista_imagenes[inicio_idx:fin_idx]
        
        # Crear un proceso asignándole su propio bloque de datos
        p = Process(target=procesar_bloque, args=(sublista,))
        procesos.append(p)

    # Iniciar todos los procesos
    for p in procesos:
        p.start()

    # Esperar a que todos los procesos terminen su trabajo
    for p in procesos:
        p.join()

if __name__ == '__main__':
    directorio_imagenes = "img"  

    # Verificar que la carpeta exista antes de leer
    if os.path.exists(directorio_imagenes):
        lista_imagenes = [
            os.path.join(directorio_imagenes, f) 
            for f in os.listdir(directorio_imagenes) 
            if os.path.isfile(os.path.join(directorio_imagenes, f))
        ]
        
        # Determinar cuántos núcleos de CPU tiene la máquina
        num_procesos = cpu_count()
        
        inicio = time.time()
        procesar_imagenes_paralelo_dominio(lista_imagenes, num_procesos)
        fin = time.time()
        
        print(f"\nTiempo total de procesamiento en paralelo: {fin - inicio:.2f} segundos")
    else:
        print(f"Error: La carpeta '{directorio_imagenes}' no existe.")