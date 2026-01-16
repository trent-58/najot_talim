// Profile.jsx
import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import api from "../axios";

export default function Profile() {
    const navigate = useNavigate();

    const [user, setUser] = useState(null);
    const [editData, setEditData] = useState({});
    const [error, setError] = useState("");

    const [showEdit, setShowEdit] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showDelete, setShowDelete] = useState(false);

    const [passwords, setPasswords] = useState({
        old: "", new1: "", new2: "",
    });

    useEffect(() => {
        api.get("/users/auth/me/")
            .then((res) => {
                setUser(res.data);
                setEditData(res.data);
            })
            .catch(() => {
                localStorage.removeItem("auth_token");
                navigate("/login");
            });
    }, [navigate]);

    const saveProfile = async () => {
        try {
            const res = await api.patch("/users/auth/me/", editData);
            setUser(res.data);
            setShowEdit(false);
        } catch {
            setError("Failed to update profile");
        }
    };

    const changePassword = async () => {
        if (!passwords.new1 || passwords.new1 !== passwords.new2) {
            setError("Passwords do not match");
            return;
        }

        try {
            await api.patch("/users/auth/me/", {password: passwords.new1});
            localStorage.removeItem("auth_token");
            navigate("/login");
        } catch {
            setError("Password update failed");
        }
    };

    const deleteAccount = async () => {
        try {
            await api.delete("/users/auth/me/");
            localStorage.removeItem("auth_token");
            navigate("/");
        } catch {
            setError("Delete failed");
        }
    };

    if (!user) return null;

    return (<div className="page-container">
            <h1 className="page-title">Profile Overview</h1>

            {error && <p className="page-error">{error}</p>}

            <div style={{marginBottom: "2rem"}}>
                <p><strong>Username:</strong> {user.username}</p>
                <p><strong>Email:</strong> {user.email || "-"}</p>
                <p><strong>First name:</strong> {user.first_name || "-"}</p>
                <p><strong>Last name:</strong> {user.last_name || "-"}</p>
                <p><strong>Language:</strong> {user.language || "-"}</p>
            </div>

            <button className="primary-button" onClick={() => setShowEdit(true)}>
                Edit Profile
            </button>

            <button
                className="secondary-button"
                style={{marginTop: "0.75rem"}}
                onClick={() => setShowPassword(true)}
            >
                Update Password
            </button>

            <button
                className="danger-button"
                style={{marginTop: "0.75rem"}}
                onClick={() => setShowDelete(true)}
            >
                Delete Account
            </button>

            {showEdit && (<div className="modal">
                    <div className="modal-box">
                        <h3>Edit Profile</h3>

                        {/* Username */}
                        <div className="form-group">
                            <label className="form-label">Username</label>
                            <input
                                className="form-input"
                                placeholder="Username"
                                value={editData.username || ""}
                                onChange={(e) => setEditData({...editData, username: e.target.value})}
                            />
                        </div>

                        {/* Email */}
                        <div className="form-group">
                            <label className="form-label">Email</label>
                            <input
                                className="form-input"
                                placeholder="Email"
                                value={editData.email || ""}
                                onChange={(e) => setEditData({...editData, email: e.target.value})}
                            />
                        </div>

                        {/* First name */}
                        <div className="form-group">
                            <label className="form-label">First name</label>
                            <input
                                className="form-input"
                                placeholder="First name"
                                value={editData.first_name || ""}
                                onChange={(e) => setEditData({...editData, first_name: e.target.value})}
                            />
                        </div>

                        {/* Last name */}
                        <div className="form-group">
                            <label className="form-label">Last name</label>
                            <input
                                className="form-input"
                                placeholder="Last name"
                                value={editData.last_name || ""}
                                onChange={(e) => setEditData({...editData, last_name: e.target.value})}
                            />
                        </div>

                        {/* Language dropdown */}
                        <div className="form-group">
                            <label className="form-label">Language</label>
                            <select
                                className="form-input"
                                value={editData.language || ""}
                                onChange={(e) => setEditData({...editData, language: e.target.value})}
                            >
                                <option value="">Select language</option>
                                <option value="en">English</option>
                                <option value="ru">Russian</option>
                                <option value="uz">Uzbek</option>
                            </select>
                        </div>


                        <button className="primary-button" onClick={saveProfile}>
                            Save
                        </button>

                        <button
                            className="secondary-button"
                            style={{marginTop: "0.5rem"}}
                            onClick={() => setShowEdit(false)}
                        >
                            Cancel
                        </button>
                    </div>
                </div>)}

            {showPassword && (<div className="modal">
                    <div className="modal-box">
                        <h3>Update Password</h3>

                        {["Old password", "New password", "Repeat new password"].map((label, i) => (
                            <div className="form-group" key={label}>
                                <label className="form-label">{label}</label>
                                <input
                                    type="password"
                                    className="form-input"
                                    placeholder={label}
                                    onChange={(e) => setPasswords({
                                        ...passwords, [i === 0 ? "old" : i === 1 ? "new1" : "new2"]: e.target.value,
                                    })}
                                />
                            </div>))}

                        <button className="primary-button" onClick={changePassword}>
                            Update
                        </button>

                        <button
                            className="secondary-button"
                            style={{marginTop: "0.5rem"}}
                            onClick={() => setShowPassword(false)}
                        >
                            Cancel
                        </button>
                    </div>
                </div>)}

            {showDelete && (<div className="modal">
                    <div className="modal-box">
                        <h3>Delete Account</h3>
                        <p>This action is permanent.</p>

                        <button className="danger-button" onClick={deleteAccount}>
                            Confirm Delete
                        </button>

                        <button
                            className="secondary-button"
                            style={{marginTop: "0.5rem"}}
                            onClick={() => setShowDelete(false)}
                        >
                            Cancel
                        </button>
                    </div>
                </div>)}
        </div>);
}
