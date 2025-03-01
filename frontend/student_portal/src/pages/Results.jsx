import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";



const apiUrl = "http://127.0.0.1:8000";


function Results() {
  const navigate = useNavigate();
  const user_id = localStorage.getItem("student_id");
  const user_name = localStorage.getItem("student_name");

  const [studentResults, setStudentResults] = useState([]); 
  
  useEffect(() => {
    fetch(`${apiUrl}/student_results/${user_id}`)
    .then(response => response.json())
    .then(data => setStudentResults(data))
    .catch(error => console.error("Error fetching results:", error));
  }, [user_id]);
  
  return (
    <>
      <h1>Results for {user_name}</h1>
      <p>StudentID: {user_id}</p>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">Subject</th>
            <th scope="col">Marks</th>
            <th scope="col">Remarks</th>
          </tr>
        </thead>
        <tbody>
          {studentResults.map((result, index) => ( // ✅ Map through results
            <tr key={index}>
              <td>{result.subjectName}</td>
              <td>{result.marks}</td>
              <td>{result.remark}</td>
            </tr>
          ))}
        </tbody>
       
      </table>
      {studentResults.length > 0 && (
      <h5>Total Marks: {studentResults[0].total_marks}</h5>)}
      <br/>
      <button
        type="button"
        className="btn btn-danger"
        onClick={() => {
          localStorage.clear();
          navigate("/login");
        }}
      >
        Logout
      </button>
    </>
  );
}

export default Results;










