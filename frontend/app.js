// app.js

const apiUrl = 'http://127.0.0.1:8000'; // URL of your FastAPI server

document.addEventListener('DOMContentLoaded', function() {
    getResults();
});

// Fetch results from the backend
function getResults() {
    fetch('http://127.0.0.1:8000/results/')
    .then(response => response.json())
    .then(data => {
        console.log(data); // Debugging: Check response in the browser console
        
        const resultsTableBody = document.querySelector('#resultsTable tbody');

        // Clear previous rows
        resultsTableBody.innerHTML = '';

        data.forEach(student => {
            // Create a new row for each student
            const row = document.createElement('tr');
            
            // Add student details
            row.innerHTML = `
                <td>${student.student_name}</td>
                <td>${student.studentID}</td>
                <td>${student.class_name}</td>  <!-- Now showing as Standard -->
                <td>${student.subjects_with_marks}</td>
                <td>${student.total_marks}</td>
            `;

            // Append the row to the table body
            resultsTableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching results:', error);
    });
}

// Handle form submission to add a new result
document.getElementById('add-result-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const resultData = {
        studentID: document.getElementById('studentID').value,
        classID: document.getElementById('classID').value,
        subjectID: document.getElementById('subjectID').value,
        teacherID: document.getElementById('teacherID').value,
        marks: document.getElementById('marks').value,
        result_date: document.getElementById('result_date').value,
    };

    try {
        const response = await fetch(`${apiUrl}/results/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(resultData)
        });

        if (response.ok) {
            alert('Result added successfully!');
            getResults(); // Refresh the results list
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error adding result:', error);
    }
});

// Fetch results when the page loads
window.onload = function() {
    getResults();
};
