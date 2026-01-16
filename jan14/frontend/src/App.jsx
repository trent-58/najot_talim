import { Link, Route, Routes, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";

import Accounts from "./pages/Accounts";
import Transactions from "./pages/Transactions";
import Reports from "./pages/Reports";

import api from "./axios";
import "./style/styles.css";

export default function App() {
  const navigate = useNavigate();

  const [open, setOpen] = useState(false);
  const [token, setToken] = useState(localStorage.getItem("auth_token"));
  const [user, setUser] = useState(null);

  useEffect(() => {
    const onStorage = () => setToken(localStorage.getItem("auth_token"));
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  useEffect(() => {
    if (!token) {
      setUser(null);
      return;
    }
    api.get("/users/auth/me/")
      .then((res) => setUser(res.data))
      .catch(() => {
        localStorage.removeItem("auth_token");
        setToken(null);
        setUser(null);
        navigate("/login");
      });
  }, [token, navigate]);

  const handleLogout = async () => {
    try {
      await api.post("/users/auth/logout/");
    } catch {}

    localStorage.removeItem("auth_token");
    setToken(null);
    setUser(null);
    setOpen(false);
    navigate("/login");
  };

  const fullName =
    user?.first_name || user?.last_name
      ? `${user.first_name || ""} ${user.last_name || ""}`.trim()
      : user?.username || "User";

  const avatarLetter =
    user?.first_name?.[0] || user?.username?.[0] || "U";

  return (
    <>
      <nav className="navbar">
        <div className="navbar-left">
          <Link to="/" className="nav-link">Home</Link>

          {token && (
            <>
              <Link to="/accounts" className="nav-link">Accounts</Link>
              <Link to="/transactions" className="nav-link">Transactions</Link>
              <Link to="/reports" className="nav-link">Reports</Link>
            </>
          )}
        </div>

        <div className="navbar-right">
          {token && user ? (
            <div className="profile-wrapper">
              <button
                type="button"
                className="profile-button"
                onClick={() => setOpen((v) => !v)}
              >
                <span className="profile-avatar">{avatarLetter}</span>
                <span className="profile-fullname">{fullName}</span>
              </button>

              {open && (
                <div className="profile-dropdown">
                  <div className="profile-dropdown-header">
                    <div className="profile-name">{user.username}</div>
                    <div className="profile-email">{user.email || "—"}</div>
                  </div>

                  <div className="profile-divider" />

                  <Link
                    to="/profile"
                    className="profile-dropdown-item"
                    onClick={() => setOpen(false)}
                  >
                    My Profile
                  </Link>

                  <button
                    type="button"
                    className="profile-dropdown-item logout"
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="nav-link">Register</Link>
            </>
          )}
        </div>
      </nav>

      <Routes>
        {/* Home is dashboard-style now */}
        <Route path="/" element={<Home />} />

        {/* auth */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* app pages */}
        <Route path="/accounts" element={<Accounts />} />
        <Route path="/transactions" element={<Transactions />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </>
  );
}
