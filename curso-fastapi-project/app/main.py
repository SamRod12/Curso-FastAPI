from fastapi import FastAPI
from datetime import datetime
import zoneinfo
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

@app.get("/")
async def root():
    return {"message":"hola mundo"}

@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time" : datetime.now(tz)}
