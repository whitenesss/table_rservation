from fastapi import FastAPI
from src.api.tables import router as table
from src.api.reservation import router as reservation








def create_app() -> FastAPI:

    app = FastAPI()

    app.include_router(table)
    app.include_router(reservation)
    return app


app = create_app()








if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)