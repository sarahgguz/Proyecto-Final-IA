import os
import subprocess
import sys

def check_dependencies():
    """Verificar si todas las dependencias requeridas están instaladas"""
    try:
        import streamlit
        import torch
        import transformers
        import pygame
        import gtts
        print("✅ Todas las dependencias requeridas están instaladas.")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("Instalando dependencias...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencias instaladas exitosamente.")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error al instalar dependencias. Por favor, ejecuta 'pip install -r requirements.txt' manualmente.")
            return False

def download_music():
    """Descargar archivos de música si no existen"""
    music_dir = "music"
    if not os.path.exists(music_dir) or not os.listdir(music_dir):
        print("Descargando archivos de música de terror...")
        try:
            subprocess.check_call([sys.executable, "download_music.py"])
            print("✅ Archivos de música descargados exitosamente.")
        except subprocess.CalledProcessError:
            print("⚠️ Error al descargar archivos de música. La aplicación seguirá funcionando pero sin música de fondo.")

def run_app():
    """Ejecutar la aplicación Streamlit"""
    print("Iniciando Narrador de Historias de Terror...")
    subprocess.call(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    print("🔥👻 Narrador de Historias de Terror con IA 👻🔥")
    print("=======================================")
    
    if check_dependencies():
        download_music()
        run_app()
    else:
        print("Por favor, soluciona los problemas de dependencias e inténtalo de nuevo.") 