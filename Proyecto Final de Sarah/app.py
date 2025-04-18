import streamlit as st
import torch
from transformers import pipeline, set_seed
import pygame
import os
import time
import random
from pathlib import Path
from gtts import gTTS
import tempfile
import threading

# Set page config
st.set_page_config(
    page_title="Narrador de Historias de Terror",
    page_icon="👻",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #000000;
        color: #ff0000;
    }
    .stTextInput > div > div > input {
        background-color: #333333;
        color: #ffffff;
    }
    .stButton > button {
        background-color: #660000;
        color: white;
    }
    h1, h2, h3 {
        color: #ff0000;
    }
    .story-text {
        font-family: 'Georgia', serif;
        font-size: 20px;
        line-height: 1.6;
        margin: 20px 0;
        color: #ff0000;
        text-shadow: 2px 2px 4px #000000;
    }
    @keyframes flicker {
        0% {opacity: 0.8;}
        5% {opacity: 0.9;}
        10% {opacity: 0.8;}
        15% {opacity: 1;}
        20% {opacity: 0.8;}
        25% {opacity: 0.9;}
        30% {opacity: 0.8;}
        35% {opacity: 1;}
        40% {opacity: 0.9;}
        45% {opacity: 1;}
        50% {opacity: 0.8;}
        55% {opacity: 0.9;}
        60% {opacity: 1;}
        65% {opacity: 0.9;}
        70% {opacity: 0.8;}
        75% {opacity: 0.9;}
        80% {opacity: 1;}
        85% {opacity: 0.8;}
        90% {opacity: 0.9;}
        95% {opacity: 0.8;}
        100% {opacity: 1;}
    }
    .flicker-text {
        animation: flicker 5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Initialize pygame for sound
pygame.mixer.init()

# Create directories if they don't exist
os.makedirs("audio", exist_ok=True)
os.makedirs("music", exist_ok=True)

# Function to initialize and cache the text generation model
@st.cache_resource
def load_story_generator():
    generator = pipeline(
        "text-generation",
        model="HuggingFaceH4/zephyr-7b-beta",
        torch_dtype=torch.float16,
        device_map="auto",
    )
    return generator

# Function to play random horror music
def play_background_music(volume=0.3):
    # List of music files
    music_files = [
        "horror_ambience_1.mp3",
        "horror_ambience_2.mp3",
        "horror_ambience_3.mp3"
    ]
    
    # Check if we have music files, otherwise use placeholders
    existing_files = [file for file in music_files if os.path.exists(os.path.join("music", file))]
    
    if not existing_files:
        st.warning("No se encontraron archivos de música. Por favor, añade archivos MP3 al directorio 'music'.")
        return
    
    # Select a random music file
    music_file = os.path.join("music", random.choice(existing_files))
    
    # Play the music
    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(volume)  # Set volume
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    except Exception as e:
        st.error(f"Error al reproducir música: {e}")

# Function to stop the music
def stop_background_music():
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    except:
        pass

# Function to convert text to speech
def text_to_speech(text, slow=False):
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3', dir='audio')
        temp_file.close()
        
        # Generate speech always in Spanish
        tts = gTTS(text=text, lang='es', slow=slow)
        tts.save(temp_file.name)
        
        return temp_file.name
    except Exception as e:
        st.error(f"Error al generar voz: {e}")
        return None

# Function to play narration
def play_narration(audio_file):
    try:
        # Initialize a separate mixer channel for narration
        narration_channel = pygame.mixer.Channel(1)
        narration_sound = pygame.mixer.Sound(audio_file)
        
        # Lower background music volume during narration
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(0.1)
        
        # Play the narration
        narration_channel.play(narration_sound)
        
        # Wait for narration to finish
        while narration_channel.get_busy():
            pygame.time.wait(100)
        
        # Restore background music volume
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(0.3)
    except Exception as e:
        st.error(f"Error al reproducir narración: {e}")

# Function to generate horror story
def generate_horror_story(prompt, max_length=500):
    try:
        story_generator = load_story_generator()
        set_seed(random.randint(1, 10000))  # Random seed for variety
        
        # Add horror context to the prompt in Spanish
        horror_prompt = f"""
        Escribe una historia de terror escalofriante que le dará pesadillas al lector.
        
        Tema: {prompt}
        
        Hazla atmosférica, con suspenso y realmente aterradora. Incluye detalles sensoriales y construye la tensión gradualmente.
        Escribe la historia completamente en español.
        """
        
        # Generate the story
        story = story_generator(
            horror_prompt,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.9,
            top_p=0.92,
            top_k=50,
            repetition_penalty=1.2
        )
        
        # Clean up the generated text to find the actual story
        generated_text = story[0]['generated_text']
        
        # Try to find where the story actually starts after the prompt
        story_text = generated_text.split("Tema:")[1] if "Tema:" in generated_text else generated_text
        story_text = story_text.split(prompt)[1] if prompt in story_text else story_text
        
        # Further clean up, looking for where the actual story might start
        for marker in ["Hazla atmosférica", "historia de terror", "Escribe una"]:
            if marker in story_text:
                parts = story_text.split(marker)
                if len(parts) > 1:
                    story_text = parts[1]
        
        # Final cleaning to find the beginning of the actual story content
        for marker in [".", "\n\n"]:
            if marker in story_text:
                story_start = story_text.find(marker) + len(marker)
                if story_start < len(story_text):
                    story_text = story_text[story_start:].strip()
                    break
        
        return story_text.strip()
    except Exception as e:
        return f"Error al generar historia: {e}"

# Function to handle narration in a separate thread
def narrate_story_thread(story_text):
    # Split the story into paragraphs for better narration
    paragraphs = [p for p in story_text.split('\n\n') if p.strip()]
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Convert paragraph to speech
            audio_file = text_to_speech(paragraph)
            if audio_file:
                # Play the narration
                play_narration(audio_file)
                
                # Delete the temporary file after playing
                try:
                    os.remove(audio_file)
                except:
                    pass

# Main app
def main():
    st.markdown("<h1 class='flicker-text'>🔥 NARRADOR DE HISTORIAS DE TERROR 👻</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <p class='flicker-text'>Bienvenido a los rincones más oscuros de tu imaginación. 
    Introduce un tema y nuestra IA creará una historia terrorífica que atormentará tus sueños.</p>
    """, unsafe_allow_html=True)
    
    # Topic input
    story_topic = st.text_input("Introduce un tema para tu historia de terror:", 
                               placeholder="p.ej., hospital abandonado, bosque embrujado, visitante de medianoche...")
    
    # Sidebar options
    st.sidebar.title("Opciones del Narrador")
    enable_narration = st.sidebar.checkbox("Activar Narración por Voz", value=True)
    slow_narration = st.sidebar.checkbox("Narración Lenta", value=False)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔮 Generar Historia de Terror"):
            if not story_topic:
                st.error("Por favor, introduce un tema para tu historia de terror.")
            else:
                with st.spinner("Invocando fuerzas oscuras para crear tu pesadilla..."):
                    # Play background music
                    play_background_music()
                    
                    # Generate the story
                    story = generate_horror_story(story_topic)
                    
                    # Store the story in session state
                    st.session_state.story = story
                    st.session_state.story_generated = True
                    
                    # Start narration if enabled
                    if enable_narration and story:
                        st.session_state.narration_thread = threading.Thread(
                            target=narrate_story_thread, 
                            args=(story,)
                        )
                        st.session_state.narration_thread.daemon = True
                        st.session_state.narration_thread.start()
    
    with col2:
        if st.button("🔇 Detener Música"):
            stop_background_music()
    
    with col3:
        if st.button("🎙️ Narrar de Nuevo") and 'story_generated' in st.session_state:
            if enable_narration and st.session_state.story:
                # Ensure background music is playing
                if not pygame.mixer.music.get_busy():
                    play_background_music(volume=0.2)
                
                # Start narration thread
                narration_thread = threading.Thread(
                    target=narrate_story_thread, 
                    args=(st.session_state.story,)
                )
                narration_thread.daemon = True
                narration_thread.start()
    
    # Display the generated story
    if 'story_generated' in st.session_state and st.session_state.story_generated:
        st.markdown("<h2 class='flicker-text'>Tu Pesadilla Comienza...</h2>", unsafe_allow_html=True)
        
        # Display the story with styling
        story_container = st.empty()
        story_text = st.session_state.story
        
        # Display the full story with styling
        story_container.markdown(f'<div class="story-text">{story_text}</div>', unsafe_allow_html=True)
        
        # Add download button for the story
        st.download_button(
            label="📥 Descargar Historia",
            data=story_text,
            file_name=f"historia_terror_{story_topic.replace(' ', '_')}.txt",
            mime="text/plain"
        )

# Run the app
if __name__ == "__main__":
    main() 