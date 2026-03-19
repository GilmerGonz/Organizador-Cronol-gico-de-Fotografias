import io
import zipfile

def procesar_archivos_web(archivos_subidos):
    """
    Esta función es el motor: recibe los archivos de la web, 
    los ordena por fecha de descarga y los mete en un ZIP.
    """
    
    # 1. Creamos una lista para guardar (fecha, archivo)
    lista_con_fecha = []
    
    for arq in archivos_subidos:
        # Extraemos la fecha de última modificación que reporta el navegador
        # Si no existe, usamos 0 para evitar errores
        fecha = getattr(arq, 'last_modified', 0)
        lista_con_fecha.append((fecha, arq))

    # 2. Ordenamos de la más vieja a la más nueva
    # x[0] se refiere a la fecha que guardamos en la tupla
    lista_con_fecha.sort(key=lambda x: x[0])

    # 3. Creamos el archivo comprimido en la memoria RAM
    buffer_zip = io.BytesIO()
    
    with zipfile.ZipFile(buffer_zip, "w") as zf:
        for indice, (fecha, arq) in enumerate(lista_con_fecha, start=1):
            # Obtenemos la extensión (jpg, png, etc.)
            extension = arq.name.split('.')[-1]
            
            # El nombre será el número del contador
            nuevo_nombre = f"{indice}.{extension}"
            
            # Agregamos el archivo al ZIP
            zf.writestr(nuevo_nombre, arq.getvalue())
    
    # Preparamos el archivo para que Streamlit lo pueda leer y descargar
    buffer_zip.seek(0)
    
    return buffer_zip