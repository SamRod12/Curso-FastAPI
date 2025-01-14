import zoneinfo
import time
from fastapi import FastAPI, Request
from datetime import datetime
from db import create_all_tables
from .routers import custormers, transactions, invoices, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(custormers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

country_timezones = {
    "CO" : "America/Bogota",
    "MX" : "America/Mexico_City",
    "AR" : "America/Argentina/Buenos_Aires",
    "BR" : "America/Sao_Paulo",
    "PE" : "America/Lima"
}
@app.middleware("http")
async def log_request_time(request:Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"request: {request.url} completed in {process_time:.4f}")
    return response

@app.middleware("http")
async def headears_requests(request:Request, call_next):
    response = await call_next(request)
    print(f"request: {request.url} headers in {request.headers}")
    return response

@app.get("/")
async def root():
    return {"message":"hola mundo"}

@app.get("/current_time/{iso_code}")
async def current_time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"current_time" : datetime.now(tz)}
