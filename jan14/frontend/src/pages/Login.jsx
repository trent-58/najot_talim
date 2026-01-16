import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../axios";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await api.post("/users/auth/login/", {
        username,
        password,
      });

      localStorage.setItem("auth_token", res.data.token);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="page-container">
      <h1 className="page-title">Login</h1>

      {error && <p className="page-error">{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          className="form-input"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          className="form-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button className="primary-button" type="submit">
          Login
        </button>
      </form>

      <p style={{ marginTop: "1rem", textAlign: "center" }}>
        No account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}
