// Home.jsx
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

function clamp(n, min, max) {
  return Math.max(min, Math.min(max, n));
}

export default function Home() {
  const navigate = useNavigate();
  const token = localStorage.getItem("auth_token");

  const [user, setUser] = useState(null);
  const [accounts, setAccounts] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [incomes, setIncomes] = useState([]);

  useEffect(() => {
    if (!token) return;

    Promise.all([
      api.get("/users/auth/me/"),
      api.get("/accounts/accounts/"),
      api.get("/finance/expenses/"),
      api.get("/finance/incomes/"),
    ])
      .then(([me, a, e, i]) => {
        setUser(me.data);
        setAccounts(a.data);
        setExpenses(e.data);
        setIncomes(i.data);
      })
      .catch(() => {
        localStorage.removeItem("auth_token");
        navigate("/login");
      });
  }, [token, navigate]);

  const stats = useMemo(() => {
    const balance = accounts.reduce((s, a) => s + Number(a.balance || 0), 0);
    const totalExpense = expenses.reduce((s, x) => s + Number(x.amount || 0), 0);
    const totalIncome = incomes.reduce((s, x) => s + Number(x.amount || 0), 0);
    return { balance, totalExpense, totalIncome, net: totalIncome - totalExpense };
  }, [accounts, expenses, incomes]);

  const chartData = useMemo(() => {
    const maxAccount = Math.max(...accounts.map((a) => Number(a.balance || 0)), 1);
    const accBars = accounts.slice(0, 6).map((a) => ({
      label: a.name,
      value: Number(a.balance || 0),
      pct: clamp((Number(a.balance || 0) / maxAccount) * 100, 0, 100),
    }));

    const maxFlow = Math.max(stats.totalIncome, stats.totalExpense, 1);
    const incomePct = clamp((stats.totalIncome / maxFlow) * 100, 0, 100);
    const expensePct = clamp((stats.totalExpense / maxFlow) * 100, 0, 100);

    return { accBars, incomePct, expensePct };
  }, [accounts, stats]);

  if (!token) {
    return (
      <div className="simple-page">
        <h1>FinanceApp</h1>
        <p>Login to start tracking accounts, incomes, and expenses.</p>
      </div>
    );
  }

  return (
    <div className="simple-page">
      <h1>Welcome back{user?.first_name ? `, ${user.first_name}` : ""}</h1>

      <div className="grid-4" style={{ marginTop: "1rem" }}>
        <div className="stat-card">
          <div className="stat-label">Total Balance</div>
          <div className="stat-value">{stats.balance}</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Total Income</div>
          <div className="stat-value positive">{stats.totalIncome}</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Total Expenses</div>
          <div className="stat-value negative">{stats.totalExpense}</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Net</div>
          <div className={`stat-value ${stats.net >= 0 ? "positive" : "negative"}`}>
            {stats.net}
          </div>
        </div>
      </div>

      {/* ONLY TWO BUTTONS, STYLED */}
      <div className="toolbar" style={{ marginTop: "1.25rem" }}>
        <button className="btn btn-primary" type="button" onClick={() => navigate("/accounts")}>
          Accounts
        </button>

        <button className="btn btn-secondary" type="button" onClick={() => navigate("/transactions")}>
          Transactions
        </button>
      </div>

      {/* Charts */}
      <div className="grid-2" style={{ marginTop: "1.25rem" }}>
        <div className="card">
          <h3 className="card-title">Income vs Expenses</h3>

          <div className="bar-block">
            <div className="bar-row">
              <div className="bar-label">Income</div>
              <div className="bar-track">
                <div className="bar-fill income" style={{ width: `${chartData.incomePct}%` }} />
              </div>
              <div className="bar-number">{stats.totalIncome}</div>
            </div>

            <div className="bar-row">
              <div className="bar-label">Expenses</div>
              <div className="bar-track">
                <div className="bar-fill expense" style={{ width: `${chartData.expensePct}%` }} />
              </div>
              <div className="bar-number">{stats.totalExpense}</div>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="card-title">Top Account Balances</h3>

          {accounts.length === 0 ? (
            <p>No accounts yet.</p>
          ) : (
            <div className="bar-block">
              {chartData.accBars.map((b) => (
                <div className="bar-row" key={b.label}>
                  <div className="bar-label">{b.label}</div>
                  <div className="bar-track">
                    <div className="bar-fill account" style={{ width: `${b.pct}%` }} />
                  </div>
                  <div className="bar-number">{b.value}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}




