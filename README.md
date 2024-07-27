# HandleCostAPI

HandleCostAPI es una API para la gestión de ingresos y egresos de usuarios. Proporciona endpoints para crear, actualizar y eliminar categorías, tipos de categoriaws e ítems (gastos/ingresos), así como para gestionar la autenticación de usuarios mediante tokens JWT.

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

**Las rutas necesitan de un Autorization con el token JWT asignado para funcionar, de forma que no cualquier puede hacer llamados a la api si no le corresponde el dato**

# Autenticación
**Iniciar sesión y obtener token de acceso**
URL: /token
Método: POST
Resumen: Iniciar sesión para obtener un token de acceso.
Cuerpo de la solicitud:

{
  "username": "string",
  "password": "string",
}
Respuestas:
200: Respuesta exitosa con el esquema Token.
422: Error de validación con el esquema HTTPValidationError.

# Tipos
**Crear tipo**
URL: /types/create_type
Método: POST
Resumen: Crear un nuevo tipo.
Cuerpo de la solicitud:

{
  "typeName": "string",
  "owner_id": 0,
  "active": true,
  "color": "string",
  "is_negative": true
}

Respuestas:
200: Tipo creado exitosamente.
422: Error de validación.

**Obtener tipos**
URL: /types/get_types/{owner_id}
Método: GET
Resumen: Obtener los tipos de un usuario.
Parametro: owner_id (Id de usuario)

Respuestas:
200: tipos obtenidos exitosamente.
422: Error de validación.

**Actualizar tipos**
URL: /types/update_type/{categorytype_id}
Método: PUT
Resumen: Actualizar un tipo en especifico.
Parametro: categorytype_id (Id de tipo)
Cuerpo de la solicitud:
{
  "typeName": "string",
  "color": "string",
  "active": true
}
Respuestas:
200: tipos obtenidos exitosamente.
422: Error de validación.


# Categorías
**Crear Categoría**
URL: /categories/create_category
Método: POST
Resumen: Crear una nueva categoría.
Cuerpo de la solicitud:
{
  "title": "string",
  "color": "string",
  "category_type": 0,
  "owner_id": 0
}

Respuestas:
200: Categoría creada exitosamente.
422: Error de validación.

**Obtener Categorías**
URL: /categories/get_categories/{owner_id}
Método: POST
Resumen: Crear una nueva categoría.
Parametro: owner_id (Id de usuario)

Respuestas:
200: Categorias obtenidas exitosamente.
422: Error de validación.


**Actualizar Categoría**
URL: /categories/update_category/{category_id}
Método: PUT
Resumen: Actualizar una categoría existente.
Parametro: category_id (Id de categoria)
Cuerpo de la solicitud:

{
  "title": "string",
  "category_type": 0,
  "color": "string",
  "active": true
}
Respuestas:
200: Categoría actualizada exitosamente.
422: Error de validación.




# Ítems
**Crear Ítem**
URL: /items/create_item
Método: POST
Resumen: Crear un nuevo ítem.
Cuerpo de la solicitud:

{
  "title": "string",
  "description": "string",
  "category": 0,
  "cost": 0,
  "createDate": "2024-07-27",
  "owner_id": 0
}

Respuestas:
200: Ítem creado exitosamente.
422: Error de validación.

**Actualizar Ítem**
URL: /items/update_item/{item_id}
Método: PUT
Resumen: Actualizar un ítem existente.
Parametro: item_id (Id de item)
Cuerpo de la solicitud:

{
  "title": "string",
  "description": "string",
  "category": 0,
  "cost": 0
}

Respuestas:
200: Ítem actualizado exitosamente.
422: Error de validación.

**Obtener Ítem**
URL: /items/get_items/{owner_id}
Método: PUT
Resumen: Actualizar un ítem existente.
Parametro: owner_id (Id de usuario)

Respuestas:
200: Ítems obtenidos exitosamente.
422: Error de validación.

**Eliminar Ítem**
URL: /items/delete_item/{item_id}
Método: PUT
Resumen: Actualizar un ítem existente.
Parametro: item_id (Id de item)

Respuestas:
200: Ítem eliminado exitosamente.
422: Error de validación.

