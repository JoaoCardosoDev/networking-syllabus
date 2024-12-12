from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class Product(BaseModel):
    id: int
    name: str
    price: float

# Temporary memory
products = []

app = FastAPI()

@app.get("/products")
def get_products():
    return products

@app.post("/products")
def create_products(product: Product):
    products.append(product)
    return {"message": "Product created", "product": product}

@app.put("/product/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index, prod in enumerate(products):
        if prod.id == product_id:
            products[index] = updated_product
            return {"message": "Product updated", "product": updated_product}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/product/{product_id}")
def delete_product(product_id: int):
    for index, prod in enumerate(products):
        if prod.id == product_id:
            products.pop(index)
            return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
