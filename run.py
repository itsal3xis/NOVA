import speech_recognition as sr
from gtts import gTTS
import os
import pygame

def speak(text, volume=0.5):
    """Convert text to speech and play it with adjustable volume using pygame."""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)

    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    os.remove("temp.mp3")

def listen_for_command():
    """Listen for commands, including the wake word 'VEXA'."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for the wake word 'VEXA'...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise
        audio = recognizer.listen(source)
        
    try:
        command = recognizer.recognize_google(audio)  # Google API speech recognition
        print(f"Recognized: {command}")
        return command.lower()  # Convert to lowercase for easy comparison
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        print("There was an issue with the speech recognition service.")
        return None

def main():
    """Main loop to listen for the wake word and respond to commands."""
    while True:
        command = listen_for_command()  # Listen for the wake word and commands
        if command:
            if 'hello' in command:  # Check for the wake word 'VEXA'
                speak("Hello, I am your assistant! How can I help you?")
                command = listen_for_command()  # Listen for the next command after the wake word

                if command:
                    if 'hello' in command:
                        speak("Hello, how can I assist you?")
                    elif 'stop' in command:
                        speak("Goodbye!")
                        break
                    else:
                        speak(f"You said: {command}")

if __name__ == "__main__":
    main()
