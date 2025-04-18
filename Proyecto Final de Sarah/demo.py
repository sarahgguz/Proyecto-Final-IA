import os
import time
import torch
from transformers import pipeline, set_seed
import random
from gtts import gTTS
import pygame
import tempfile

def print_with_delay(text, delay=0.03):
    """Imprime texto con efecto de máquina de escribir"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def setup():
    """Configura directorios necesarios y pygame"""
    os.makedirs("audio", exist_ok=True)
    os.makedirs("music", exist_ok=True)
    
    # Initialize pygame for audio
    pygame.mixer.init()
    pygame.init()

def play_music(music_file):
    """Reproduce música de fondo"""
    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # Loop indefinitely
        print("🎵 Reproduciendo música de fondo...")
    except Exception as e:
        print(f"⚠️ Error al reproducir música: {e}")

def text_to_speech(text, slow=False):
    """Convierte texto a voz y devuelve el nombre del archivo"""
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3', dir='audio')
        temp_file.close()
        
        tts = gTTS(text=text, lang='es', slow=slow)
        tts.save(temp_file.name)
        
        return temp_file.name
    except Exception as e:
        print(f"⚠️ Error al generar voz: {e}")
        return None

def play_narration(audio_file):
    """Reproduce narración de audio"""
    try:
        sound = pygame.mixer.Sound(audio_file)
        
        # Lower background music volume
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(0.1)
            
        # Play narration
        channel = pygame.mixer.Channel(1)
        channel.play(sound)
        
        # Wait for narration to finish
        while channel.get_busy():
            pygame.time.wait(100)
            
        # Restore music volume
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(0.3)
            
    except Exception as e:
        print(f"⚠️ Error al reproducir narración: {e}")

def load_story_generator():
    """Carga el modelo de generación de texto"""
    print("🤖 Cargando generador de historias con IA (esto puede tardar un momento)...")
    
    generator = pipeline(
        "text-generation",
        model="HuggingFaceH4/zephyr-7b-beta",
        torch_dtype=torch.float16,
        device_map="auto",
    )
    
    return generator

def generate_horror_story(prompt, generator, max_length=500):
    """Genera una historia de terror basada en el tema proporcionado"""
    print(f"📝 Generando historia de terror sobre: '{prompt}'")
    
    set_seed(random.randint(1, 10000))
    
    # Create the horror prompt
    horror_prompt = f"""
    Escribe una historia de terror escalofriante que le dará pesadillas al lector.
    
    Tema: {prompt}
    
    Hazla atmosférica, con suspenso y realmente aterradora. Incluye detalles sensoriales y construye la tensión gradualmente.
    Escribe la historia completamente en español.
    """
    
    # Generate the story
    story = generator(
        horror_prompt,
        max_length=max_length,
        num_return_sequences=1,
        temperature=0.9,
        top_p=0.92,
        top_k=50,
        repetition_penalty=1.2
    )
    
    # Extract and clean up the generated text
    generated_text = story[0]['generated_text']
    
    # Try to find where the story actually starts after the prompt
    story_text = generated_text.split("Tema:")[1] if "Tema:" in generated_text else generated_text
    story_text = story_text.split(prompt)[1] if prompt in story_text else story_text
    
    # Further clean up to find the beginning of the actual story
    for marker in ["Hazla atmosférica", "historia de terror", "Escribe una"]:
        if marker in story_text:
            parts = story_text.split(marker)
            if len(parts) > 1:
                story_text = parts[1]
    
    # Final cleaning
    for marker in [".", "\n\n"]:
        if marker in story_text:
            story_start = story_text.find(marker) + len(marker)
            if story_start < len(story_text):
                story_text = story_text[story_start:].strip()
                break
    
    return story_text.strip()

def narrate_story(story_text, slow=False):
    """Narra el texto de la historia"""
    print("\n🎙️ Iniciando narración...\n")
    
    # Split the story into paragraphs
    paragraphs = [p for p in story_text.split('\n\n') if p.strip()]
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Display the paragraph with typewriter effect
            print_with_delay(paragraph)
            print()
            
            # Convert to speech and play
            audio_file = text_to_speech(paragraph, slow)
            if audio_file:
                play_narration(audio_file)
                
                # Clean up the temporary file
                try:
                    os.remove(audio_file)
                except:
                    pass

def main():
    """Función principal de demostración"""
    # ASCII art title
    title = """
    ╔═══════════════════════════════════════════════════╗
    ║   🔥👻  NARRADOR DE HISTORIAS DE TERROR  👻🔥   ║
    ╚═══════════════════════════════════════════════════╝
    """
    print(title)
    
    # Setup
    setup()
    
    # Check for music files
    music_files = [f for f in os.listdir("music") if f.endswith(".mp3")]
    if music_files:
        music_file = os.path.join("music", random.choice(music_files))
        play_music(music_file)
    else:
        print("⚠️ No se encontraron archivos de música. Ejecuta download_music.py primero para obtener música de fondo.")
    
    # Default topic if none provided
    topics = ["manicomio abandonado", "bosque embrujado", "llamada misteriosa", 
              "puerta del sótano", "monstruo de la infancia", "visitante de medianoche"]
    topic = random.choice(topics)
    
    # Ask for user input
    print("\n¡Bienvenido al Narrador de Historias de Terror!")
    print("Esta demostración generará y narrará una historia de terror para ti.")
    user_topic = input(f"\nIntroduce un tema para tu historia de terror (o presiona Enter para '{topic}'): ")
    
    if user_topic.strip():
        topic = user_topic.strip()
    
    # Load model
    generator = load_story_generator()
    
    # Generate story
    print("\n" + "="*50)
    story = generate_horror_story(topic, generator)
    
    # Display the story title
    print("\n" + "="*50)
    print(f"👁️  TU PESADILLA: {topic.upper()} 👁️")
    print("="*50 + "\n")
    
    # Narrate the story
    narrate_story(story)
    
    # Clean up
    print("\n" + "="*50)
    print("¡Gracias por experimentar el Narrador de Historias de Terror!")
    print("Aplicación completa disponible con 'streamlit run app.py'")
    
    # Keep playing music until user exits
    print("\nPresiona Ctrl+C para salir...\n")
    try:
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSaliendo del Narrador de Historias de Terror. Que duermas bien... si puedes.") 