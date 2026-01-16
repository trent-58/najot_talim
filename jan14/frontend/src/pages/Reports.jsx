// Reports.jsx
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Reports() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  const [accounts, setAccounts] = useState([]);
  const [expenseCats, setExpenseCats] = useState([]);
  const [incomeCats, setIncomeCats] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [incomes, setIncomes] = useState([]);

  const [duration, setDuration] = useState("month");
  const [accountId, setAccountId] = useState("all");

  const loadAll = async () => {
    setErr("");
    setLoading(true);
    try {
      const [a, ec, ic, ex, inc] = await Promise.all([
        api.get("/accounts/accounts/"),
        api.get("/accounts/expense-categories/"),
        api.get("/accounts/income-categories/"),
        api.get("/finance/expenses/"),
        api.get("/finance/incomes/"),
      ]);
      setAccounts(a.data || []);
      setExpenseCats(ec.data || []);
      setIncomeCats(ic.data || []);
      setExpenses(ex.data || []);
      setIncomes(inc.data || []);
    } catch {
      localStorage.removeItem("auth_token");
      navigate("/login");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  const now = new Date();

  const startForDuration = useMemo(() => {
    const startOfDay = (x) => new Date(x.getFullYear(), x.getMonth(), x.getDate());
    const startOfWeekMon = (x) => {
      const day = x.getDay();
      const diff = day === 0 ? -6 : 1 - day;
      const y = new Date(x);
      y.setDate(y.getDate() + diff);
      return startOfDay(y);
    };
    const addMonths = (x, m) => {
      const y = new Date(x);
      y.setMonth(y.getMonth() + m);
      return y;
    };
    const today = startOfDay(now);

    if (duration === "today") return today;
    if (duration === "week") return startOfWeekMon(now);
    if (duration === "month") return new Date(now.getFullYear(), now.getMonth(), 1);
    if (duration === "3m") return addMonths(today, -3);
    if (duration === "6m") return addMonths(today, -6);
    if (duration === "year") return new Date(now.getFullYear(), 0, 1);
    return new Date(1970, 0, 1);
  }, [duration]);

  const accountMap = useMemo(() => new Map(accounts.map((a) => [a.id, a])), [accounts]);
  const expenseCatMap = useMemo(() => new Map(expenseCats.map((c) => [c.id, c])), [expenseCats]);
  const incomeCatMap = useMemo(() => new Map(incomeCats.map((c) => [c.id, c])), [incomeCats]);

  const inRange = (iso) => {
    const d = new Date(iso);
    return d >= startForDuration && d <= now;
  };

  const filteredExpenses = useMemo(() => {
    let list = expenses || [];
    list = list.filter((x) => x.created_at && inRange(x.created_at));
    if (accountId !== "all") list = list.filter((x) => String(x.account) === String(accountId));
    return list;
  }, [expenses, duration, accountId, startForDuration]);

  const filteredIncomes = useMemo(() => {
    let list = incomes || [];
    list = list.filter((x) => x.created_at && inRange(x.created_at));
    if (accountId !== "all") list = list.filter((x) => String(x.account) === String(accountId));
    return list;
  }, [incomes, duration, accountId, startForDuration]);

  const totals = useMemo(() => {
    const sum = (arr) => arr.reduce((s, x) => s + Number(x.amount || 0), 0);
    const income = sum(filteredIncomes);
    const expense = sum(filteredExpenses);
    const net = income - expense;
    return { income, expense, net };
  }, [filteredIncomes, filteredExpenses]);

  const daysInRange = useMemo(() => {
    const ms = now.getTime() - startForDuration.getTime();
    const d = Math.max(1, Math.ceil(ms / (1000 * 60 * 60 * 24)));
    return d;
  }, [startForDuration]);

  const avg = useMemo(() => {
    return {
      incomePerDay: totals.income / daysInRange,
      expensePerDay: totals.expense / daysInRange,
      netPerDay: totals.net / daysInRange,
    };
  }, [totals, daysInRange]);

  const allTx = useMemo(() => {
    const ex = filteredExpenses.map((x) => ({ ...x, tx_type: "expense" }));
    const inc = filteredIncomes.map((x) => ({ ...x, tx_type: "income" }));
    return [...ex, ...inc].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }, [filteredExpenses, filteredIncomes]);

  const topExpenseCats = useMemo(() => {
    const m = new Map();
    filteredExpenses.forEach((x) => {
      const key = x.category == null ? "none" : String(x.category);
      m.set(key, (m.get(key) || 0) + Number(x.amount || 0));
    });
    const rows = [...m.entries()]
      .map(([k, v]) => ({
        key: k,
        label: k === "none" ? "No category" : expenseCatMap.get(Number(k))?.name || "—",
        value: v,
      }))
      .sort((a, b) => b.value - a.value);
    return rows.slice(0, 6);
  }, [filteredExpenses, expenseCatMap]);

  const topIncomeCats = useMemo(() => {
    const m = new Map();
    filteredIncomes.forEach((x) => {
      const key = x.category == null ? "none" : String(x.category);
      m.set(key, (m.get(key) || 0) + Number(x.amount || 0));
    });
    const rows = [...m.entries()]
      .map(([k, v]) => ({
        key: k,
        label: k === "none" ? "No category" : incomeCatMap.get(Number(k))?.name || "—",
        value: v,
      }))
      .sort((a, b) => b.value - a.value);
    return rows.slice(0, 6);
  }, [filteredIncomes, incomeCatMap]);

  const monthKey = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;

  const monthlySeries = useMemo(() => {
    const mIncome = new Map();
    const mExpense = new Map();

    filteredIncomes.forEach((x) => {
      const d = new Date(x.created_at);
      const k = monthKey(d);
      mIncome.set(k, (mIncome.get(k) || 0) + Number(x.amount || 0));
    });

    filteredExpenses.forEach((x) => {
      const d = new Date(x.created_at);
      const k = monthKey(d);
      mExpense.set(k, (mExpense.get(k) || 0) + Number(x.amount || 0));
    });

    const keys = new Set([...mIncome.keys(), ...mExpense.keys()]);
    const sorted = [...keys].sort((a, b) => (a < b ? -1 : 1));

    return sorted.map((k) => ({
      k,
      income: mIncome.get(k) || 0,
      expense: mExpense.get(k) || 0,
      net: (mIncome.get(k) || 0) - (mExpense.get(k) || 0),
    }));
  }, [filteredIncomes, filteredExpenses]);

  const fmt = (n) => {
    const x = Number(n || 0);
    if (!Number.isFinite(x)) return "0";
    return x.toLocaleString(undefined, { maximumFractionDigits: 2 });
  };

  const periodLabel = useMemo(() => {
    if (duration === "today") return "Today";
    if (duration === "week") return "This week";
    if (duration === "month") return "This month";
    if (duration === "3m") return "Last 3 months";
    if (duration === "6m") return "Last 6 months";
    if (duration === "year") return "This year";
    return "All time";
  }, [duration]);

  const miniBars = useMemo(() => {
    const max = Math.max(1, ...monthlySeries.map((x) => Math.max(x.income, x.expense)));
    return monthlySeries.slice(-8).map((x) => ({
      ...x,
      incomePct: (x.income / max) * 100,
      expensePct: (x.expense / max) * 100,
    }));
  }, [monthlySeries]);

  const donut = useMemo(() => {
    const total = totals.income + totals.expense;
    if (total <= 0) return { incomePct: 50, expensePct: 50 };
    return {
      incomePct: (totals.income / total) * 100,
      expensePct: (totals.expense / total) * 100,
    };
  }, [totals]);

  const Donut = ({ incomePct, expensePct }) => {
    const r = 46;
    const c = 2 * Math.PI * r;
    const incomeLen = (incomePct / 100) * c;
    const expenseLen = (expensePct / 100) * c;

    return (
      <svg width="120" height="120" viewBox="0 0 120 120" className="donut">
        <g transform="translate(60 60) rotate(-90)">
          <circle r={r} cx="0" cy="0" fill="transparent" stroke="rgba(148,163,184,0.35)" strokeWidth="14" />
          <circle
            r={r}
            cx="0"
            cy="0"
            fill="transparent"
            stroke="var(--blue)"
            strokeWidth="14"
            strokeDasharray={`${incomeLen} ${c - incomeLen}`}
            strokeLinecap="round"
          />
          <circle
            r={r}
            cx="0"
            cy="0"
            fill="transparent"
            stroke="var(--red)"
            strokeWidth="14"
            strokeDasharray={`${expenseLen} ${c - expenseLen}`}
            strokeDashoffset={-incomeLen}
            strokeLinecap="round"
          />
        </g>
        <text x="60" y="58" textAnchor="middle" className="donut-title">
          {fmt(totals.net)}
        </text>
        <text x="60" y="78" textAnchor="middle" className="donut-sub">
          Net
        </text>
      </svg>
    );
  };

  return (
    <div className="simple-page">
      <div className="page-head">
        <div>
          <h1>Reports</h1>
          <p className="muted">{periodLabel}</p>
        </div>

        <div className="toolbar">
          <select className="form-input select-compact" value={duration} onChange={(e) => setDuration(e.target.value)}>
            <option value="today">Today</option>
            <option value="week">This week</option>
            <option value="month">This month</option>
            <option value="3m">Last 3 months</option>
            <option value="6m">Last 6 months</option>
            <option value="year">This year</option>
            <option value="all">All time</option>
          </select>

          <select className="form-input select-compact" value={accountId} onChange={(e) => setAccountId(e.target.value)}>
            <option value="all">All accounts</option>
            {accounts.map((a) => (
              <option key={a.id} value={a.id}>
                {a.name} ({a.currency})
              </option>
            ))}
          </select>

          <button type="button" className="btn btn-ghost" onClick={loadAll}>
            Refresh
          </button>
        </div>
      </div>

      {err && <p className="page-error">{err}</p>}

      {loading ? (
        <div className="card">
          <p>Loading…</p>
        </div>
      ) : (
        <>
          <div className="report-grid">
            <div className="card stat-card">
              <div className="stat-title">Income</div>
              <div className="stat-value positive">+ {fmt(totals.income)}</div>
              <div className="stat-sub muted">{fmt(avg.incomePerDay)} / day</div>
            </div>

            <div className="card stat-card">
              <div className="stat-title">Expense</div>
              <div className="stat-value negative">- {fmt(totals.expense)}</div>
              <div className="stat-sub muted">{fmt(avg.expensePerDay)} / day</div>
            </div>

            <div className="card stat-card">
              <div className="stat-title">Net</div>
              <div className={`stat-value ${totals.net >= 0 ? "positive" : "negative"}`}>{fmt(totals.net)}</div>
              <div className="stat-sub muted">{fmt(avg.netPerDay)} / day</div>
            </div>

            <div className="card chart-card">
              <div className="chart-head">
                <div className="chart-title">Income vs Expense</div>
                <div className="legend">
                  <span className="legend-dot blue" /> Income
                  <span className="legend-dot red" /> Expense
                </div>
              </div>
              <div className="chart-body">
                <Donut incomePct={donut.incomePct} expensePct={donut.expensePct} />
                <div className="chart-metrics">
                  <div className="metric-row">
                    <div className="metric-label">Income</div>
                    <div className="metric-value">{fmt(totals.income)}</div>
                  </div>
                  <div className="metric-row">
                    <div className="metric-label">Expense</div>
                    <div className="metric-value">{fmt(totals.expense)}</div>
                  </div>
                  <div className="metric-row">
                    <div className="metric-label">Days</div>
                    <div className="metric-value">{daysInRange}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="report-grid-2">
            <div className="card chart-card">
              <div className="chart-head">
                <div className="chart-title">Monthly trend</div>
                <div className="muted">{miniBars.length ? `${miniBars[0].k} → ${miniBars[miniBars.length - 1].k}` : "—"}</div>
              </div>

              <div className="bar-wrap">
                {miniBars.length ? (
                  miniBars.map((x) => (
                    <div key={x.k} className="bar-col">
                      <div className="bar-stack">
                        <div className="bar income" style={{ height: `${x.incomePct}%` }} />
                        <div className="bar expense" style={{ height: `${x.expensePct}%` }} />
                      </div>
                      <div className="bar-label">{x.k.slice(5)}</div>
                    </div>
                  ))
                ) : (
                  <p>No data.</p>
                )}
              </div>

              <div className="bar-legend">
                <span className="legend-dot blue" /> Income
                <span className="legend-dot red" /> Expense
              </div>
            </div>

            <div className="card chart-card">
              <div className="chart-head">
                <div className="chart-title">Top expense categories</div>
                <div className="muted">By total spend</div>
              </div>

              {topExpenseCats.length ? (
                <div className="rank-list">
                  {topExpenseCats.map((x, idx) => (
                    <div className="rank-row" key={`ex-${x.key}`}>
                      <div className="rank-left">
                        <span className="rank-pill">{idx + 1}</span>
                        <span className="rank-name">{x.label}</span>
                      </div>
                      <div className="rank-val negative">{fmt(x.value)}</div>
                    </div>
                  ))}
                </div>
              ) : (
                <p>No expenses.</p>
              )}
            </div>

            <div className="card chart-card">
              <div className="chart-head">
                <div className="chart-title">Top income categories</div>
                <div className="muted">By total income</div>
              </div>

              {topIncomeCats.length ? (
                <div className="rank-list">
                  {topIncomeCats.map((x, idx) => (
                    <div className="rank-row" key={`in-${x.key}`}>
                      <div className="rank-left">
                        <span className="rank-pill">{idx + 1}</span>
                        <span className="rank-name">{x.label}</span>
                      </div>
                      <div className="rank-val positive">{fmt(x.value)}</div>
                    </div>
                  ))}
                </div>
              ) : (
                <p>No incomes.</p>
              )}
            </div>

            <div className="card chart-card">
              <div className="chart-head">
                <div className="chart-title">Latest activity</div>
                <div className="muted">Last 10 transactions</div>
              </div>

              {allTx.length ? (
                <div className="mini-table">
                  {allTx.slice(0, 10).map((t) => {
                    const a = accountMap.get(t.account);
                    const aLabel = a ? a.name : "—";
                    const cLabel =
                      t.tx_type === "expense"
                        ? t.category == null
                          ? "No category"
                          : expenseCatMap.get(t.category)?.name || "—"
                        : t.category == null
                          ? "No category"
                          : incomeCatMap.get(t.category)?.name || "—";

                    return (
                      <div className="mini-row" key={`${t.tx_type}-${t.id}`}>
                        <div className="mini-left">
                          <span className={`mini-badge ${t.tx_type === "income" ? "mini-income" : "mini-expense"}`}>
                            {t.tx_type}
                          </span>
                          <div className="mini-meta">
                            <div className="mini-title">{cLabel}</div>
                            <div className="mini-sub muted">
                              {aLabel} • {t.created_at ? new Date(t.created_at).toLocaleString() : "—"}
                            </div>
                          </div>
                        </div>
                        <div className={`mini-amt ${t.tx_type === "income" ? "positive" : "negative"}`}>
                          {t.tx_type === "income" ? "+" : "-"}
                          {fmt(t.amount)}
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p>No transactions.</p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}





