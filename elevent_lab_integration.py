import json

import whisper
from elevenlabs import generate, save

from chat import Chat
from prompt import BACKEND_REQ_TEMPLATE
from utils import save_json

model = whisper.load_model("base")
chat = Chat(system="You are the Meta-Mart Assistant and your name is 'Hayathi'. you will never ask any additional question")


def generate_json(message, chat_history):
    bot_message = chat.prompt_for_json(content=message)
    chat_history.append((message, bot_message))
    if bot_message == "Negative":
        return False, chat_history
    return bot_message, chat_history


def run_text_prompt(message, chat_history):
    bot_message = chat.prompt(content=message)

    # Specify the file path where you want to store the text
    file_path = "data/output.txt"

    # Open the file in write mode and write the transcription
    with open(file_path, "w") as file:
        file.write(bot_message)

    audio = generate(
        text=bot_message,
        voice="Bella"
    )
    output_path = "data/output.mp3"

    save(audio, output_path)

    # play(audio, notebook=True)

    chat_history.append((message, bot_message))
    return output_path, chat_history


def run_audio_prompt(audio, chat_history):
    if audio is None:
        return None, chat_history

    message_transcription = model.transcribe(audio)["text"]
    _, chat_history = run_text_prompt(message_transcription, chat_history)

    json_file, chat_history = generate_json(BACKEND_REQ_TEMPLATE.format(question=message_transcription), chat_history)
    save_json(json_file)
    return _, chat_history
