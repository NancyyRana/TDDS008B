from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(
    title="Student Management API",
    description="REST API built using FastAPI with SQLite Database",
    version="2.0.0"
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
# Database Connection
# ==============================

def get_connection():
    connection = sqlite3.connect("students.db")
    connection.row_factory = sqlite3.Row
    return connection


# ==============================
# Create Database Table
# ==============================

def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_table()


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

    connection = get_connection()

    students = connection.execute(
        "SELECT * FROM students"
    ).fetchall()

    connection.close()

    return [dict(student) for student in students]


# ==============================
# GET STUDENT BY ID
# ==============================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    connection = get_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    connection.close()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return dict(student)


# ==============================
# CREATE NEW STUDENT
# ==============================

@app.post("/students")
def create_student(student: Student):

    connection = get_connection()

    existing_student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student.id,)
    ).fetchone()

    if existing_student:
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Student ID already exists"
        )

    connection.execute("""
        INSERT INTO students (id, name, age, course, email)
        VALUES (?, ?, ?, ?, ?)
    """, (
        student.id,
        student.name,
        student.age,
        student.course,
        student.email
    ))

    connection.commit()
    connection.close()

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

    connection = get_connection()

    existing_student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if existing_student is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    connection.execute("""
        UPDATE students
        SET id = ?, name = ?, age = ?, course = ?, email = ?
        WHERE id = ?
    """, (
        updated_student.id,
        updated_student.name,
        updated_student.age,
        updated_student.course,
        updated_student.email,
        student_id
    ))

    connection.commit()
    connection.close()

    return {
        "message": "Student updated successfully",
        "student": updated_student
    }


# ==============================
# DELETE STUDENT
# ==============================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    connection = get_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Student deleted successfully",
        "student": dict(student)
    }