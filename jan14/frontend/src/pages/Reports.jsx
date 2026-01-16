import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Reports() {
  const navigate = useNavigate();
  const [expenses, setExpenses] = useState([]);
  const [incomes, setIncomes] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/finance/expenses/"),
      api.get("/finance/incomes/"),
    ])
      .then(([e, i]) => {
        setExpenses(e.data);
        setIncomes(i.data);
      })
      .catch(() => {
        setError("Failed to load report data");
        navigate("/login");
      });
  }, [navigate]);

  const totals = useMemo(() => {
    const totalExpense = expenses.reduce((s, x) => s + Number(x.amount || 0), 0);
    const totalIncome = incomes.reduce((s, x) => s + Number(x.amount || 0), 0);
    return { totalExpense, totalIncome, net: totalIncome - totalExpense };
  }, [expenses, incomes]);

  return (
    <div className="simple-page">
      <h1>Reports</h1>
      {error && <p className="page-error">{error}</p>}

      <div style={{ marginTop: "1rem" }}>
        <p><strong>Total income:</strong> {totals.totalIncome}</p>
        <p><strong>Total expenses:</strong> {totals.totalExpense}</p>
        <p><strong>Net:</strong> {totals.net}</p>
      </div>
    </div>
  );
}
