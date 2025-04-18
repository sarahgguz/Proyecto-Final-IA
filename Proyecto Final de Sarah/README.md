# Horror Story Narrator with AI

This application uses deep learning models to generate horror stories based on user inputs and plays atmospheric horror music in the background to enhance the user experience. The app also features text-to-speech narration to bring the horror stories to life.

## Features

- Generate horror stories using the HuggingFace Zephyr-7B model
- Text-to-speech narration of the generated stories in multiple languages
- Atmospheric UI with horror-themed styling and flickering text effects
- Background horror music that plays during story generation
- Interactive Streamlit interface for easy user interaction
- Download generated stories as text files

## Prerequisites

- Python 3.8 or higher
- GPU recommended for faster story generation (but not required)

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/horror-story-narrator.git
cd horror-story-narrator
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Download sample horror music files:
```
python download_music.py
```

## Usage

1. Run the Streamlit application:
```
streamlit run app.py
```

2. Open the provided URL in your browser (typically http://localhost:8501)

3. Enter a topic for your horror story (e.g., "abandoned hospital", "haunted forest")

4. Click "Generate Horror Story" and enjoy your personalized horror experience!

5. Use the sidebar to customize narration settings:
   - Enable/disable voice narration
   - Select narration language (English, Spanish, French, German, Italian)
   - Toggle slow narration mode for added creepiness

6. Use the control buttons to:
   - Generate a new horror story
   - Stop the background music
   - Re-narrate the current story

7. Download your story using the "Download Story" button

## How It Works

This application leverages:

- **Hugging Face Transformers**: Uses the Zephyr-7B model for generating coherent and contextually relevant horror stories
- **PyTorch**: Powers the deep learning model for text generation
- **Streamlit**: Provides an interactive web interface
- **Pygame**: Handles the background music playback
- **gTTS (Google Text-to-Speech)**: Converts generated text to spoken word in multiple languages

## Customization

- Add your own horror music files to the `music` directory
- Adjust the `max_length` parameter in the `generate_horror_story` function to control story length
- Modify the CSS in the application to change the visual appearance
- Add additional languages to the narration options

## License

This project is available under the MIT License.

## Acknowledgments

- Free horror ambient sounds from [Freesound](https://freesound.org/)
- HuggingFace for providing access to state-of-the-art language models
- Google Text-to-Speech API for voice narration capabilities 