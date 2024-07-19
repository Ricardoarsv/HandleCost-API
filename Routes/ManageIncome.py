from fastapi import APIRouter

router = APIRouter()


@router.get("/Incomes/Test")
def read_root():
    return 'Hello from Incomes/Test'