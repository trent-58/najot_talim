import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../axios";

export default function Register() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await api.post("/users/auth/register/", form);
      localStorage.setItem("auth_token", res.data.token);
      navigate("/");
    } catch (err) {
      setError("Registration failed");
    }
  };

  return (
    <div className="page-container">
      <h1 className="page-title">Register</h1>

      {error && <p className="page-error">{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          className="form-input"
          placeholder="Username"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
        />

        <input
          className="form-input"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input
          className="form-input"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />

        <button className="primary-button" type="submit">
          Register
        </button>
      </form>

      <p style={{ marginTop: "1rem", textAlign: "center" }}>
        Have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}
