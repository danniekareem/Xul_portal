import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const apiUrl = "http://127.0.0.1:8000";

export default function ManageClasses() {
    const navigate = useNavigate();
    const [classes, setClasses] = useState([]);
    const [newClass, setNewClass] = useState("");
    const [editingClass, setEditingClass] = useState(null);
    const [editClassName, setEditClassName] = useState("");

    useEffect(() => {
        fetchClasses();
    }, []);

    const fetchClasses = async () => {
        const response = await fetch(`${apiUrl}/classes`);
        const data = await response.json();
        setClasses(data);
    };

    const addClass = async () => {
        if (!newClass.trim()) return;
        await fetch(`${apiUrl}/classes`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ class_: parseInt(newClass) }),
        });
        setNewClass("");
        fetchClasses();
    };

    const deleteClass = async (id) => {
        await fetch(`${apiUrl}/classes/${id}`, { method: "DELETE" });
        fetchClasses();
    };

    const startEditing = (classItem) => {
        setEditingClass(classItem.id);
        setEditClassName(classItem.class);
    };

    const updateClass = async (id) => {
        await fetch(`${apiUrl}/classes/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ class_: parseInt(editClassName) }),
        });
        setEditingClass(null);
        fetchClasses();
    };

    return (
        <div className="manage-classes-container">
            <h2 className="section-title">📚 Manage Classes</h2>

            {/* Add Class Section */}
            <div className="class-form">
                <input
                    type="number"
                    placeholder="Enter Class Number"
                    value={newClass}
                    onChange={(e) => setNewClass(e.target.value)}
                />
                <button className="primary-button" onClick={addClass}>➕ Add Class</button>
            </div>

            {/* Class List */}
            <div className="class-list">
                <table>
                    <thead>
                        <tr>
                            <th>Class</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {classes.length > 0 ? (
                            classes.map((classItem) => (
                                <tr key={classItem.id}>
                                    <td>
                                        {editingClass === classItem.id ? (
                                            <input
                                                type="number"
                                                value={editClassName}
                                                onChange={(e) => setEditClassName(e.target.value)}
                                            />
                                        ) : (
                                            `Class ${classItem.class}`
                                        )}
                                    </td>
                                    <td>
                                        {editingClass === classItem.id ? (
                                            <button className="save-button" onClick={() => updateClass(classItem.id)}>💾 Save</button>
                                        ) : (
                                            <button className="edit-button" onClick={() => startEditing(classItem)}>✏️ Edit</button>
                                        )}
                                        <button className="delete-button" onClick={() => deleteClass(classItem.id)}>🗑️ Delete</button>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="2" className="no-data">No classes available</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

        </div>
    );
}
