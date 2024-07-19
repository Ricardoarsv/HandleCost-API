import uvicorn
from fastapi import FastAPI
from Routes.ManageIncome import router as manage_income_router
from Routes.ManageUsers import router as manage_users_router
from Models.user import User
from Models.item import Item
from Controller.Database import engine

app = FastAPI()


User.metadata.create_all(bind=engine)
Item.metadata.create_all(bind=engine)

# Incluye el router en la aplicación
app.include_router(manage_income_router)
app.include_router(manage_users_router)

    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
