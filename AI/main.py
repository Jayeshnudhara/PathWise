from fastapi import FastAPI
from pydantic import BaseModel
from Recommendations import generate_roadmap

app = FastAPI()
class RoadmapRequest(BaseModel):
    career: str
    skill_gaps: list[str]

@app.get("/")
def home():
    return {"message": "PathWise backend is running!"}


@app.post("/roadmap")
def create_roadmap(data: RoadmapRequest):

    roadmap = generate_roadmap(
        data.career,
        data.skill_gaps
    )

    return {
        "roadmap": roadmap
    }