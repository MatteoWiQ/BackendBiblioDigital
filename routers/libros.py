from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt

# Importamos nuestros módulos externos
import models
import schemas
from database import get_db
from security import SECRET_KEY, ALGORITHM

router = APIRouter()


reusable_oauth2 = HTTPBearer()



def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(reusable_oauth2)):
    """
    Esta función agarra el token que manda React, lo descifra y nos dice 
    quién es el usuario y qué rol tiene. Si el token expiró o es falso, bloquea el paso.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        rol: str = payload.get("rol")
        
        if email is None or rol is None:
            raise HTTPException(status_code=401, detail="Token inválido")
            
        return {"email": email, "rol": rol}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


@router.get("/", response_model=list[schemas.BookResponse])
def listar_libros(db: Session = Depends(get_db)):
    libros = db.query(models.Book).all()
    return libros


@router.post("/", response_model=schemas.BookResponse, status_code=201)
def crear_libro(
    libro: schemas.BookCreate, 
    db: Session = Depends(get_db), 
    usuario_actual: dict = Depends(obtener_usuario_actual)
):

    if usuario_actual["rol"] != "Admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de Administrador para realizar esta acción")
    
    nuevo_libro = models.Book(
        titulo=libro.titulo,
        autor=libro.autor,
        descripcion=libro.descripcion,
        url_pdf=libro.url_pdf
    )
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro


@router.put("/{libro_id}", response_model=schemas.BookResponse)
def actualizar_libro(
    libro_id: int, 
    libro_actualizado: schemas.BookCreate, 
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):

    if usuario_actual["rol"] != "Admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de Administrador")
        
  
    libro_db = db.query(models.Book).filter(models.Book.id == libro_id).first()
    if not libro_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro_db.titulo = libro_actualizado.titulo
    libro_db.autor = libro_actualizado.autor
    libro_db.descripcion = libro_actualizado.descripcion
    libro_db.url_pdf = libro_actualizado.url_pdf
    
    db.commit()
    db.refresh(libro_db)
    return libro_db

@router.delete("/{libro_id}")
def eliminar_libro(
    libro_id: int, 
    db: Session = Depends(get_db),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):

    if usuario_actual["rol"] != "Admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de Administrador")
        
    libro_db = db.query(models.Book).filter(models.Book.id == libro_id).first()
    if not libro_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
        
    db.delete(libro_db)
    db.commit()
    return {"message": f"Libro con ID {libro_id} eliminado exitosamente"}