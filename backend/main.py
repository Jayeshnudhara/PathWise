from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "PathWise backend is running!"}