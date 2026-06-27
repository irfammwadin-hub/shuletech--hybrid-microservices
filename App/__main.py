from fastapi import FastAPI
from app.database_mysql import engine, Base
from app.routes import core_routes

# Tengeneza Tables za MySQL kama hazipo (Kwenye uanzishaji wa docker)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ShuleTech Distributed ERP",
    description="Hybrid Microservices Architecture for Zanzibar Academy",
    version="1.0.0"
)

# Unganisha zile routes tulizotengeneza
app.include_router(core_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to ShuleTech Distributed ERP System API"}