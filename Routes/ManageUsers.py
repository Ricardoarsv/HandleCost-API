from fastapi import APIRouter, HTTPException, Depends
from Models.user import User
from Models.item import Item
from Models.category import Category
from Models.type import Categorytype
from Controller.Users import UserCreate, get_password_hash
from Controller.Database import db_dependency
from Routes.ManageJWT import get_current_user, create_access_token
from sqlalchemy import extract, func
from datetime import datetime
import calendar

router = APIRouter()


@router.post("/users/create_user")
async def create_user(user: UserCreate, db: db_dependency):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email,
                   hashed_password=hashed_password,
                   is_active=True,
                   Language=user.Language)
    
    userByUsername = db.query(User).filter(User.username == db_user.username).first()
    userByEmail = db.query(User).filter(User.email == db_user.email).first()

    if userByUsername:
        raise HTTPException(status_code=400, detail="Username already exist")
    
    if userByEmail:
        raise HTTPException(status_code=401, detail="this email already exist")
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer", "user": db_user}



@router.get("/users/get_users")
async def get_users(db: db_dependency, current_user: User = Depends(get_current_user)):
    return db.query(User).all()


@router.put("/users/delete_user/{user_id}")
async def delete_user(user_id: int, db: db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    setattr(db_user, 'is_active', False)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/get_user_Statistics/{user_id}")
async def get_user_Statistics(user_id: int, db: db_dependency, current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's statistics")


    # Obtener la fecha actual y el primer y último día del mes actual
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    first_day_of_month = current_date.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0)
    _, last_day = calendar.monthrange(current_year, current_month)
    last_day_of_month = current_date.replace(
        day=last_day, hour=23, minute=59, second=59, microsecond=999999)

    # Inicializar variables
    itemsCategories = {}
    itemsCategories_current_month = {}
    itemsTypesAmount_current_month = {}
    itemsTypesAmount_all_time = {}
    itemsCategoryAmount_current_month = {}
    itemsCategoryAmount_all_time = {}

    # Inicializar totales
    totalAmountCategories_current_month = 0
    totalAmountTypes_current_month = 0
    totalAmountCategories_all_time = 0
    totalAmountTypes_all_time = 0

    # Procesar los ítems y calcular los totales
    items_with_categories = db.query(Item, Category, Categorytype).join(Category, Item.category == Category.id).join(
        Categorytype, Category.category_type == Categorytype.id).filter(Item.owner_id == user_id).all()

    for item, category, category_type in items_with_categories:
        # Procesar categorías
        if itemsCategories.get(category.id) is None:
            itemsCategories[category.id] = {
                "id": category.id,
                "title": category.title,
                "total": 1,
                "color": category.color
            }
        else:
            itemsCategories[category.id]["total"] += 1
            
        # Procesar categorías
        if itemsCategories_current_month.get(category.id) is None:
            itemsCategories_current_month[category.id] = {
                "id": category.id,
                "title": category.title,
                "total": 0,
                "color": category.color
            }
            
        # Procesar tipos para current_month
        if itemsTypesAmount_current_month.get(category_type.id) is None:
            itemsTypesAmount_current_month[category_type.id] = {
                "id": category_type.id,
                "title": category_type.typeName,
                "total": 0,
                "color": category_type.color
            }

        # Procesar tipos para all_time
        if itemsTypesAmount_all_time.get(category_type.id) is None:
            itemsTypesAmount_all_time[category_type.id] = {
                "id": category_type.id,
                "title": category_type.typeName,
                "total": 0,
                "color": category_type.color
            }

        # Procesar montos por categoría para current_month
        if itemsCategoryAmount_current_month.get(category.id) is None:
            itemsCategoryAmount_current_month[category.id] = {
                "id": category.id,
                "title": category.title,
                "total": 0,
                "color": category.color,
            }

        # Procesar montos por categoría para all_time
        if itemsCategoryAmount_all_time.get(category.id) is None:
            itemsCategoryAmount_all_time[category.id] = {
                "id": category.id,
                "title": category.title,
                "total": 0,
                "color": category.color,
            }

        # Actualizar totales para all_time
        totalAmountCategories_all_time += item.cost
        totalAmountTypes_all_time += item.cost

        # Actualizar totales para current_month si el ítem está en el mes actual
        if first_day_of_month <= item.createDate <= last_day_of_month:
            totalAmountCategories_current_month += item.cost
            totalAmountTypes_current_month += item.cost
            itemsTypesAmount_current_month[category_type.id]['total'] += item.cost
            itemsCategoryAmount_current_month[category.id]['total'] += item.cost
            itemsCategories_current_month[category.id]["total"] += 1
            
        # Actualizar totales en las estructuras de datos para all_time
        itemsTypesAmount_all_time[category_type.id]['total'] += item.cost
        itemsCategoryAmount_all_time[category.id]['total'] += item.cost

    user_Statistics = {
        "current_month": {
            "categories": itemsCategories_current_month,
            "types": itemsTypesAmount_current_month,
            "categoryAmount": itemsCategoryAmount_current_month
        },
        "all_time": {
            "categories": itemsCategories,
            "types": itemsTypesAmount_all_time,
            "categoryAmount": itemsCategoryAmount_all_time
        }
    }

    return {
        "current_month": {
            "categories": user_Statistics["current_month"]["categories"],
            "types": user_Statistics["current_month"]["types"],
            "categoryAmount": user_Statistics["current_month"]["categoryAmount"]
        },
        "all_time": {
            "categories": user_Statistics["all_time"]["categories"],
            "types": user_Statistics["all_time"]["types"],
            "categoryAmount": user_Statistics["all_time"]["categoryAmount"]
        }
    }

@router.get("/users/get_user_data/{user_id}")
async def get_user_data(user_id: int, db: db_dependency, current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if int(current_user.id) != int(user_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this user's statistics")

    items_with_categories = db.query(Item, Category, Categorytype).join(Category, Item.category == Category.id).join(
        Categorytype, Category.category_type == Categorytype.id).filter(Item.owner_id == user_id).all()

    if len(items_with_categories) == 0:
        raise HTTPException(
            status_code=400, detail="You dont have Items")

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    # Obtener el primer y el último día del mes actual
    first_day_of_month = current_date.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0)
    _, last_day = calendar.monthrange(current_year, current_month)
    last_day_of_month = current_date.replace(
        day=last_day, hour=23, minute=59, second=59, microsecond=999999)

    spents = 0
    totalAmount = 0
    monthlyTotalAmount = 0
    monthlySpents = 0
    categories = {}
    monthlyCategories = {}

    for item, category, category_type in items_with_categories:
        if categories.get(category.id) is None:
            categories[category.id] = {
                "title": category.title,
                "total": 1,
                "color": category.color
            }
        else:
            categories[category.id]["total"] += 1

        if first_day_of_month <= item.createDate <= last_day_of_month:
            if monthlyCategories.get(category.id) is None:
                monthlyCategories[category.id] = {
                    "title": category.title,
                    "total": 1,
                    "color": category.color
                }
            else:
                monthlyCategories[category.id]["total"] += 1

            if category_type.is_negative:
                monthlyTotalAmount -= item.cost
                monthlySpents += item.cost
            else:
                monthlyTotalAmount += item.cost

        if category_type.is_negative:
            totalAmount -= item.cost
            spents += item.cost
        else:
            totalAmount += item.cost

    # Obtener el valor máximo
    max_value = max(categories.values(), key=lambda x: x['total'])['total']
    max_categories = [value['title']
                      for value in categories.values() if value['total'] == max_value]
    result_string = ', '.join(max_categories)

    # Obtener el valor máximo mensual
    if monthlyCategories:
        max_monthly_value = max(
            monthlyCategories.values(), key=lambda x: x['total'])['total']
        max_monthly_categories = [value['title'] for value in monthlyCategories.values(
        ) if value['total'] == max_monthly_value]
        monthly_result_string = ', '.join(max_monthly_categories)
    else:
        monthly_result_string = ''

    # Calcular gastos del mes actual y del mes anterior
    current_month_spents = db.query(func.sum(Item.cost)).join(Category, Item.category == Category.id).join(Categorytype, Category.category_type == Categorytype.id).filter(
        Item.owner_id == user_id,
        extract('month', Item.createDate) == current_month,
        extract('year', Item.createDate) == current_year,
        Categorytype.is_negative == True
    ).scalar() or 0

    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    previous_month_spents = db.query(func.sum(Item.cost)).join(Category, Item.category == Category.id).join(Categorytype, Category.category_type == Categorytype.id).filter(
        Item.owner_id == user_id,
        extract('month', Item.createDate) == previous_month,
        extract('year', Item.createDate) == previous_year,
        Categorytype.is_negative == True
    ).scalar() or 0

    difference_between_months = current_month_spents - previous_month_spents

    
    user_data = {
        "user": db_user.id,
        "YearlyTotalAmount":totalAmount,
        "YearlySpents": spents,
        "YearlyMax_categories": result_string,
        "MonthlyDifferents": difference_between_months, 
        "MonthlyTotalAmount": monthlyTotalAmount, 
        "MonthlySpents": monthlySpents,
        "MonthlyMax_categories": monthly_result_string
    }
    return user_data
