from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from moviepy.editor import ImageSequenceClip
from typing import List
import os
import uuid

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to DreamMotion API!"}

@app.post("/create-video")
async def create_video(files: List[UploadFile] = File(...)):
    temp_folder = "temp_images"
    os.makedirs(temp_folder, exist_ok=True)

    file_paths = []
    for idx, file in enumerate(files):
        file_path = os.path.join(temp_folder, f"{idx}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_paths.append(file_path)

    # Crear el video con ImageSequenceClip
    clip = ImageSequenceClip(file_paths, fps=1)
    
    output_path = f"video_{uuid.uuid4().hex}.webm"  # Guardamos como .webm que no necesita ffmpeg extra
    clip.write_videofile(
        output_path,
        codec="libvpx",     # Codec compatible sin ffmpeg extra
        audio=False,
        verbose=False,
        logger=None
    )

    # Borrar las imágenes temporales
    for path in file_paths:
        os.remove(path)
    os.rmdir(temp_folder)

    # Devolver el archivo de video
    return FileResponse(output_path, media_type="video/webm", filename="video.webm")
