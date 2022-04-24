from distutils.command.config import config
from fastapi import FastAPI
from routers import coffee
from tortoise.contrib.fastapi import register_tortoise
from models.todo import Todos, Todos_Pydantic, TodosIn_Pydantic

app = FastAPI()

@app.get('/')  # Create route
async def root():
    return {'msg': 'Hello FastAPI'}

def configRouter():
    app.include_router(coffee.router)

# configRouter()

@app.get('/todos')
async def show_todos():
    return await Todos_Pydantic.from_queryset(Todos.all())

@app.post('/todo')
async def create_todo(todo: TodosIn_Pydantic):
    todo_obj = await Todos.create(**todo.dict(exclude_unset=True))  
    return await TodosIn_Pydantic.from_tortoise_orm(todo_obj)

@app.put('/todo/{id}')
async def update_todo(id: int, todo: TodosIn_Pydantic):
    await Todos.filter(id=id).update(**todo.dict(exclude_unset=True))
    return await Todos_Pydantic.from_queryset_single(Todos.get(id=id))

@app.delete('/todo/{id}')
async def delete_todo(id: int):
    todo_count = await Todos.filter(id=id).delete()
    if todo_count is None:
        return {'msg':f"Todo {id} not found !"}
    return {'msg':f"Todo {id} was deleted successful !"}

register_tortoise(
    app,
    db_url='sqlite://db.sqlite2',
    modules={'models':['main']},
    generate_schemas=True,
    add_exception_handlers=True
)