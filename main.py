from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Habilitar CORS para que frontend y backend puedan comunicarse sin errores
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las conexiones
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to DreamMotion API!"}

@app.post("/generate-video/")
async def generate_video(files: list[UploadFile] = File(...)):
    # Aquí iría la lógica real de generar el video
    # Por ahora devolvemos un mensaje de prueba
    return {"message": "Video creation simulated successfully!"}

# Solo si ejecutas localmente (no en Render)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
