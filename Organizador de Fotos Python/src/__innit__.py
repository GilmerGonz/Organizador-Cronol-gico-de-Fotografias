import io
import zipfile

def procesar_archivos_web(archivos_subidos):
    """
    Recibe una lista de archivos de Streamlit, los ordena por fecha 
    de última modificación y devuelve un buffer de memoria con un ZIP.
    """
    
    # 1. Creamos una lista de tuplas: (fecha_modificacion, objeto_archivo)
    # Streamlit guarda la fecha de modificación en el atributo 'last_modified'
    lista_con_fecha = []
    
    for arq in archivos_subidos:
        # Obtenemos la fecha (si no existe, usamos 0 como valor por defecto)
        fecha = getattr(arq, 'last_modified', 0)
        lista_con_fecha.append((fecha, arq))

    # 2. Ordenar la lista basándonos en la fecha (el primer elemento de la tupla)
    # Esto asegura que la foto más vieja sea la primera (1, 2, 3...)
    lista_con_fecha.sort(key=lambda x: x[0])

    # 3. Crear un archivo ZIP en la memoria RAM (no en el disco duro)
    buffer_zip = io.BytesIO()
    
    with zipfile.ZipFile(buffer_zip, "w") as zf:
        for indice, (fecha, arq) in enumerate(lista_con_fecha, start=1):
            # Extraer la extensión original (ej: .jpg o .png)
            extension = arq.name.split('.')[-1]
            
            # Generar el nuevo nombre enumerado
            nuevo_nombre = f"{indice}.{extension}"
            
            # Escribir el archivo dentro del ZIP con su nuevo nombre
            zf.writestr(nuevo_nombre, arq.getvalue())
    
    # Reposicionar el puntero del buffer al inicio para que pueda ser leído al descargar
    buffer_zip.seek(0)
    
    return buffer_zip