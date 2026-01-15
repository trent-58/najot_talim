import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api
      .get("/users/auth/me/")
      .then((res) => {
        setUser(res.data);
      })
      .catch(() => {
        localStorage.removeItem("auth_token");
        navigate("/login");
      });
  }, []);

  if (!user) return <p>Loading...</p>;

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {user.username}</p>
    </div>
  );
}
