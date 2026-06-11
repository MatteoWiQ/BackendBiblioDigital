from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, libros, users 
from database import engine
import models

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://front-biblio-digital-e986.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(libros.router, prefix="/api/libros", tags=["Libros"])
# Y cambiamos "usuarios.router" por "users.router" aquí:
app.include_router(users.router, prefix="/api/usuarios", tags=["Usuarios"])