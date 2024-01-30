from datetime import datetime
from databases import Database
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, DateTime, MetaData

app = FastAPI()

DATABASE_URL = "sqlite:///./shop.bd"

database = Database(DATABASE_URL)


metadata = MetaData()

templates = Jinja2Templates(directory="templates")

users = Table("users",
              metadata,
              Column("id", Integer, primary_key=True),
              Column("first_name", String(50)),
              Column("last_name", String(50)),
              Column("email", String(120)),
              Column("password", String(50)),
              )

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("description", String(255)),
    Column("price", Integer),
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("date_ordered", DateTime, default=datetime.utcnow()),
    Column("status", String, default="Pending"),
)


class User(BaseModel):
    id: int
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=120)
    password: str = Field(max_length=50)


class Product(BaseModel):
    id: int
    name: str = Field(max_length=100)
    description: str = Field(max_length=255)
    price: float


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    date_ordered: datetime
    status: str


metadata.create_all(create_engine(DATABASE_URL))


@app.post("/users/", response_model=User)
async def create_user(user: User):
    query = users.insert().values(**user.dict())
    await database.execute(query)
    return user


@app.get("/users/")
async def read_users(request: Request):
    query = users.select()
    users_result = await database.fetch_all(query)
    user_table = pd.DataFrame(users_result, columns=["id", "first_name", "last_name", "email", "password"]).to_html()
    return templates.TemplateResponse("shop.html", {"request": request, "user_table": user_table})


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user_result = await database.fetch_one(query)
    user_model = User(**user_result)
    return user_model


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    query = users.update().where(users.c.id == user_id).values(**user.dict())
    await database.execute(query)
    return user


@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    user_result = await database.fetch_one(query)
    user_model = User(**user_result)
    return user_model


@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    query = products.insert().values(**product.dict())
    result = await database.execute(query)
    product_id = result
    return {**product.dict(), "id": product_id}


@app.get("/products/")
async def read_products(request: Request):
    query = products.select()
    products_result = await database.fetch_all(query)
    product_table = pd.DataFrame(products_result, columns=["id", "name", "description", "price"]).to_html()
    return templates.TemplateResponse("shop.html", {"request": request, "product_table": product_table})


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    product_result = await database.fetch_one(query)
    product_model = Product(**product_result)
    return product_model


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    query = products.update().where(products.c.id == product_id).values(**product.dict())
    await database.execute(query)
    return product


@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    product_result = await database.fetch_one(query)
    product_model = Product(**product_result)
    return product_model


@app.post("/orders/", response_model=Order)
async def create_order(order: Order):
    query = orders.insert().values(**order.model_dump())
    result = await database.execute(query)
    order_id = result
    return {**order.model_dump(), "id": order_id, "date_ordered": datetime.utcnow()}


@app.get("/orders/")
async def read_orders(request: Request):
    query = orders.select()
    orders_result = await database.fetch_all(query)
    order_table = pd.DataFrame(orders_result,
                               columns=["id", "user_id", "product_id", "date_ordered", "status"]).to_html()
    return templates.TemplateResponse("shop.html", {"request": request, "order_table": order_table})


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order_result = await database.fetch_one(query)
    order_model = Order(**order_result)
    return order_model


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: Order):
    query = orders.update().where(orders.c.id == order_id).values(**order.dict())
    await database.execute(query)
    return order


@app.delete("/orders/{order_id}", response_model=Order)
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    order_result = await database.fetch_one(query)
    order_model = Order(**order_result)
    return order_model


