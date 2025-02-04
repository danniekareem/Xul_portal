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

function Results() {
  const [results, setResults] = useState(null);
  const studentID = localStorage.getItem("student_id");
  const studentName = localStorage.getItem("student_name");
  const navigate = useNavigate();

  useEffect(() => {
      if (!studentID) {
          alert("Student ID not found. Redirecting to login...");
          navigate("/");
          return;
      }

      fetch(`http://127.0.0.1:8000/results/${studentID}`)
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
           <button className="logout-button" onClick={() => { localStorage.clear(); navigate("/"); }}>
                Logout
            </button>
      </div>
  );
}


export default function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/results" element={<Results />} />
            </Routes>
        </Router>
    );
}
