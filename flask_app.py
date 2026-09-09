from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


# ==============================
# DATABASE CONNECTION
# ==============================

def get_connection():
    connection = sqlite3.connect("students.db")
    connection.row_factory = sqlite3.Row
    return connection


# ==============================
# CREATE DATABASE TABLE
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

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to Student Management API using Flask"
    })


# ==============================
# GET ALL STUDENTS
# ==============================

@app.route("/students", methods=["GET"])
def get_students():

    connection = get_connection()

    students = connection.execute(
        "SELECT * FROM students"
    ).fetchall()

    connection.close()

    return jsonify([dict(student) for student in students])


# ==============================
# GET STUDENT BY ID
# ==============================

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):

    connection = get_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    connection.close()

    if student is None:
        return jsonify({
            "detail": "Student not found"
        }), 404

    return jsonify(dict(student))


# ==============================
# CREATE NEW STUDENT
# ==============================

@app.route("/students", methods=["POST"])
def create_student():

    data = request.get_json()

    required_fields = ["id", "name", "age", "course", "email"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "detail": f"{field} is required"
            }), 400

    connection = get_connection()

    existing_student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (data["id"],)
    ).fetchone()

    if existing_student:
        connection.close()

        return jsonify({
            "detail": "Student ID already exists"
        }), 400

    connection.execute("""
        INSERT INTO students (id, name, age, course, email)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["name"],
        data["age"],
        data["course"],
        data["email"]
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Student created successfully",
        "student": data
    }), 201


# ==============================
# UPDATE STUDENT
# ==============================

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):

    data = request.get_json()

    connection = get_connection()

    existing_student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if existing_student is None:
        connection.close()

        return jsonify({
            "detail": "Student not found"
        }), 404

    connection.execute("""
        UPDATE students
        SET id = ?, name = ?, age = ?, course = ?, email = ?
        WHERE id = ?
    """, (
        data["id"],
        data["name"],
        data["age"],
        data["course"],
        data["email"],
        student_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Student updated successfully",
        "student": data
    })


# ==============================
# DELETE STUDENT
# ==============================

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    connection = get_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        connection.close()

        return jsonify({
            "detail": "Student not found"
        }), 404

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Student deleted successfully",
        "student": dict(student)
    })


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":
    app.run(debug=True)