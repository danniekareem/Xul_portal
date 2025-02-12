import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "./Results.css"; // Import the CSS file

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
            <h2 className="login-title">Teacher/Admin Login</h2>
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

// Protected Dashboard Route

const Dashboard = () => {
    const navigate = useNavigate();
    const user_id = localStorage.getItem("user_id");
    const user_name = localStorage.getItem("user_name");

    const [summary, setSummary] = useState({
        total_students: 0,
        total_teachers: 0,
        total_classes: 0,
        total_subjects: 0,
    });

    useEffect(() => {
        if (!user_id) {
            alert("Unauthorized access. Redirecting to login...");
            navigate("/login_teacher_admin");
            return;
        }

        // Fetch summary data from the backend
        fetch(`${apiUrl}/dashboard-summary/`)
            .then(response => response.json())
            .then(data => setSummary(data))
            .catch(error => console.error("Error fetching summary:", error));
    }, [user_id, navigate]);

    return (
        <div className="dashboard-container">
            {/* Sidebar */}
            <aside className="sidebar">
                <h3>Dashboard</h3>
                <ul>
                    <li onClick={() => navigate("/manage_classes")}>📚 Manage Classes</li>
                    <li onClick={() => navigate("/manage_subjects")}>📖 Manage Subjects</li>
                    <li onClick={() => navigate("/manage_results")}>📝 Manage Results</li>
                    <li onClick={() => navigate("/manage_students")}>👨‍🎓 Manage Students</li>
                </ul>

                {/* 🔹 Logout Button Now Moved Up Slightly */}
                <button className="logout-button" onClick={() => { 
                    localStorage.clear(); 
                    navigate("/login_teacher_admin"); 
                }}>
                    Logout
                </button>
            </aside>


            {/* Main Content */}
            <main className="dashboard-main">
                {/* Teacher/Admin Info */}
                <header className="dashboard-header">
                    <h2>Teacher/Admin Dashboard</h2>
                    <p>Welcome, <strong>{user_name}</strong>!</p>
                </header>

                {/* Summary Section */}
                <div className="dashboard-summary">
                    <div className="summary-card">👨‍🎓 Students: {summary.total_students}</div>
                    <div className="summary-card">👨‍🏫 Teachers: {summary.total_teachers}</div>
                    <div className="summary-card">🏫 Classes: {summary.total_classes}</div>
                    <div className="summary-card">📖 Subjects: {summary.total_subjects}</div>
                </div>
            </main>
        </div>
    );
};


const Results = () => {
    const [results, setResults] = useState(null);
    const studentID = localStorage.getItem("student_id");
    const studentName = localStorage.getItem("student_name");
    const navigate = useNavigate();

    useEffect(() => {
        if (!studentID) {
            alert("Student ID not found. Redirecting to login...");
            navigate("/login_student");
            return;
        }

        fetch(`${apiUrl}/results/${studentID}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.message) {
                    setResults(null); // No results found
                } else {
                    setResults(data);
                }
            })
            .catch((error) => console.error("Error fetching results:", error));
    }, [studentID, navigate]);

    return (
        <div className="report-container">
            <div className="report-header">
                <h2>Student Report</h2>
                <p><strong>Name:</strong> {studentName}</p>
                <p><strong>Student ID:</strong> {studentID}</p>
            </div>

            {results ? (
                <>
                    <table className="results-table">
                        <thead>
                            <tr>
                                <th>Subject</th>
                                <th>Marks</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Object.entries(results.subjects_with_marks || {}).map(([subject, marks]) => (
                                <tr key={subject}>
                                    <td>{subject}</td>
                                    <td>{marks}</td>
                                    <td></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div className="total-marks">
                        <h3>Total Marks: {results.total_marks}</h3>
                    </div>
                </>
            ) : (
                <p className="no-results">No results found.</p>
            )}

            <button className="logout-button" onClick={() => { localStorage.clear(); navigate("/login_student"); }}>
                Logout
            </button>
        </div>
    );
};

export default function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login_student" element={<Login />} />
                <Route path="/results" element={<Results />} />
                <Route path="/login_teacher_admin" element={<TeacherAdminLogin />} />
                <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
        </Router>
    );
}
