
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Product Catalog")


@app.get("/health")
def health():
    return {"status": "running"}


products = {
    1: {"id": 1, "name": "Python Handbook", "price": 25.0, "category": "books"},
    2: {"id": 2, "name": "USB Keyboard", "price": 45.0, "category": "electronics"},
    3: {"id": 3, "name": "API Design Guide", "price": 35.0, "category": "books"},
}

customers = {}
next_customer_id = 1


@app.get("/products")
def list_products(category: str | None = None, max_price: float | None = None):
    result = []

    for product in products.values():
        if category is not None and product["category"] != category:
            continue
        if max_price is not None and product["price"] > max_price:
            continue
        result.append(product)

    return result


@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    return products[product_id]


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=80)


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    new_id = max(products, default=0) + 1
    new_product = {"id": new_id, **product.model_dump()}
    products[new_id] = new_product

    return new_product


@app.post("/customers", status_code=201)
def create_customer(customer: CustomerCreate):
    global next_customer_id

    new_customer = {
        "id": next_customer_id,
        **customer.model_dump()
    }

    customers[next_customer_id] = new_customer
    next_customer_id += 1

    return new_customer
