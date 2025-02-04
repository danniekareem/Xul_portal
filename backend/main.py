import pymssql
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
import crud 
from schemas import UserCreate, ClassCreate,SubjectCreate,TeacherCreate, StudentCreate, ResultCreate, ResultUpdate, StudentLoginRequest
from collections import defaultdict


# Create FastAPI instance
app = FastAPI()


# Allow CORS for the frontend
origins = [
    "http://localhost:3000",  # Allows requests from localhost
    "http://localhost:8080",  # React/Vue/Other local dev servers
    "http://127.0.0.1:8000",  # Localhost
    "http://127.0.0.1:3000",
    "http://localhost",  
    "http://127.0.0.1",
    # Add other allowed origins if needed...
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)




# 🔹 Endpoint for student login
@app.post("/student-login/")
def student_login(request: StudentLoginRequest, conn=Depends(get_db)):
    return crud.student_login(conn, request.studentID, request.dob)


# POST endpoint to create a user
@app.post("/users/")
def create_new_user(user: UserCreate, conn: pymssql.Connection = Depends(get_db)):
    return crud.create_user(conn=conn, user=user)


# GET endpoint to get a user by ID
@app.get("/users/{user_id}")
def get_active_user(user_id: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.get_user(conn=conn, user_id=user_id)
    
# GET endpoint to get all users
@app.get("/users")
def get_active_users(conn: pymssql.Connection = Depends(get_db)):
    return crud.get_all_users(conn=conn)


# PUT endpoint to update a user by ID
@app.put("/users/{user_id}")
def update_existing_user(user_id: int, user: UserCreate, conn: pymssql.Connection = Depends(get_db)):
    return crud.update_user(conn=conn, user_id=user_id, user=user)


#DELETE a user by ID endpoint 
@app.delete("/users/{user_id}")
def deactivate_user(user_id: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.delete_user(conn=conn, user_id=user_id)



#######################################################
# CLASSES ENDPOINTS
######################################################


# Create a new class
@app.post("/classes")
def add_class(class_data: ClassCreate, conn: pymssql.Connection = Depends(get_db)):
    return crud.create_class(conn, class_data)


# Get all active classes
@app.get("/classes")
def fetch_classes(conn: pymssql.Connection = Depends(get_db)):
    return crud.get_all_classes(conn)


# Get a single active class by ID
@app.get("/classes/{class_id}")
def fetch_class(class_id: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.get_class(conn, class_id)


# Delete (deactivate) a class by ID
@app.delete("/classes/{class_id}")
def remove_class(class_id: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.delete_class(conn, class_id)


# Update an existing class
@app.put("/classes/{class_id}")
def modify_class(class_id: int, new_class: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.update_class(conn, class_id, new_class)




#######################################################
# SUBJECTS ENDPOINTS
######################################################

# Create a new subject
@app.post("/subjects")
def add_subject(subject_data: SubjectCreate, conn: pymssql.Connection = Depends(get_db)):
    return crud.create_subject(conn, subject_data)

# Get all active subjects
@app.get("/subjects")
def fetch_subjects(conn: pymssql.Connection = Depends(get_db)):
    return crud.get_all_subjects(conn)

# Get a single active subject by ID
@app.get("/subjects/{subject_id}")
def fetch_subject(subject_id: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.get_subject(conn, subject_id)

# Update an existing subject
@app.put("/subjects/{subject_id}")
def modify_subject(subject_id: int, new_subject_name: str, conn: pymssql.Connection = Depends(get_db)):
    return crud.update_subject(conn, subject_id, new_subject_name)

# Delete (deactivate) a subject by ID
@app.delete("/subjects/{subject_id}")
def remove_subject(subject_id: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.delete_subject(conn, subject_id)



#######################################################
# teachers ENDPOINTS
######################################################



# Create a new teacher
@app.post("/teachers")
def add_teacher(teacher_data: TeacherCreate, conn: pymssql.Connection = Depends(get_db)):
    return crud.create_teacher(conn, teacher_data)

# Get all active teachers
@app.get("/teachers")
def fetch_teachers(conn: pymssql.Connection = Depends(get_db)):
    return crud.get_all_teachers(conn)

# Get a single active teacher by ID
@app.get("/teachers/{teacher_id}")
def fetch_teacher(teacher_id: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.get_teacher(conn, teacher_id)

# Update an existing teacher
@app.put("/teachers/{teacher_id}")
def modify_teacher(teacher_id: int, teacher_data: TeacherCreate, conn: pymssql.Connection = Depends(get_db)):
    return crud.update_teacher(conn, teacher_id, teacher_data)

# Delete (deactivate) a teacher by ID
@app.delete("/teachers/{teacher_id}")
def remove_teacher(teacher_id: int, conn: pymssql.Connection = Depends(get_db)):
    return crud.delete_teacher(conn, teacher_id)



#######################################################
# teachers ENDPOINTS
######################################################

# Create Student
@app.post("/students")
def create_student_endpoint(student: StudentCreate, conn=Depends(get_db)):
    return crud.create_student(conn, student)

# Get All Active Students
@app.get("/students")
def get_all_students_endpoint(conn=Depends(get_db)):
    return crud.get_all_students(conn)

# Get Single Student by ID
@app.get("/students/{student_id}")
def get_student_by_id_endpoint(student_id: int, conn=Depends(get_db)):
    return crud.get_student_by_id(conn, student_id)

# Update Student
@app.put("/students/{student_id}")
def update_student_endpoint(student_id: int, student: StudentCreate, conn=Depends(get_db)):
    return crud.update_student(conn, student_id, student)

# Deactivate Student
@app.delete("/students/{student_id}")
def deactivate_student_endpoint(student_id: int, conn=Depends(get_db)):
    return crud.deactivate_student(conn, student_id)


#######################################################
# results ENDPOINTS
######################################################

# Create result
@app.post("/results/")
def create_result_endpoint(result: ResultCreate, conn=Depends(get_db)):
    try:
        return crud.create_result(conn, result)
    except HTTPException as e:
        raise e  # Pass the exception through to the client


# Get  results
@app.get("/results/")
def get_results(conn=Depends(get_db)):
    results = crud.get_results(conn)
    return results


# Get results for a student by studentID (userid)
@app.get("/results/{student_id}")
def get_student_results(student_id: str, conn=Depends(get_db)):
    results = crud.get_results_by_student_id(conn, student_id)
    if not results:
        return {"message": "No results found"}
    
    total_marks = sum(result["marks"] for result in results)
    
    return {
        "student_id": student_id,
        "subjects_with_marks": {result["subjectName"]: result["marks"] for result in results},
        "total_marks": total_marks
    }

# Update a result
@app.put("/results/{result_id}")
def update_result(result_id: int, result: ResultUpdate, conn=Depends(get_db)):
    return crud.update_result(conn, result_id, result)

# Soft delete a result (mark as inactive)
@app.delete("/results/{result_id}")
def delete_result(result_id: int, conn=Depends(get_db)):
    return crud.delete_result(conn, result_id)