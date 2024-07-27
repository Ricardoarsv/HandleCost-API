# HandleCostAPI

HandleCostAPI es una API para la gestión de categorías, ítems y autenticación de usuarios. Proporciona endpoints para crear, actualizar y eliminar categorías e ítems, así como para gestionar la autenticación de usuarios mediante tokens.

## Inicialización de la API

### Prerrequisitos

Asegúrate de tener Python 3.10+ instalado.

1. **Crear entorno virtual**
```
bash
python -m venv App
```

2. **Activar entorno virtual**
```
bash
./App/Scripts/Activate
```

3. **Instalar dependencias**
```
bash
pip install -r requeriments.txt
```

4. **Iniciar el servidor con UVICORN**
```
bash
uvicorn main:app --reload
```

## Endpoints

# Autenticación
**Iniciar sesión y obtener token de acceso**
URL: /token
Método: POST
Resumen: Iniciar sesión para obtener un token de acceso.
Cuerpo de la solicitud:

{
  "grant_type": "password",
  "username": "string",
  "password": "string",
  "scope": "string",
  "client_id": "string",
  "client_secret": "string"
}
Respuestas:
200: Respuesta exitosa con el esquema Token.
422: Error de validación con el esquema HTTPValidationError.

# Categorías
**Crear Categoría**
URL: /categories
Método: POST
Resumen: Crear una nueva categoría.
Cuerpo de la solicitud:

{
  "title": "string",
  "color": "string",
  "category_type": 1,
  "owner_id": 1
}
Respuestas:
200: Categoría creada exitosamente.
422: Error de validación.

**Actualizar Categoría**
URL: /categories/{id}
Método: PUT
Resumen: Actualizar una categoría existente.
Cuerpo de la solicitud:

{
  "title": "string",
  "color": "string",
  "category_type": 1,
  "active": true
}
Respuestas:
200: Categoría actualizada exitosamente.
422: Error de validación.

# Ítems
**Crear Ítem**
URL: /items
Método: POST
Resumen: Crear un nuevo ítem.
Cuerpo de la solicitud:

{
  "title": "string",
  "description": "string",
  "category": 1,
  "cost": 100.0,
  "createDate": "YYYY-MM-DD",
  "owner_id": 1
}
Respuestas:
200: Ítem creado exitosamente.
422: Error de validación.

**Actualizar Ítem**
URL: /items/{id}
Método: PUT
Resumen: Actualizar un ítem existente.
Cuerpo de la solicitud:

{
  "title": "string",
  "description": "string",
  "category": 1,
  "cost": 100.0
}
Respuestas:
200: Ítem actualizado exitosamente.
422: Error de validación.
Esquemas
Token

{
  "access_token": "string",
  "token_type": "string",
  "user": "integer"
}
HTTPValidationError

{
  "detail": [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
CategoryCreate

{
  "title": "string",
  "color": "string",
  "category_type": 1,
  "owner_id": 1
}
CategoryUpdate

{
  "title": "string",
  "color": "string",
  "category_type": 1,
  "active": true
}
ItemCreate

{
  "title": "string",
  "description": "string",
  "category": 1,
  "cost": 100.0,
  "createDate": "YYYY-MM-DD",
  "owner_id": 1
}
ItemUpdate

{
  "title": "string",
  "description": "string",
  "category": 1,
  "cost": 100.0
}
Seguridad
OAuth2PasswordBearer

{
  "type": "oauth2",
  "flows": {
    "password": {
      "tokenUrl": "token",
      "scopes": {}
    }
  }
}
