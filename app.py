from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, Field
from base64 import b64encode, b64decode
import jwt
import os
from datetime import datetime, timedelta

# Crear instancia de FastAPI
app = FastAPI(
    title="Security Toolbox API",
    description="API para encoding y decoding en Base64 y generación/validación de JWT.",
    version="1.0.0"
)

# Clave secreta para JWT
SECRET_KEY = os.getenv("SECRET_KEY")


# Modelo para JWT
class JWTData(BaseModel):
    payload: dict = Field(..., example={"user_id": 1})
    expiration_minutes: int = Field(..., example=10)


@app.get("/ping",
    summary="Ping al servidor",
    description="Responde con 'pong' para verificar si el servidor está activo.",
)
async def ping():
    """Responde "pong" al usuario."""
    return "pong"


@app.get("/encode_base64",
    summary="Codificar texto a Base64",
    description="Codifica el texto proporcionado en formato Base64.",
    responses={
        200: {
            "description": "Texto codificado en Base64",
            "content": {
                "application/json": {
                    "example": {
                        "encoded_text": "aG9sYQ=="
                    }
                }
            }
        }
    },
)
async def encode_base64(
    text: str = Query(..., description="Texto a encodear en Base64", example="hola"),
):
    """Codifica el texto en base64."""
    encoded = b64encode(text.encode()).decode()
    return {
        "encoded_text": encoded,
    }

@app.get("/decode_base64",
    summary="Decodificar texto en Base64",
    description="Decodifica el texto proporcionado codificado en Base64.",
    responses={
        200: {
            "description": "Texto decodificado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "decoded_text": "hola"
                    }
                }
            }
        },
        400: {
            "description": "Texto Base64 no válido",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid base64 encoded text"
                    }
                }
            }
        }
    },
)
async def decode_base64(encoded_text: str = Query(..., description="Texto codificado en Base64 para decodificar", example="aG9sYQ==")):
    """Intenta decodificar el texto en base64."""
    try:
        decoded = b64decode(encoded_text).decode()

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid base64 encoded text")
    
    return {
        "decoded_text": decoded,
    }


@app.post("/jwt/generate",
    summary="Generar token JWT",
    description="Genera un JWT con un payload y un tiempo de expiración especificado.",
    responses={
        200: {
            "description": "Token JWT generado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzEyNjAzNjZ9.Kk4pp8yNErLgfBrojOq0IltRInSqUlAV2bUe0T3rzQc"
                    }
                }
            }
        },
        400: {
            "description": "Error en la solicitud",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error al generar el token JWT"
                    }
                }
            }
        }
    }
)
async def generate_jwt(data: JWTData):
    """Genera un token JWT con un payload y tiempo de expiración especificado."""
    expiration = datetime.utcnow() + timedelta(minutes=data.expiration_minutes)
    payload = {**data.payload, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {
        "jwt_token": token,
    }


@app.get("/jwt/validate",
    summary="Validar token JWT",
    description="Valida el token JWT proporcionado.",
    responses={
        200: {
            "description": "Token JWT válido",
            "content": {
                "application/json": {
                    "example": {
                        "valid": True,
                        "payload": {"user_id": 1, "exp": 1691224106}
                    }
                }
            }
        },
        400: {
            "description": "Token no válido o expirado",
            "content": {
                "application/json": {
                    "examples": {
                        "expired_token": {
                            "summary": "Token expirado",
                            "value": {
                                "detail": "Token has expired"
                            }
                        },
                        "invalid_token": {
                            "summary": "Token no válido",
                            "value": {
                                "detail": "Invalid token"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def validate_jwt(token: str):
    """Valida un token JWT."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    return {
        "valid": True,
        "payload": decoded,
    }
