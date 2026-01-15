import { Routes, Route, Link, useNavigate } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const navigate = useNavigate();
  const token = localStorage.getItem("auth_token");

  const handleLogout = () => {
    localStorage.removeItem("auth_token");
    navigate("/");
  };

  return (
    <>
      <nav
        style={{
          padding: "1rem",
          backgroundColor: "#0C2C55",
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <div>
          <Link to="/" style={{ marginRight: "1rem", color: "#EDEDCE" }}>
            Home
          </Link>
          <Link to="/about" style={{ marginRight: "1rem", color: "#EDEDCE" }}>
            About
          </Link>
          {token && (
            <Link to="/dashboard" style={{ color: "#EDEDCE" }}>
              Dashboard
            </Link>
          )}
        </div>

        <div>
          {token ? (
            <button
              onClick={handleLogout}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: "#296374",
                color: "#EDEDCE",
                border: "none",
                borderRadius: "4px",
              }}
            >
              Logout
            </button>
          ) : (
            <>
              <Link to="/login" style={{ marginRight: "1rem", color: "#EDEDCE" }}>
                Login
              </Link>
              <Link to="/register" style={{ color: "#EDEDCE" }}>
                Register
              </Link>
            </>
          )}
        </div>
      </nav>

      <div style={{ padding: "1rem" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </>
  );
}
