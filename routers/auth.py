from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

# Importamos nuestros propios archivos
import models
import schemas
import security
from database import get_db

router = APIRouter()
# RUTA DE REGISTRO
@router.post("/registro", response_model=schemas.UserResponse)
def registrar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Verificamos si el correo ya existe en la base de datos
    usuario_existente = db.query(models.User).filter(models.User.email == user.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    # 2. Encriptamos la contraseña
    hashed_pwd = security.get_password_hash(user.password)
    
    # 3. Creamos el nuevo usuario con el modelo de SQLAlchemy
    nuevo_usuario = models.User(
        email=user.email,
        hashed_password=hashed_pwd,
        rol=user.rol # Recuerda que por defecto será "Usuario"
    )
    
    # 4. Lo guardamos en MySQL
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario) # Refrescamos para obtener el ID que le dio MySQL
    
    return nuevo_usuario

# RUTA DE LOGIN (Generación del JWT)

@router.post("/login", response_model=schemas.Token)
def iniciar_sesion(user_credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Buscamos al usuario por su correo
    usuario = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    # 2. Verificamos que el usuario exista y que la contraseña sea correcta
    if not usuario or not security.verify_password(user_credentials.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Si todo está bien, armamos los datos que irán dentro del Token (email y rol)
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # EMPAQUETAMOS EL ROL AQUÍ. Esto es vital para tu proyecto.
    token_data = {"sub": usuario.email, "rol": usuario.rol} 
    
    access_token = security.create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    
    # 4. Le entregamos el token a React
    return {"access_token": access_token, "token_type": "bearer"}
