import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

const API = "http://localhost:8000/api";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    try {
      await axios.post(`${API}/users/auth/register/`, { username, email, password });
      navigate("/login");
    } catch (err) {
      const data = err.response?.data;
      if (data) {
        const msg = data.username?.[0] || data.email?.[0] || data.password?.[0] || "Registration failed";
        setError(msg);
      } else {
        setError("Registration failed");
      }
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "2rem auto", padding: "2rem", backgroundColor: "#fff", borderRadius: "8px" }}>
      <h1 style={{ marginBottom: "1.5rem", color: "#0C2C55" }}>Register</h1>
      {error && <p style={{ color: "red", marginBottom: "1rem" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ width: "100%", padding: "0.75rem", marginBottom: "1rem", borderRadius: "4px", border: "1px solid #629FAD", boxSizing: "border-box" }}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ width: "100%", padding: "0.75rem", marginBottom: "1rem", borderRadius: "4px", border: "1px solid #629FAD", boxSizing: "border-box" }}
        />
        <input
          type="password"
          placeholder="Password (min 8 characters)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: "100%", padding: "0.75rem", marginBottom: "1rem", borderRadius: "4px", border: "1px solid #629FAD", boxSizing: "border-box" }}
        />
        <button type="submit" style={{ width: "100%", padding: "0.75rem", backgroundColor: "#0C2C55", color: "#EDEDCE", border: "none", borderRadius: "4px", cursor: "pointer" }}>
          Register
        </button>
      </form>
      <p style={{ marginTop: "1rem", textAlign: "center" }}>
        Have an account? <Link to="/login" style={{ color: "#296374" }}>Login</Link>
      </p>
    </div>
  );
}

