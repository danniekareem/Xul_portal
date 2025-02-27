import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "./Results.css"; // Import the CSS file
import ManageClasses from "./pages/ManageClasses";


const apiUrl = "http://127.0.0.1:8000"; // FastAPI backend URL

const Login = () => {
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
            navigate("/results");
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
                <button type="submit" className="submit-btn">Login</button>
            </form>
            {error && <p className="error-message">{error}</p>}
        </div>
    );
};



// Teacher/Admin Login
const TeacherAdminLogin = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");

        const response = await fetch(`${apiUrl}/teacher-admin-login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        
        if (data.message === "Login successful") {
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("user_name", data.user_name);

                navigate("/dashboard");
        } else {
            setError("Invalid credentials");
        }
    };

    return (
        <div className="login-container">
            <h2 className="login-title">Teacher Login</h2>
            <form onSubmit={handleLogin} className="login-form">
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="input-field"
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="input-field"
                />
                <button type="submit" className="submit-btn">Login</button>
            </form>
            {error && <p className="error-message">{error}</p>}
        </div>
    );
};



// Dashboard Component
const Dashboard = () => {
    const navigate = useNavigate();
    const user_id = localStorage.getItem("user_id");
    const user_name = localStorage.getItem("user_name"); // ✅ Define user_name

    const [summary, setSummary] = useState({
        total_students: 0,
        total_teachers: 0,
        total_classes: 0,
        total_subjects: 0,
    });

    const [activeSection, setActiveSection] = useState("dashboard");

    useEffect(() => {
        if (!user_id) {
            alert("Unauthorized access. Redirecting to login...");
            navigate("/login_teacher_admin");
            return;
        }

        fetch(`${apiUrl}/dashboard-summary/`)
            .then(response => response.json())
            .then(data => setSummary(data))
            .catch(error => console.error("Error fetching summary:", error));
    }, [user_id, navigate]);

    return (
        <div className="dashboard-container">
            <aside className="sidebar">
                <h3>Dashboard</h3>
                <ul>
                    <li onClick={() => setActiveSection("dashboard")}>🏠 Home</li>
                    <li onClick={() => setActiveSection("manage_classes")}>📚 Manage Classes</li>
                    <li onClick={() => setActiveSection("manage_subjects")}>📖 Manage Subjects</li>
                    <li onClick={() => setActiveSection("manage_results")}>📝 Manage Results</li>
                    <li onClick={() => setActiveSection("manage_students")}>👨‍🎓 Manage Students</li>
                </ul>

                <button className="logout-button" onClick={() => { 
                    localStorage.clear(); 
                    navigate("/login_teacher_admin"); 
                }}>
                    Logout
                </button>
            </aside>

            <main className="dashboard-main">
                <header className="dashboard-header">
                    <h2>Teacher/Admin Dashboard</h2>
                    <p>Welcome, <strong>{user_name}</strong>!</p>
                </header>

                {activeSection === "dashboard" && (
                    <div className="dashboard-summary">
                        <div className="summary-card">👨‍🎓 Students: {summary.total_students}</div>
                        <div className="summary-card">👨‍🏫 Teachers: {summary.total_teachers}</div>
                        <div className="summary-card">🏫 Classes: {summary.total_classes}</div>
                        <div className="summary-card">📖 Subjects: {summary.total_subjects}</div>
                    </div>
                )}

                {activeSection === "manage_classes" && <ManageClasses user_name={user_name} />}
            </main>
        </div>
    );
};


// Results Component...

export default function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login_student" element={<Login />} />
                
                <Route path="/login_teacher_admin" element={<TeacherAdminLogin />} />
                <Route path="/dashboard" element={<Dashboard />} />
                {/* Remove separate route for ManageClasses */}
            </Routes>
        </Router>
    );
}




