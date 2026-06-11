import os  # <-- ¡No olvides importar os para poder usar os.getenv!
from datetime import datetime, timedelta, timezone  # <-- Añadimos timezone
from typing import Optional
import jwt 
import bcrypt 
from dotenv import load_dotenv

# Cargamos las variables que escribiste en el archivo .env
load_dotenv()

# ==============================================================================
# LEER VARIABLES DESDE EL .env
# ==============================================================================
# os.getenv("NOMBRE", "VALOR_POR_DEFECTO") intenta leer del .env; si no lo encuentra, usa el defecto.
SECRET_KEY = os.getenv("SECRET_KEY", "clave_temporal_por_si_falla_el_env") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Como os.getenv siempre devuelve texto (str), lo convertimos a entero (int)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


def get_password_hash(password: str) -> str:
    """Toma una contraseña en texto plano (ej. '12345') y devuelve un hash string seguro"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara la contraseña que envía el usuario en el login con el hash de la base de datos"""
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Genera el token JWT que se enviará al frontend (React)"""
    to_encode = data.copy()
    
    # Usamos datetime.now(timezone.utc) que es la forma moderna y recomendada
    ahora_utc = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = ahora_utc + expires_delta
    else:
        expire = ahora_utc + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt