import pymssql
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
import crud 
from schemas import UserCreate, ClassCreate,SubjectCreate,TeacherCreate, StudentCreate, ResultCreate, ResultUpdate, StudentLoginRequest, TeacherAdminLoginRequest, ClassUpdate,Class
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    "http://localhost:5173"
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


# 🔹 Endpoint for teacher/admin login
@app.post("/teacher-admin-login/")
def teacher_admin_login(request: TeacherAdminLoginRequest, conn=Depends(get_db)):
    return crud.teacher_admin_login(conn, request.email, request.password)

@app.get("/dashboard-summary/")
def dashboard_summary(conn=Depends(get_db)):
    cursor = conn.cursor(as_dict=True)

    # Get total students
    cursor.execute("SELECT COUNT(*) AS total_students FROM students WHERE record_status = 'Active'")
    total_students = cursor.fetchone()["total_students"]

    # Get total teachers
    cursor.execute("SELECT COUNT(*) AS total_teachers FROM teachers WHERE record_status = 'Active'")
    total_teachers = cursor.fetchone()["total_teachers"]

    # Get total classes
    cursor.execute("SELECT COUNT(*) AS total_classes FROM classes WHERE record_status = 'Active'")
    total_classes = cursor.fetchone()["total_classes"]

    # Get total subjects
    cursor.execute("SELECT COUNT(*) AS total_subjects FROM subjects WHERE record_status = 'Active'")
    total_subjects = cursor.fetchone()["total_subjects"]

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_classes": total_classes,
        "total_subjects": total_subjects
    }


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
#@app.put("/classes/{class_id}")
#def modify_class(class_id: int, new_class: int, conn: pymssql.Connection = Depends(get_db)):
 #   return crud.update_class(conn, class_id, new_class)


@app.put("/classes/{class_id}")
async def update_class(class_id: int, class_data: ClassUpdate, conn: pymssql.Connection = Depends(get_db)):
    #print(f"Received request to update class {class_id} with data: {class_data.dict()}")  # Debugging print

    cursor = conn.cursor()

    # Check if class ID exists
    cursor.execute("SELECT id FROM classes WHERE id = %s", (class_id,))
    existing_class = cursor.fetchone()
    if not existing_class:
        print(f"Class ID {class_id} not found.")  # Debugging print
        raise HTTPException(status_code=404, detail="Class not found")

    # Check if the new class_ value already exists
    cursor.execute("SELECT id FROM classes WHERE class = %s AND id != %s", (class_data.class_, class_id))
    duplicate_class = cursor.fetchone()
    if duplicate_class:
        print(f"Class {class_data.class_} already exists.")  # Debugging print
        raise HTTPException(status_code=400, detail="Class already exists")

    # Proceed with update
    cursor.execute("UPDATE classes SET class = %s WHERE id = %s", (class_data.class_, class_id))
    conn.commit()

    print(f"Class {class_id} updated successfully.")  # Debugging print
    return {"message": "Class updated successfully"}



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
# students ENDPOINTS
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
@app.get("/student_results/{student_id}")
def get_student_results(student_id: str, conn=Depends(get_db)):
    #logger.info(f"Fetching results for student ID: {student_id}")  

    results = crud.get_results_by_student_id(conn, student_id)  # ✅ Make sure it's calling the function in `crud.py`
    
    if not results:
        logger.info(f"No results found for student ID: {student_id}")
        return {"message": "No results found"}

    logger.info(f"Response: {results}")  
    return results

# Update a result
@app.put("/results/{result_id}")
def update_result(result_id: int, result: ResultUpdate, conn=Depends(get_db)):
    return crud.update_result(conn, result_id, result)

# Soft delete a result (mark as inactive)
@app.delete("/results/{result_id}")
def delete_result(result_id: int, conn=Depends(get_db)):
    return crud.delete_result(conn, result_id)