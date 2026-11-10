from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello(name: str | None = None):
    return {"message": f"Hello {name or 'World'}!"}
