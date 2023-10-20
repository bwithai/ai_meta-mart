# system
import shutil
import os
import time
from dotenv import load_dotenv

# bot
import openai
from elevenlabs import set_api_key
from chat import Chat
from elevent_lab_integration import run_audio_prompt, generate_json, run_text_prompt

# server
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from prompt import BACKEND_REQ_TEMPLATE
from utils import get_files, create_zip_archive, manage_memory, save_json

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
set_api_key(os.environ["ELEVENT_LAB_API"])
chat = Chat(system="You are a helpful assistant.")
chat_history = []

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-audio-file")
async def upload_audio_file(file: UploadFile = File(...), query: str = Form(...)):
    """
    - **param file**: Audio file to query from a model
    - **param query**: Query from a model in a txt **Note**: to skip query type "negative"
    - **return**: zip directory that contain json (product details), txt file (txt response from a model), mp3 output in voice
    """
    global chat_history
    if not file.read() and query == "":
        return {"message": "No upload file sent or query parameter is empty"}
        # file_name, extension = os.path.splitext(file.filename)

    if query == "negative":
        dist_path = os.path.join(os.getcwd(), 'data')
        manage_memory(dist_path)

        file_path = os.path.join(dist_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        output_path, chat_history = run_audio_prompt(file_path, chat_history)
        os.remove(file_path)
    else:
        json_file, chat_history = generate_json(BACKEND_REQ_TEMPLATE.format(question=query),
                                                chat_history)
        _, chat_history = run_text_prompt(query, chat_history)
        save_json(json_file)

    # Return multiple file as a response
    data_files = get_files()
    files_to_return = []
    for file in data_files:
        files_to_return.append(f"data/" + str(file))

    # Create a temporary zip archive containing multiple files
    zip_filename = "multiple_files.zip"
    create_zip_archive(files_to_return, zip_filename)

    # Return the zip archive as a response
    if os.path.exists(zip_filename):
        return FileResponse(zip_filename, headers={"Content-Disposition": f"attachment; filename={zip_filename}"})
    else:
        raise HTTPException(status_code=404, detail="Files not found")
