import streamlit as st
from src.procesador import procesar_archivos_web

# 1. Configuración de la Identidad Visual
st.set_page_config(
    page_title="Organizador Cronológico de Fotos",
    page_icon="📸",
    layout="centered"
)

# Estilo personalizado corregido
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #007BFF;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True) # <-- Cambio clave aquí

# 2. Encabezado de la Aplicación
st.title("📸 Organizador de Fotos")
st.subheader("Control Cronológico de Descargas")
st.write("""
    Sube tus fotos aquí. El sistema detectará el momento en que fueron descargadas 
    y las enumerará de la más antigua (**1**) a la más reciente.
""")

st.divider()

# 3. Zona de Carga de Archivos
fotos_subidas = st.file_uploader(
    "Arrastra tus imágenes aquí o haz clic para buscar", 
    type=['png', 'jpg', 'jpeg', 'webp', 'gif'], 
    accept_multiple_files=True
)

# 4. Lógica de Interacción
if fotos_subidas:
    cantidad = len(fotos_subidas)
    st.success(f"✅ Se han detectado {cantidad} archivos listos para procesar.")
    
    # Botón para iniciar el proceso
    if st.button("🚀 Generar Archivo Numerado"):
        with st.spinner("Ordenando archivos por fecha de descarga..."):
            try:
                # Llamamos a la función del procesador
                archivo_zip = procesar_archivos_web(fotos_subidas)
                
                st.balloons() # Animación de éxito
                st.info("¡Proceso completado con éxito!")
                
                # 5. Botón de Descarga del ZIP generado
                st.download_button(
                    label="⬇️ Descargar todas las fotos (.zip)",
                    data=archivo_zip,
                    file_name="fotos_cronologicas.zip",
                    mime="application/zip"
                )
            except Exception as e:
                st.error(f"Hubo un error al procesar las imágenes: {e}")

else:
    st.info("Esperando archivos... Por favor, sube las fotos que deseas enumerar.")

# 6. Pie de página
st.divider()
st.caption("Herramienta de organización interna para ITELC - Gestión de archivos secuenciales.")