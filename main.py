from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Student Management API",
    description="REST API built using FastAPI",
    version="1.0.0"
)


# ==============================
# Student Data Model
# ==============================

class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str
    email: str


# ==============================
# Temporary Student Data
# ==============================

students = [
    {
        "id": 1,
        "name": "Rahul",
        "age": 20,
        "course": "Data Science",
        "email": "rahul@gmail.com"
    },
    {
        "id": 2,
        "name": "Priya",
        "age": 21,
        "course": "Computer Science",
        "email": "priya@gmail.com"
    }
]


# ==============================
# HOME
# ==============================

@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management API"
    }


# ==============================
# GET ALL STUDENTS
# ==============================

@app.get("/students")
def get_students():
    return students


# ==============================
# GET STUDENT BY ID
# ==============================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# ==============================
# CREATE NEW STUDENT
# ==============================

@app.post("/students")
def create_student(student: Student):

    # Check if ID already exists
    for existing_student in students:
        if existing_student["id"] == student.id:
            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

    students.append(student.model_dump())

    return {
        "message": "Student created successfully",
        "student": student
    }


# ==============================
# UPDATE STUDENT
# ==============================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: Student
):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            students[index] = updated_student.model_dump()

            return {
                "message": "Student updated successfully",
                "student": updated_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# ==============================
# DELETE STUDENT
# ==============================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            deleted_student = students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student": deleted_student
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )