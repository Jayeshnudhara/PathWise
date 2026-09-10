from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from AI.Recommendations import generate_roadmap
from backend.database import engine
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
class AssessmentRequest(BaseModel):
    career: str
    student_id: int


@app.post("/assessment")
def save_assessment(data: AssessmentRequest):

    with engine.connect() as connection:
        connection.execute(
            text(
                """
                INSERT INTO assessment_results (student_id, career)
                VALUES (:student_id, :career)
                """
            ),
            {
                "student_id": data.student_id,
                "career": data.career
            }
        )
        connection.commit()

    return {
        "message": "Assessment saved successfully!",
        "career": data.career,
        "student_id": data.student_id
    }
@app.get("/assessment/{student_id}")
def get_assessment(student_id: int):

    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT career
                FROM assessment_results
                WHERE student_id = :student_id
                ORDER BY created_at DESC
                LIMIT 1
                """
            ),
            {"student_id": student_id}
        ).fetchone()

    if result is None:
        return {
            "career": None
        }

    return {
        "career": result[0]
    }
class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/login")
def login(data: LoginRequest):

    with engine.connect() as connection:
        result = connection.execute(
            text(
                """
                SELECT student_id, name, email
                FROM students
                WHERE email = :email
                LIMIT 1
                """
            ),
            {"email": data.email}
        ).fetchone()

    if result is None:
        return {
            "success": False,
            "message": "Student not found"
        }

    return {
        "success": True,
        "student_id": result[0],
        "name": result[1],
        "email": result[2]
    }
class RegistrationRequest(BaseModel):
    name: str
    email: str


@app.post("/register")
def register(data: RegistrationRequest):

    with engine.connect() as connection:

        existing = connection.execute(
            text("""
                SELECT student_id
                FROM students
                WHERE email = :email
            """),
            {"email": data.email}
        ).fetchone()

        if existing:
            return {
                "success": False,
                "message": "Email already registered"
            }

        result = connection.execute(
            text("""
                INSERT INTO students (name, email)
                VALUES (:name, :email)
            """),
            {
                "name": data.name,
                "email": data.email
            }
        )

        connection.commit()

        return {
            "success": True,
            "message": "Registration successful",
            "student_id": result.lastrowid
        }
@app.get("/careers")
def get_careers():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT career_id, career_name, description
                FROM careers
            """)
        ).fetchall()

    return [
        {
            "career_id": row[0],
            "career_name": row[1],
            "description": row[2]
        }
        for row in result
    ]
@app.get("/students/{student_id}")
def get_student(student_id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT student_id, name, email
                FROM students
                WHERE student_id = :student_id
            """),
            {"student_id": student_id}
        ).fetchone()

    if result is None:
        return {
            "success": False,
            "message": "Student not found"
        }

    return {
        "success": True,
        "student_id": result[0],
        "name": result[1],
        "email": result[2]
    }
@app.get("/opportunities")
def get_opportunities():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    opportunity_id,
                    title,
                    company,
                    opportunity_type,
                    description,
                    required_skills,
                    location
                FROM opportunities
                ORDER BY created_at DESC
            """)
        ).fetchall()

    return [
        {
            "opportunity_id": row[0],
            "title": row[1],
            "company": row[2],
            "opportunity_type": row[3],
            "description": row[4],
            "required_skills": row[5],
            "location": row[6]
        }
        for row in result
    ]
@app.get("/opportunities/{opportunity_id}")
def get_opportunity(opportunity_id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    opportunity_id,
                    title,
                    company,
                    opportunity_type,
                    description,
                    required_skills,
                    location
                FROM opportunities
                WHERE opportunity_id = :opportunity_id
            """),
            {"opportunity_id": opportunity_id}
        ).fetchone()

    if result is None:
        return {
            "success": False,
            "message": "Opportunity not found"
        }

    return {
        "success": True,
        "opportunity_id": result[0],
        "title": result[1],
        "company": result[2],
        "opportunity_type": result[3],
        "description": result[4],
        "required_skills": result[5],
        "location": result[6]
    }