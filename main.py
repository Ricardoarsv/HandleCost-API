import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from Routes.ManageUsers import router as manage_users_router
from Routes.ManageItems import router as manage_items_router
from Routes.ManageTypes import router as manage_types_router
from Routes.ManageCategories import router as manage_categories_router
from Routes.ManageJWT import router as manage_JWT_router
from Models.user import User
from Models.item import Item
from Models.category import Category
from Models.type import Categorytype
from Controller.Database import engine


app = FastAPI()

# Configura las orígenes permitidas
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



User.metadata.create_all(bind=engine)
Item.metadata.create_all(bind=engine)
Categorytype.metadata.create_all(bind=engine)
Category.metadata.create_all(bind=engine)

# Incluye el router en la aplicación
app.include_router(manage_users_router)
app.include_router(manage_items_router)
app.include_router(manage_types_router)
app.include_router(manage_categories_router)
app.include_router(manage_JWT_router)

@app.get("/Admin/Docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.96.211", port=8000)
