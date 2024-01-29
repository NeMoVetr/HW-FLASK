from datetime import datetime

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, DateTime, MetaData

app = FastAPI()

DATABASE_URL = "sqlite:///./shop.bd"

engine = create_engine(DATABASE_URL)

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


metadata.create_all(engine)


@app.post("/users/", response_model=User)
async def create_user(user: User):
    print("user.model_dump():", user.model_dump())
    with engine.connect() as connection:
        query = users.insert().values(**user.model_dump())
        connection.execute(query)

        print("user:", user)
        return user


@app.get("/users/")
async def read_users(request: Request):
    with engine.connect() as connection:
        query = users.select()
        print(query)
        users_result = connection.execute(query).fetchall()
        print(f"Users fetched: {users_result}")
        user_table = pd.DataFrame(users_result,
                                  columns=["id", "first_name", "last_name", "email", "password"]).to_html()
        return HTMLResponse(content=templates.get_template("shop.html").render(request=request, user_table=user_table))


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    with engine.connect() as connection:
        query = users.select().where(users.c.id == user_id)
        user_result = connection.execute(query).fetchone()

        user_model_dump = User(**user_result.model_dump())
        return user_model_dump


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    with engine.connect() as connection:
        query = users.update().where(users.c.id == user_id).values(**user.model_dump())
        connection.execute(query)
        return user


@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    with engine.connect() as connection:
        query = users.delete().where(users.c.id == user_id)
        user_result = connection.execute(query).fetchone()
        user_model_dump = User(**user_result.model_dump())
        return user_model_dump


@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    with engine.connect() as connection:
        query = products.insert().values(**product.model_dump())
        result = connection.execute(query)
        product_id = result.inserted_primary_key[0]
        return {**product.model_dump(), "id": product_id}


@app.get("/products/")
def read_products(request: Request):
    with engine.connect() as connection:
        query = products.select()
        products_result = connection.execute(query).fetchall()
        product_table = pd.DataFrame(products_result, columns=["id", "name", "description", "price"]).to_html()
        return HTMLResponse(
            content=templates.get_template("shop.html").render(request=request, product_table=product_table))


@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int):
    with engine.connect() as connection:
        query = products.select().where(products.c.id == product_id)
        product_result = connection.execute(query).fetchone()

        product_model_dump = Product(**product_result.model_dump())
        return product_model_dump


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    with engine.connect() as connection:
        query = products.update().where(products.c.id == product_id).values(**product.model_dump())
        connection.execute(query)
        return product


@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    with engine.connect() as connection:
        query = products.delete().where(products.c.id == product_id)
        product_result = connection.execute(query).fetchone()
        product_model_dump = Product(**product_result.model_dump())
        return product_model_dump


@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    with engine.connect() as connection:
        query = orders.insert().values(**order.model_dump(), order_date=datetime.utcnow())
        result = connection.execute(query)
        order_id = result.inserted_primary_key[0]
        return {**order.model_dump(), "id": order_id, "order_date": datetime.utcnow()}


@app.get("/orders/")
def read_orders(request: Request):
    with engine.connect() as connection:
        query = orders.select()
        orders_result = connection.execute(query).fetchall()
        order_table = pd.DataFrame(orders_result,
                                   columns=["id", "user_id", "product_id", "order_date", "status"]).to_html()
        return HTMLResponse(
            content=templates.get_template("shop.html").render(request=request, order_table=order_table))


@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int):
    with engine.connect() as connection:
        query = orders.select().where(orders.c.id == order_id)
        order_result = connection.execute(query).fetchone()
        order_model_dump = Order(**order_result.model_dump())
        return order_model_dump


@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: Order):
    with engine.connect() as connection:
        query = orders.update().where(orders.c.id == order_id).values(**order.model_dump())
        connection.execute(query)
        return order


@app.delete("/orders/{order_id}", response_model=Order)
def delete_order(order_id: int):
    with engine.connect() as connection:
        query = orders.delete().where(orders.c.id == order_id)
        order_result = connection.execute(query).fetchone()
        order_model_dump = Order(**order_result.model_dump())
        return order_model_dump

