from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="streamingdevices-api", version="1.0")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)