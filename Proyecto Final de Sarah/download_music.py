import os
import urllib.request
import ssl

# Crear un directorio para archivos de audio si no existe
os.makedirs("music", exist_ok=True)

# URLs para sonidos ambientales de terror gratuitos
# Estos son marcadores de posición - en una aplicación real, utilizarías URLs de fuentes legítimas
horror_music_urls = [
    ("https://freesound.org/data/previews/463/463074_4082826-lq.mp3", "horror_ambience_1.mp3"),
    ("https://freesound.org/data/previews/557/557398_10907800-lq.mp3", "horror_ambience_2.mp3"),
    ("https://freesound.org/data/previews/456/456674_5121236-lq.mp3", "horror_ambience_3.mp3"),
]

def download_music_files():
    """Descargar archivos de música de terror para la aplicación"""
    print("Descargando archivos de música de terror...")
    
    # Crear contexto SSL para manejar la verificación de certificados SSL
    context = ssl._create_unverified_context()
    
    for url, filename in horror_music_urls:
        target_path = os.path.join("music", filename)
        
        # Omitir si el archivo ya existe
        if os.path.exists(target_path):
            print(f"El archivo {filename} ya existe. Omitiendo descarga.")
            continue
        
        try:
            print(f"Descargando {filename}...")
            urllib.request.urlretrieve(url, target_path)
            print(f"Descarga exitosa de {filename}")
        except Exception as e:
            print(f"Error al descargar {filename}: {e}")
    
    print("¡Descarga de música completada!")

if __name__ == "__main__":
    download_music_files() 