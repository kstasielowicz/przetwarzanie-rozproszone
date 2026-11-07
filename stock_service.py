from fastapi import FastAPI, HTTPException
import httpx
import uvicorn
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [STOCK SERVICE] - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock Service")

STOCKS = {
    123: {"productId": 123, "quantity": 15},
    124: {"productId": 124, "quantity": 8}
}

PRODUCT_SERVICE_URL = "http://127.0.0.1:8001/products"

@app.get("/stock/{product_id}")
async def get_stock(product_id: int):
    logger.info(f"Otrzymano zapytanie o stan magazynowy produktu ID: {product_id}")
    logger.info(f"Wysyłanie zapytania weryfikacyjnego do Product Service (ID: {product_id})...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PRODUCT_SERVICE_URL}/{product_id}")
        except Exception as e:
            logger.error(f"Błąd połączenia z Product Service: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error: Cannot reach Product Service")
            
    if response.status_code == 200:
        logger.info(f"Odpowiedź z Product Service: 200 OK. Produkt istnieje.")
        stock = STOCKS.get(product_id, {"productId": product_id, "quantity": 0})
        logger.info(f"Zwracanie stanu magazynowego: {stock}")
        return stock
        
    elif response.status_code == 404:
        logger.warning(f"Odpowiedź z Product Service: 404 Not Found. Produkt nie istnieje.")
        raise HTTPException(status_code=404, detail="Product not found")
        
    else:
        logger.error(f"Nieoczekiwany błąd z Product Service. Status: {response.status_code}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    logger.info("Uruchamianie Serwisu Magazynowego na porcie 8002...")
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="warning")