from fastapi import FastAPI, HTTPException
import uvicorn
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [PRODUCT SERVICE] - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Product Service")

PRODUCTS = {
    123: {"id": 123, "name": "Laptop", "price": 4500.00},
    124: {"id": 124, "name": "Smartphone", "price": 2500.00}
}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    logger.info(f"Otrzymano zapytanie o produkt ID: {product_id}")
    
    if product_id in PRODUCTS:
        logger.info(f"Sukces: Znaleziono produkt ID: {product_id}")
        return PRODUCTS[product_id]
        
    logger.warning(f"Błąd 404: Produkt ID: {product_id} nie istnieje")
    raise HTTPException(status_code=404, detail="Product not found")

if __name__ == "__main__":
    logger.info("Uruchamianie Serwisu Produktów na porcie 8001...")
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="warning")