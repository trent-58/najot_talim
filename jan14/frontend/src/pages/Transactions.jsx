// Transactions.jsx
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Transactions() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [accounts, setAccounts] = useState([]);
  const [expenseCats, setExpenseCats] = useState([]);
  const [incomeCats, setIncomeCats] = useState([]);

  const [expenses, setExpenses] = useState([]);
  const [incomes, setIncomes] = useState([]);

  const [viewMode, setViewMode] = useState("all");
  const [categoryFilter, setCategoryFilter] = useState("");
  const [duration, setDuration] = useState("all");

  const [txModalOpen, setTxModalOpen] = useState(false);
  const [txMode, setTxMode] = useState("create");
  const [txType, setTxType] = useState("expense");
  const [activeId, setActiveId] = useState(null);

  const [txForm, setTxForm] = useState({
    account: "",
    category: "",
    amount: "",
    note: "",
  });

  const [catModalOpen, setCatModalOpen] = useState(false);
  const [catType, setCatType] = useState("expense");
  const [catForm, setCatForm] = useState({ name: "", icon: "" });

  const loadAll = async () => {
    setError("");
    setLoading(true);
    try {
      const [a, ec, ic, e, i] = await Promise.all([
        api.get("/accounts/accounts/"),
        api.get("/accounts/expense-categories/"),
        api.get("/accounts/income-categories/"),
        api.get("/finance/expenses/"),
        api.get("/finance/incomes/"),
      ]);
      setAccounts(a.data || []);
      setExpenseCats(ec.data || []);
      setIncomeCats(ic.data || []);
      setExpenses(e.data || []);
      setIncomes(i.data || []);
    } catch {
      localStorage.removeItem("auth_token");
      navigate("/login");
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const [ec, ic] = await Promise.all([
        api.get("/accounts/expense-categories/"),
        api.get("/accounts/income-categories/"),
      ]);
      setExpenseCats(ec.data || []);
      setIncomeCats(ic.data || []);
    } catch {}
  };

  useEffect(() => {
    loadAll();
  }, []);

  const accountMap = useMemo(() => new Map(accounts.map((a) => [a.id, a])), [accounts]);
  const expenseCatMap = useMemo(() => new Map(expenseCats.map((c) => [c.id, c])), [expenseCats]);
  const incomeCatMap = useMemo(() => new Map(incomeCats.map((c) => [c.id, c])), [incomeCats]);

  const merged = useMemo(() => {
    const ex = (expenses || []).map((x) => ({ ...x, tx_type: "expense" }));
    const inc = (incomes || []).map((x) => ({ ...x, tx_type: "income" }));
    return [...ex, ...inc].sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }, [expenses, incomes]);

  const inRange = (iso) => {
    if (duration === "all") return true;

    const d = new Date(iso);
    const now = new Date();

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

    const todayStart = startOfDay(now);

    if (duration === "today") return d >= todayStart;
    if (duration === "week") return d >= startOfWeekMon(now);
    if (duration === "month") return d >= new Date(now.getFullYear(), now.getMonth(), 1);
    if (duration === "3m") return d >= addMonths(todayStart, -3);
    if (duration === "6m") return d >= addMonths(todayStart, -6);
    if (duration === "year") return d >= new Date(now.getFullYear(), 0, 1);

    return true;
  };

  const filtered = useMemo(() => {
    let list = merged;

    list = list.filter((t) => inRange(t.created_at));

    if (viewMode !== "all") {
      list = list.filter((t) => t.tx_type === viewMode);
    }

    if (!categoryFilter) return list;

    if (categoryFilter === "none") {
      return list.filter((t) => t.category == null);
    }

    const [t, idStr] = categoryFilter.split(":");
    const id = Number(idStr);
    return list.filter((x) => x.tx_type === t && Number(x.category) === id);
  }, [merged, viewMode, categoryFilter, duration]);

  const txCategoryLabel = (tx) => {
    if (tx.category == null) return "No category";
    if (tx.tx_type === "expense") return expenseCatMap.get(tx.category)?.name || "—";
    return incomeCatMap.get(tx.category)?.name || "—";
  };

  const txAccountLabel = (tx) => {
    const a = accountMap.get(tx.account);
    return a ? `${a.name} (${a.currency})` : "—";
  };

  const openCreate = () => {
    setError("");
    setTxMode("create");
    setActiveId(null);

    const firstAccount = accounts[0]?.id || "";
    const firstExpenseCat = expenseCats[0]?.id || "";
    const firstIncomeCat = incomeCats[0]?.id || "";

    setTxType("expense");
    setTxForm({
      account: firstAccount,
      category: firstExpenseCat,
      amount: "",
      note: "",
    });

    if (!firstAccount) {
      setError("Create an account first.");
      return;
    }

    setTxModalOpen(true);
  };

  const openEdit = (tx) => {
    setError("");
    setTxMode("edit");
    setTxType(tx.tx_type);
    setActiveId(tx.id);
    setTxForm({
      account: tx.account ?? "",
      category: tx.category ?? "",
      amount: String(tx.amount ?? ""),
      note: tx.note ?? "",
    });
    setTxModalOpen(true);
  };

  const onSwitchTxType = (nextType) => {
    if (txMode === "edit") return;
    setTxType(nextType);

    const firstExpenseCat = expenseCats[0]?.id || "";
    const firstIncomeCat = incomeCats[0]?.id || "";
    setTxForm((p) => ({
      ...p,
      category: nextType === "expense" ? firstExpenseCat : firstIncomeCat,
    }));
  };

  const submitTx = async (e) => {
    e.preventDefault();
    setError("");

    if (!txForm.account) {
      setError("Select an account.");
      return;
    }
    if (!txForm.amount) {
      setError("Amount is required.");
      return;
    }

    const payload = {
      account: Number(txForm.account),
      category: txForm.category ? Number(txForm.category) : null,
      amount: Number(txForm.amount),
      note: txForm.note || "",
    };

    try {
      if (txType === "expense") {
        if (txMode === "create") {
          await api.post("/finance/expenses/", payload);
        } else {
          await api.patch(`/finance/expenses/${activeId}/`, payload);
        }
      } else {
        if (txMode === "create") {
          await api.post("/finance/incomes/", payload);
        } else {
          await api.patch(`/finance/incomes/${activeId}/`, payload);
        }
      }

      setTxModalOpen(false);
      await loadAll();
    } catch (err) {
      const data = err.response?.data;
      if (typeof data === "string") setError(data);
      else if (data?.detail) setError(data.detail);
      else setError("Save failed.");
    }
  };

  const deleteTx = async (tx) => {
    setError("");
    const ok = window.confirm("Delete this transaction?");
    if (!ok) return;

    try {
      if (tx.tx_type === "expense") {
        await api.delete(`/finance/expenses/${tx.id}/`);
      } else {
        await api.delete(`/finance/incomes/${tx.id}/`);
      }
      await loadAll();
    } catch (err) {
      const data = err.response?.data;
      if (data?.detail) setError(data.detail);
      else setError("Delete failed.");
    }
  };

  const openAddCategoryExpense = () => {
    setError("");
    setCatType("expense");
    setCatForm({ name: "", icon: "" });
    setCatModalOpen(true);
  };

  const openAddCategoryIncome = () => {
    setError("");
    setCatType("income");
    setCatForm({ name: "", icon: "" });
    setCatModalOpen(true);
  };

  const submitCategory = async (e) => {
    e.preventDefault();
    setError("");

    const name = (catForm.name || "").trim();
    const icon = (catForm.icon || "").trim();
    if (!name) {
      setError("Category name is required.");
      return;
    }

    try {
      if (catType === "expense") {
        const res = await api.post("/accounts/expense-categories/", {
          name,
          ...(icon ? { icon } : {}),
        });
        await loadCategories();
        setTxType("expense");
        setTxForm((p) => ({ ...p, category: res.data?.id || "" }));
      } else {
        const res = await api.post("/accounts/income-categories/", { name });
        await loadCategories();
        setTxType("income");
        setTxForm((p) => ({ ...p, category: res.data?.id || "" }));
      }
      setCatModalOpen(false);
    } catch (err) {
      const data = err.response?.data;
      const msg = data?.name?.[0] || data?.detail || "Failed to create category.";
      setError(msg);
    }
  };

  return (
    <div className="simple-page">
      <div className="page-head">
        <div>
          <h1>Transactions</h1>
          <p className="muted">Merged list + filters + add/edit/delete + category popup.</p>
        </div>

        <div className="toolbar">
          <div className="btn-group">
            <button
              type="button"
              className={`btn ${viewMode === "all" ? "btn-primary" : "btn-ghost"}`}
              onClick={() => setViewMode("all")}
            >
              All
            </button>
            <button
              type="button"
              className={`btn ${viewMode === "expense" ? "btn-danger" : "btn-ghost"}`}
              onClick={() => setViewMode("expense")}
            >
              Expenses
            </button>
            <button
              type="button"
              className={`btn ${viewMode === "income" ? "btn-primary" : "btn-ghost"}`}
              onClick={() => setViewMode("income")}
            >
              Incomes
            </button>
          </div>

          <select
            className="form-input select-compact"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
          >
            <option value="all">All time</option>
            <option value="today">Today</option>
            <option value="week">This week</option>
            <option value="month">This month</option>
            <option value="3m">Last 3 months</option>
            <option value="6m">Last 6 months</option>
            <option value="year">This year</option>
          </select>

          <select
            className="form-input select-compact"
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
          >
            <option value="">All categories</option>
            <option value="none">No category</option>
            <optgroup label="Expense categories">
              {expenseCats.map((c) => (
                <option key={`e-${c.id}`} value={`expense:${c.id}`}>
                  {c.name}
                </option>
              ))}
            </optgroup>
            <optgroup label="Income categories">
              {incomeCats.map((c) => (
                <option key={`i-${c.id}`} value={`income:${c.id}`}>
                  {c.name}
                </option>
              ))}
            </optgroup>
          </select>

          <button type="button" className="btn btn-ghost" onClick={openAddCategoryExpense}>
            + Expense Category
          </button>
          <button type="button" className="btn btn-ghost" onClick={openAddCategoryIncome}>
            + Income Category
          </button>

          <button type="button" className="btn btn-primary" onClick={openCreate}>
            + Transaction
          </button>
        </div>
      </div>

      {error && <p className="page-error">{error}</p>}

      <div className="card">
        {loading ? (
          <p>Loading…</p>
        ) : filtered.length === 0 ? (
          <p>No transactions.</p>
        ) : (
          <div className="table">
            <div className="table-head tx-grid">
              <div>Type</div>
              <div>Category</div>
              <div>Account</div>
              <div>Note</div>
              <div>Date</div>
              <div className="right">Amount</div>
              <div className="right">Actions</div>
            </div>

            {filtered.map((tx) => (
              <div className="table-row tx-grid" key={`${tx.tx_type}-${tx.id}`}>
                <div className="strong">{tx.tx_type === "income" ? "Income" : "Expense"}</div>
                <div className="muted">{txCategoryLabel(tx)}</div>
                <div className="muted">{txAccountLabel(tx)}</div>
                <div className="muted">{tx.note || "—"}</div>
                <div className="muted">{tx.created_at ? new Date(tx.created_at).toLocaleString() : "—"}</div>
                <div className={`right strong ${tx.tx_type === "income" ? "positive" : "negative"}`}>
                  {tx.tx_type === "income" ? `+${tx.amount}` : `-${tx.amount}`}
                </div>
                <div className="right actions">
                  <button type="button" className="btn btn-sm btn-ghost" onClick={() => openEdit(tx)}>
                    Edit
                  </button>
                  <button type="button" className="btn btn-sm btn-danger" onClick={() => deleteTx(tx)}>
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {txModalOpen && (
        <div className="modal">
          <div className="modal-box">
            <div className="modal-head">
              <h3 className="modal-title">{txMode === "create" ? "Add Transaction" : "Edit Transaction"}</h3>
              <button type="button" className="btn btn-sm btn-ghost" onClick={() => setTxModalOpen(false)}>
                ✕
              </button>
            </div>

            <div className="toolbar" style={{ marginBottom: "0.75rem" }}>
              <button
                type="button"
                className={`btn ${txType === "expense" ? "btn-danger" : "btn-ghost"}`}
                disabled={txMode === "edit"}
                onClick={() => onSwitchTxType("expense")}
              >
                Expense
              </button>
              <button
                type="button"
                className={`btn ${txType === "income" ? "btn-primary" : "btn-ghost"}`}
                disabled={txMode === "edit"}
                onClick={() => onSwitchTxType("income")}
              >
                Income
              </button>

              <div style={{ flex: 1 }} />

              {txType === "expense" ? (
                <button type="button" className="btn btn-ghost" onClick={openAddCategoryExpense}>
                  + Add Expense Category
                </button>
              ) : (
                <button type="button" className="btn btn-ghost" onClick={openAddCategoryIncome}>
                  + Add Income Category
                </button>
              )}
            </div>

            <form onSubmit={submitTx}>
              <div className="form-group">
                <label className="form-label">Account</label>
                <select
                  className="form-input"
                  value={txForm.account}
                  onChange={(e) => setTxForm((p) => ({ ...p, account: e.target.value }))}
                  required
                >
                  {accounts.map((a) => (
                    <option key={a.id} value={a.id}>
                      {a.name} ({a.currency})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Category</label>
                <select
                  className="form-input"
                  value={txForm.category ?? ""}
                  onChange={(e) => setTxForm((p) => ({ ...p, category: e.target.value }))}
                >
                  <option value="">No category</option>
                  {(txType === "expense" ? expenseCats : incomeCats).map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Amount</label>
                  <input
                    className="form-input"
                    type="number"
                    step="0.01"
                    placeholder="0"
                    value={txForm.amount}
                    onChange={(e) => setTxForm((p) => ({ ...p, amount: e.target.value }))}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Note</label>
                  <input
                    className="form-input"
                    placeholder="Optional"
                    value={txForm.note}
                    onChange={(e) => setTxForm((p) => ({ ...p, note: e.target.value }))}
                  />
                </div>
              </div>

              <div className="modal-actions">
                <button type="submit" className={`btn ${txType === "expense" ? "btn-danger" : "btn-primary"}`}>
                  Save
                </button>
                <button type="button" className="btn btn-secondary" onClick={() => setTxModalOpen(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {catModalOpen && (
        <div className="modal">
          <div className="modal-box">
            <div className="modal-head">
              <h3 className="modal-title">{catType === "expense" ? "Add Expense Category" : "Add Income Category"}</h3>
              <button type="button" className="btn btn-sm btn-ghost" onClick={() => setCatModalOpen(false)}>
                ✕
              </button>
            </div>

            <form onSubmit={submitCategory}>
              <div className="form-group">
                <label className="form-label">Name</label>
                <input
                  className="form-input"
                  placeholder={catType === "expense" ? "e.g. Food, Transport" : "e.g. Salary, Bonus"}
                  value={catForm.name}
                  onChange={(e) => setCatForm((p) => ({ ...p, name: e.target.value }))}
                  required
                />
              </div>

              {catType === "expense" && (
                <div className="form-group">
                  <label className="form-label">Icon (optional)</label>
                  <input
                    className="form-input"
                    placeholder="e.g. 🍔"
                    value={catForm.icon}
                    onChange={(e) => setCatForm((p) => ({ ...p, icon: e.target.value }))}
                  />
                </div>
              )}

              <div className="modal-actions">
                <button type="submit" className="btn btn-primary">
                  Create
                </button>
                <button type="button" className="btn btn-secondary" onClick={() => setCatModalOpen(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}





