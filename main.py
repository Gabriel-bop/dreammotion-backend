from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from moviepy.editor import ImageSequenceClip
import uvicorn
import os
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploaded_images"
VIDEO_OUTPUT = "output_video.mp4"

# Crear carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to DreamMotion API!"}

@app.post("/generate-video/")
async def generate_video(files: List[UploadFile] = File(...)):
    # Limpiar carpeta anterior
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    image_paths = []

    # Guardar todas las imágenes subidas
    for idx, file in enumerate(files):
        file_path = os.path.join(UPLOAD_FOLDER, f"{idx}.png")
        with open(file_path, "wb") as f:
            f.write(await file.read())
        image_paths.append(file_path)

    if not image_paths:
        return {"error": "No se subieron imágenes."}

    # Crear video usando moviepy
    clip = ImageSequenceClip(image_paths, fps=2)  # 2 frames por segundo
    clip.write_videofile(VIDEO_OUTPUT, codec="libx264", audio=False)

    return FileResponse(VIDEO_OUTPUT, media_type="video/mp4", filename="dreammotion_video.mp4")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
