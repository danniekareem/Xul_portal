import pymssql
from pymssql import Connection
from schemas import UserCreate, ClassCreate, SubjectCreate,TeacherCreate,StudentCreate, ResultCreate, ResultUpdate, TeacherAdminLoginRequest
import bcrypt
from fastapi import HTTPException




def student_login(conn, studentID: str, dob: str):
    cursor = conn.cursor(as_dict=True)

    # 🔹 Check if the student exists and is active
    cursor.execute("SELECT id, firstName, lastName, studentID FROM students WHERE studentID = %s AND DOB = %s AND record_status = 'Active'", (studentID, dob))
    student = cursor.fetchone()

    if not student:
        raise HTTPException(status_code=401, detail="Invalid Student ID or DOB, or account is inactive.")

    return {
        "message": "Login successful",
        "student_id": student["studentID"],
        "student_name": f"{student['firstName']} {student['lastName']}"
    }




def teacher_admin_login(conn, email: str, password: str):
    cursor = conn.cursor(as_dict=True)

    # 🔹 Fetch the user
    cursor.execute(
        "SELECT id, firstName, lastName, password FROM teachers WHERE email = %s AND record_status = 'Active'",
        (email,)
    )
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or account is inactive.")

    #print(f"Stored hashed password: {user['password']}")  # Debugging

    # 🔹 Verify the hashed password
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid password.")

    return {
        "message": "Login successful",
        "user_id": user["id"],
        "user_name": f"{user['firstName']} {user['lastName']}",
       
    }


####################################################
#USER CRUD
####################################################


def create_user(conn, user: UserCreate):
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # SQL query to insert a new user
    query = """
        INSERT INTO users (firstname, lastname, email, password, role)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor = conn.cursor()
    cursor.execute(query, (user.firstname, user.lastname, user.email, hashed_password, user.role))
    conn.commit()

    # Optionally, fetch the user after creation
    cursor.execute("SELECT * FROM users WHERE email=%s", (user.email,))
    db_user = cursor.fetchone()

    return db_user


#SELECT A USER
def get_user(conn, user_id: int):
    """
    Retrieve a user by ID, only if they are active.
    """
    cursor = conn.cursor()
    
    query = """
        SELECT * FROM users 
        WHERE id = %s AND record_status = 'Active'
    """
    
    cursor.execute(query, (user_id,))
    db_user = cursor.fetchone()

    if db_user:
        return {
            "id": db_user[0],
            "firstname": db_user[1],
            "lastname": db_user[2],
            "email": db_user[4],
            "role": db_user[5],
            "record_status": db_user[6],  # Should always be 'Active'
            "created_at": db_user[7],
            "updated_at": db_user[8]
        }
    else:
        return {"error": "User not found or inactive"}
    

#Select All users
def get_all_users(conn):
    """
    Retrieve all active users.
    """
    cursor = conn.cursor()
    
    query = """
        SELECT * FROM users 
        WHERE record_status = 'Active'
    """
    
    cursor.execute(query)
    users = cursor.fetchall()

    if users:
        return [
            {
                "id": user[0],
                "firstname": user[1],
                "lastname": user[2],
                "email": user[4],
                "role": user[5],
                "record_status": user[6],  # Should always be 'Active'
                "created_at": user[7],
                "updated_at": user[8]
            }
            for user in users
        ]
    else:
        return {"message": "No active users found"}



#UDPDATE USER
def update_user(conn: Connection, user_id: int, user: UserCreate):
    # Hash the user's new password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor = conn.cursor()
    
    # Update the user's details in the database
    cursor.execute("""
        UPDATE users
        SET firstname = %s, lastname = %s, email = %s, password = %s, role = %s, record_status = %s, updated_at = GETDATE()
        WHERE id = %s
    """, (user.firstname, user.lastname, user.email, hashed_password, user.role, user.record_status, user_id))
    
    conn.commit()  # Save changes
    return {"message": "User updated successfully"}


#DEACTIVATE USER
def delete_user(conn, user_id: int):
    """
    Soft delete a user by setting record_status to 'Inactive'
    """
    query = """
        UPDATE users 
        SET record_status = 'Inactive'
        WHERE id = %s
    """
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (user_id,))
        conn.commit()

        # Fetch the updated user to confirm the status change
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        db_user = cursor.fetchone()

        return {
            "message": "User has been deactivated",
            "user": {
                "id": db_user[0],
                "firstname": db_user[1],
                "lastname": db_user[2],
                "email": db_user[4],
                "role": db_user[5],
                "record_status": db_user[6],  # Should now be 'Inactive'
                "created_at": db_user[7],
                "updated_at": db_user[8]
            }
        }
    except pymssql.DatabaseError as e:
        print(f"Error occurred: {e}")
        return {"error": "Failed to deactivate user"}
    finally:
        cursor.close()


###########################################
# CLASSES CRUD
###########################################

# Create a new class
def create_class(conn: pymssql.Connection, class_data: ClassCreate):
    cursor = conn.cursor()
    query = "INSERT INTO classes (class) VALUES (%s)"
    cursor.execute(query, (class_data.class_,))
    conn.commit()
    return {"message": "Class added successfully"}


# Get all active classes
def get_all_classes(conn: pymssql.Connection):
    cursor = conn.cursor()
    query = "SELECT * FROM classes WHERE record_status = 'Active'"
    cursor.execute(query)
    classes = cursor.fetchall()

    return [
        {"id": row[0], "class": row[1], "record_status": row[2]}
        for row in classes
    ] if classes else {"message": "No active classes found"}


# Get a single active class
def get_class(conn: pymssql.Connection, class_id: int):
    cursor = conn.cursor()
    query = "SELECT * FROM classes WHERE id = %s AND record_status = 'Active'"
    cursor.execute(query, (class_id,))
    row = cursor.fetchone()
    
    return {"id": row[0], "class": row[1], "record_status": row[2]} if row else {"error": "Class not found"}


# Delete (Deactivate) a class
def delete_class(conn: pymssql.Connection, class_id: int):
    cursor = conn.cursor()
    query = "UPDATE classes SET record_status = 'Inactive' WHERE id = %s"
    cursor.execute(query, (class_id,))
    conn.commit()
    return {"message": "Class deactivated successfully"}


# Update an existing class
def update_class(conn: pymssql.Connection, class_id: int, new_class: int):
    cursor = conn.cursor()

    # Check if the class exists and is active
    cursor.execute("SELECT id FROM classes WHERE id = %s AND record_status = 'Active'", (class_id,))
    existing_class = cursor.fetchone()

    if not existing_class:
        return {"error": "Class not found or inactive"}

    # Update the class value
    query = """
        UPDATE classes 
        SET class = %s
        WHERE id = %s
    """
    cursor.execute(query, (new_class, class_id))
    conn.commit()

    # Fetch and return the updated class
    cursor.execute("SELECT * FROM classes WHERE id = %s", (class_id,))
    updated_class = cursor.fetchone()

    return {
        "message": "Class updated successfully",
        "class": {
            "id": updated_class[0],
            "class": updated_class[1],
            "record_status": updated_class[2]
        }
    }




###########################################
# Subjects CRUD
###########################################



# Create a new subject
def create_subject(conn: pymssql.Connection, subject_data: SubjectCreate):
    cursor = conn.cursor()
    query = "INSERT INTO subjects (subjectName) VALUES (%s)"
    cursor.execute(query, (subject_data.subject_name,))
    conn.commit()
    return {"message": "Subject added successfully"}

# Get all active subjects
def get_all_subjects(conn: pymssql.Connection):
    cursor = conn.cursor()
    query = "SELECT * FROM subjects WHERE record_status = 'Active'"
    cursor.execute(query)
    subjects = cursor.fetchall()

    return [
        {"id": row[0], "subject_name": row[1], "record_status": row[2]}
        for row in subjects
    ] if subjects else {"message": "No active subjects found"}

# Get a single active subject
def get_subject(conn: pymssql.Connection, subject_id: int):
    cursor = conn.cursor()
    query = "SELECT * FROM subjects WHERE id = %s AND record_status = 'Active'"
    cursor.execute(query, (subject_id,))
    row = cursor.fetchone()
    
    return {"id": row[0], "subject_name": row[1], "record_status": row[2]} if row else {"error": "Subject not found"}

# Update an existing subject
def update_subject(conn: pymssql.Connection, subject_id: int, new_subject_name: str):
    cursor = conn.cursor()

    # Check if the subject exists and is active
    cursor.execute("SELECT id FROM subjects WHERE id = %s AND record_status = 'Active'", (subject_id,))
    existing_subject = cursor.fetchone()

    if not existing_subject:
        return {"error": "Subject not found or inactive"}

    # Update the subject name
    query = """
        UPDATE subjects 
        SET subjectName = %s
        WHERE id = %s
    """
    cursor.execute(query, (new_subject_name, subject_id))
    conn.commit()

    # Fetch and return the updated subject
    cursor.execute("SELECT * FROM subjects WHERE id = %s", (subject_id,))
    updated_subject = cursor.fetchone()

    return {
        "message": "Subject updated successfully",
        "subject": {
            "id": updated_subject[0],
            "subject_name": updated_subject[1],
            "record_status": updated_subject[2]
        }
    }

# Delete (Deactivate) a subject
def delete_subject(conn: pymssql.Connection, subject_id: int):
    cursor = conn.cursor()
    query = "UPDATE subjects SET record_status = 'Inactive' WHERE id = %s"
    cursor.execute(query, (subject_id,))
    conn.commit()
    return {"message": "Subject deactivated successfully"}



###########################################
# Teachers CRUD
###########################################



# Create a new teacher
def create_teacher(conn: pymssql.Connection, teacher_data: TeacherCreate):
    cursor = conn.cursor()
    
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(teacher_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    query = """
        INSERT INTO teachers (firstName, lastName, email, password, phoneNumber, classID) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        teacher_data.first_name, teacher_data.last_name, teacher_data.email, 
        hashed_password, teacher_data.phone_number, teacher_data.class_id
    ))
    conn.commit()

    return {"message": "Teacher added successfully"}

# Get all active teachers
def get_all_teachers(conn: pymssql.Connection):
    cursor = conn.cursor()
    query = "SELECT * FROM teachers WHERE record_status = 'Active'"
    cursor.execute(query)
    teachers = cursor.fetchall()

    return [
        {"id": row[0], "first_name": row[1], "last_name": row[2], "email": row[3], 
         "phone_number": row[5], "class_id": row[6], "record_status": row[7]}
        for row in teachers
    ] if teachers else {"message": "No active teachers found"}

# Get a single active teacher
def get_teacher(conn: pymssql.Connection, teacher_id: int):
    cursor = conn.cursor()
    query = "SELECT * FROM teachers WHERE id = %s AND record_status = 'Active'"
    cursor.execute(query, (teacher_id,))
    row = cursor.fetchone()

    return {"id": row[0], "first_name": row[1], "last_name": row[2], "email": row[3], 
            "phone_number": row[5], "class_id": row[6], "record_status": row[7]} if row else {"error": "Teacher not found"}

# Update an existing teacher
def update_teacher(conn: pymssql.Connection, teacher_id: int, teacher_data: TeacherCreate):
    cursor = conn.cursor()

    # Hash the new password
    hashed_password = bcrypt.hashpw(teacher_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    query = """
        UPDATE teachers 
        SET firstName = %s, lastName = %s, email = %s, password = %s, 
            phoneNumber = %s, classID = %s
        WHERE id = %s
    """
    cursor.execute(query, (
        teacher_data.first_name, teacher_data.last_name, teacher_data.email,
        hashed_password, teacher_data.phone_number, teacher_data.class_id, teacher_id
    ))
    conn.commit()

    return {"message": "Teacher updated successfully"}

# Deactivate a teacher instead of deleting
def delete_teacher(conn: pymssql.Connection, teacher_id: int):
    cursor = conn.cursor()
    query = "UPDATE teachers SET record_status = 'Inactive' WHERE id = %s"
    cursor.execute(query, (teacher_id,))
    conn.commit()
    return {"message": "Teacher deactivated successfully"}



###########################################
# Students CRUD
###########################################

#Create a Student
def create_student(conn, student: StudentCreate):
    query = """
        INSERT INTO students (firstName, lastName, studentID, DOB, classID, dateOfJoin, teacherID, record_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Active')
    """
    
    cursor = conn.cursor()
    cursor.execute(query, (student.firstName, student.lastName, student.studentID, student.DOB, student.classID, student.dateOfJoin, student.teacherID))
    conn.commit()

    cursor.execute("SELECT * FROM students WHERE studentID = %s", (student.studentID,))
    return cursor.fetchone()


# Get All Active Students
def get_all_students(conn):
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT * FROM students WHERE record_status = 'Active'")
    return cursor.fetchall()


# Get Active Student by ID
def get_student_by_id(conn, student_id: int):
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT * FROM students WHERE id = %s AND record_status = 'Active'", (student_id,))
    return cursor.fetchone()


# Get update Student by ID
def update_student(conn, student_id: int, student: StudentCreate):
    query = """
        UPDATE students
        SET firstName = %s, lastName = %s, studentID = %s, DOB = %s, classID = %s, dateOfJoin = %s, teacherID = %s
        WHERE id = %s
    """
    
    cursor = conn.cursor()
    cursor.execute(query, (student.firstName, student.lastName, student.studentID, student.DOB, student.classID, student.dateOfJoin, student.teacherID, student_id))
    conn.commit()
    return {"message": "Student updated successfully"}



#Soft Delete (Deactivate) a Student
def deactivate_student(conn, student_id: int):
    query = "UPDATE students SET record_status = 'Inactive' WHERE id = %s"
    
    cursor = conn.cursor()
    cursor.execute(query, (student_id,))
    conn.commit()
    
    return {"message": "Student deactivated successfully"}


###########################################
# Results CRUD
###########################################


def create_result(conn, result):
    cursor = conn.cursor(as_dict=True)

    # 🔹 Check if the teacher exists and is active
    cursor.execute("SELECT record_status FROM teachers WHERE id = %s", (result.teacherID,))
    teacher = cursor.fetchone()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if teacher["record_status"].lower() != "active":
        raise HTTPException(status_code=400, detail="Cannot add result. Teacher is inactive")

    # 🔹 Check if the student exists and is active
    cursor.execute("SELECT record_status FROM students WHERE id = %s", (result.studentID,))
    student = cursor.fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if student["record_status"].lower() != "active":
        raise HTTPException(status_code=400, detail="Cannot add result. Student is inactive")

    # 🔹 Check if the class exists and is active
    cursor.execute("SELECT record_status FROM classes WHERE id = %s", (result.classID,))
    class_data = cursor.fetchone()
    if not class_data:
        raise HTTPException(status_code=404, detail="Class not found")
    if class_data["record_status"].lower() != "active":
        raise HTTPException(status_code=400, detail="Cannot add result. Class is inactive")

    # 🔹 Insert the result if all checks pass
    query = """
        INSERT INTO results (studentID, classID, subjectID, teacherID, marks, result_date, record_status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Active')
    """
    cursor.execute(query, (result.studentID, result.classID, result.subjectID, result.teacherID, result.marks, result.result_date))
    
    conn.commit()
    return {"message": "Result added successfully"}



# Get all active results
def get_results(conn):
    query = """
        SELECT 
            s.firstName AS student_name, 
            s.studentID, 
            c.class AS class_name,
            STRING_AGG(CONCAT(sub.subjectName, ': ', r.marks), ', ') AS subjects_with_marks,
            SUM(r.marks) AS total_marks
        FROM results r
        JOIN students s ON r.studentID = s.id
        JOIN classes c ON r.classID = c.id
        JOIN subjects sub ON r.subjectID = sub.id
        WHERE r.record_status = 'active'
        GROUP BY s.firstName, s.studentID, c.class
        ORDER BY s.studentID;
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Process the rows and return the structured data
    students = []
    for row in rows:
        student = {
            "student_name": row[0],
            "studentID": row[1],
            "class_name": row[2],
            "subjects_with_marks": row[3],
            "total_marks": row[4]
        }
        students.append(student)

    return students



# Fetch results by studentID (userid)
def get_results_by_student_id(conn, student_id: str):
    query = """
        SELECT r.subjectID, s.subjectName, r.marks
        FROM results r
        JOIN subjects s ON r.subjectID = s.id
        JOIN students st ON r.userid = st.studentID
        WHERE r.userid = %s AND r.record_status = 'Active'
    """
    cursor = conn.cursor(as_dict=True)
    cursor.execute(query, (student_id,))
    return cursor.fetchall()


# Update a result
def update_result(conn, result_id: int, result: ResultUpdate):
    query = """
        UPDATE results
        SET marks = %s, result_date = %s
        WHERE id = %s AND record_status = 'Active'
    """
    cursor = conn.cursor()
    cursor.execute(query, (result.marks, result.result_date, result_id))
    conn.commit()
    return {"message": "Result updated successfully"}

# Delete a result (soft delete)
def delete_result(conn, result_id: int):
    query = """
        UPDATE results
        SET record_status = 'Inactive'
        WHERE id = %s
    """
    cursor = conn.cursor()
    cursor.execute(query, (result_id,))
    conn.commit()
    return {"message": "Result deleted (soft delete) successfully"}