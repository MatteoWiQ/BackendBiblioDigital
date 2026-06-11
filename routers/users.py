from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
import models
from routers.libros import obtener_usuario_actual
import schemas
from database import get_db
from security import SECRET_KEY, ALGORITHM
import security
router = APIRouter()


reusable_oauth2 = HTTPBearer()
@router.get("/", response_model=list[schemas.UserResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    if usuario_actual["rol"] != "Admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de Administrador")
        
    usuarios = db.query(models.User).all()
    return usuarios

@router.put("/{user_id}", response_model=schemas.UserResponse)
def actualizar_usuario(
    user_id: int, 
    usuario_actualizado: schemas.UserCreate,
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    if usuario_actual["rol"] != "Admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de Administrador")
        
    user_db = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 1. Actualizamos los datos comunes
    user_db.email = usuario_actualizado.email
    user_db.rol = usuario_actualizado.rol
    
    # 2. 🔥 ENCRIPTAR Y ACTUALIZAR LA CONTRASEÑA 🔥
    # Usamos la función de tu archivo security para generar el nuevo hash seguro
    user_db.hashed_password = security.get_password_hash(usuario_actualizado.password)
    
    # 3. Guardamos los cambios en la base de datos
    db.commit()
    db.refresh(user_db)
    return user_db

@router.delete("/{user_id}")
def eliminar_usuario(
    user_id: int, 
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    if usuario_actual["rol"] != "Admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de Administrador")
        
    user_db = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    db.delete(user_db)
    db.commit()
    return {"message": f"Usuario con ID {user_id} eliminado exitosamente"}

@router.post("/registro", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)

def registrar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):

    usuario_existente = db.query(models.User).filter(models.User.email == user.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    contrasena_encriptada = security.get_password_hash(user.password)
    

    nuevo_usuario = models.User(
        email=user.email,
        hashed_password=contrasena_encriptada,
        rol="Usuario" 
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario