from fastapi import FastAPI
import uvicorn


app = FastAPI(title="UNICN SERVER")


@app.get("/")
async def health_check():
    return {"status": "Healthy"}


def init() -> None:
    uvicorn.run(app)


if __name__ == '__main__':
    init()
