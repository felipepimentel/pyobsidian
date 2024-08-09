import os
import speech_recognition as sr
from pydub import AudioSegment
from ..obsidian_helper import load_config, write_to_file

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    audio.export("temp.wav", format="wav")

    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    os.remove("temp.wav")
    return text

def process_voice_notes(config):
    vault_path = config['obsidian']['vault_path']
    voice_notes_folder = os.path.join(vault_path, 'VoiceNotes')
    processed_folder = os.path.join(voice_notes_folder, 'Processed')
    os.makedirs(processed_folder, exist_ok=True)

    for file_name in os.listdir(voice_notes_folder):
        if file_name.endswith(('.mp3', '.wav', '.m4a')):
            audio_path = os.path.join(voice_notes_folder, file_name)
            text = convert_audio_to_text(audio_path)
            note_path = os.path.join(vault_path, f"{os.path.splitext(file_name)[0]}.md")
            write_to_file(note_path, text)
            os.rename(audio_path, os.path.join(processed_folder, file_name))
            print(f"Processed {file_name} into {note_path}")

if __name__ == "__main__":
    config = load_config()
    process_voice_notes(config)
    print("Voice notes processed successfully.")
