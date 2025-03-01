import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const apiUrl = "http://127.0.0.1:8000"; // FastAPI backend URL

function Login  ()  {
    const navigate = useNavigate();
    const [studentID, setStudentID] = useState("");
    const [dob, setDob] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");

        const response = await fetch(`${apiUrl}/student-login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ studentID, dob })
        });
        const data = await response.json();

        if (data.message === "Login successful" && data.student_id) {
            localStorage.setItem("student_id", data.student_id);
            localStorage.setItem("student_name", data.student_name);
            navigate("/results", data.student_id);
           
        } else {
            setError("Invalid credentials");
        }
    };

    return (
        <div className="login-container">
            <h2 className="login-title">Student Login</h2>
            <form onSubmit={handleLogin} className="login-form">
                <input
                    type="text"
                    placeholder="Student ID"
                    value={studentID}
                    onChange={(e) => setStudentID(e.target.value)}
                    required
                    className="input-field"
                />
                <input
                    type="date"
                    value={dob}
                    onChange={(e) => setDob(e.target.value)}
                    required
                    className="input-field"
                />
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
            {error && <p className="error-message">{error}</p>}
        </div>
    );
};


export default Login;

