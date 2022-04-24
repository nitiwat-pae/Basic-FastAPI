from unicodedata import name
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix='/coffee',
    tags=['Coffee'],
    responses={404:{
        'msg':'Not found'
    }}
)

class Coffee(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    star: int


coffee_db = [
    {
        'name': 'Espresso',
        'description': 'กาแฟดำเข้มสุดๆ',
        'price': 60.5,
        'star': 5
    },
    {
        'name': 'Americano',
        'description': 'กาแฟดำ 1 ช็อตผสมน้ำร้อน',
        'price': 65,
        'star': 5
    }
]

# Works with POST -------------------------------------------------------------------------------------------------
@router.post('/addCoffee')
async def addCoffee(addCoffee: Coffee):
    new_coffee = coffee_db.append(addCoffee)
    print(new_coffee)
    return coffee_db[-1]
# Works with POST -------------------------------------------------------------------------------------------------

# Works with DELETE -------------------------------------------------------------------------------------------------
@router.delete('/coffee/{id}')
async def deleteCoffee(id: int):
    coffee = coffee_db[id-1]
    print(coffee['name'])
    coffee_db.pop(id-1)
    result = {'msg':f"{coffee['name']} was deleted !"}
    return result
# Works with DELETE -------------------------------------------------------------------------------------------------


# Works with PUT -------------------------------------------------------------------------------------------------
@router.put('/coffee/{id}')
async def updateCoffee(id: int, coffee: Coffee):
    coffee_db[id-1].update(coffee)
    result = {'msg': f"Coffee id {id} is updated !"}
    return result
# Works with PUT -------------------------------------------------------------------------------------------------

# Works with Database -------------------------------------------------------------------------------------------------
@router.get('/')
async def root():
    return coffee_db

# @router.get('/coffee/{id}')
# async def coffee_by_id(id: int):
#     if id == 0:
#         return 'The id must more than zero !'
#     coffee = coffee_db[id-1]
#     return coffee
# Works with Database -------------------------------------------------------------------------------------------------


# SAMPLE----------------------------------------------------------------------------------------------------------------
# @router.get('/')  # Create route
# async def root():
#     return {'msg': 'Hello FastAPI'}


# @router.get('/hello_fastapi')
# async def hello_fastapi():
#     return {'msg': 'FastAPI is awesome'}


# @router.get('/item/{item_id}')
# async def get_item(item_id: int):
#     print(item_id)
#     # return {'msg':'item is {}'.format(item_id)}
#     return {'msg': f'item is {item_id}'}
# SAMPLE----------------------------------------------------------------------------------------------------------------