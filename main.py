import uvicorn
from fastapi import FastAPI
from db.database import database, engine, metadata
from routes import routes_academy, routes_sync
from core.config import settings
from moodle.client import get_moodle_client
from moodle.routes_moodle import router as moodle_router

app = FastAPI(title="Plataforma API - FastAPI")

app.include_router(routes_academy.router)
app.include_router(routes_sync.router)
app.include_router(moodle_router)

@app.on_event("startup")
async def startup():
    await database.connect()
    app.state.moodle = get_moodle_client()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    mc = app.state.moodle
    if hasattr(mc, "close"):
        await mc.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.app_port, reload=True)
