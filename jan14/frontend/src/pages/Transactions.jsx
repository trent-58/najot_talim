// Transactions.jsx
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Transactions() {
  const navigate = useNavigate();

  const [error, setError] = useState("");

  const [accounts, setAccounts] = useState([]);
  const [expenseCats, setExpenseCats] = useState([]);
  const [incomeCats, setIncomeCats] = useState([]);

  const [expenses, setExpenses] = useState([]);
  const [incomes, setIncomes] = useState([]);

  const [tab, setTab] = useState("expenses"); // expenses | incomes

  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState("create"); // create | edit
  const [kind, setKind] = useState("expense"); // expense | income
  const [activeId, setActiveId] = useState(null);

  const [form, setForm] = useState({
    account: "",
    category: "",
    amount: "",
    note: "",
  });

  const load = async () => {
    setError("");
    try {
      const [a, ec, ic, e, i] = await Promise.all([
        api.get("/accounts/accounts/"),
        api.get("/accounts/expense-categories/"),
        api.get("/accounts/income-categories/"),
        api.get("/finance/expenses/"),
        api.get("/finance/incomes/"),
      ]);

      setAccounts(a.data);
      setExpenseCats(ec.data);
      setIncomeCats(ic.data);
      setExpenses(e.data);
      setIncomes(i.data);
    } catch {
      localStorage.removeItem("auth_token");
      navigate("/login");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const accountName = useMemo(() => {
    const map = new Map(accounts.map((a) => [a.id, a.name]));
    return (id) => map.get(id) || "—";
  }, [accounts]);

  const expenseCatName = useMemo(() => {
    const map = new Map(expenseCats.map((c) => [c.id, c.name]));
    return (id) => map.get(id) || "—";
  }, [expenseCats]);

  const incomeCatName = useMemo(() => {
    const map = new Map(incomeCats.map((c) => [c.id, c.name]));
    return (id) => map.get(id) || "—";
  }, [incomeCats]);

  const openCreate = (k) => {
    setError("");
    setKind(k);
    setMode("create");
    setActiveId(null);

    const firstAccount = accounts[0]?.id || "";
    const firstCat =
      k === "expense" ? (expenseCats[0]?.id || "") : (incomeCats[0]?.id || "");

    setForm({
      account: firstAccount,
      category: firstCat,
      amount: "",
      note: "",
    });

    setOpen(true);
  };

  const openEdit = (k, item) => {
    setError("");
    setKind(k);
    setMode("edit");
    setActiveId(item.id);

    setForm({
      account: item.account || "",
      category: item.category || "",
      amount: String(item.amount ?? ""),
      note: item.note || "",
    });

    setOpen(true);
  };

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    if (!form.account) {
      setError("Select an account");
      return;
    }

    const payload = {
      account: Number(form.account),
      category: form.category ? Number(form.category) : null,
      amount: Number(form.amount),
      note: form.note,
    };

    try {
      if (kind === "expense") {
        if (mode === "create") await api.post("/finance/expenses/", payload);
        else await api.patch(`/finance/expenses/${activeId}/`, payload);
      } else {
        if (mode === "create") await api.post("/finance/incomes/", payload);
        else await api.patch(`/finance/incomes/${activeId}/`, payload);
      }

      setOpen(false);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Save failed");
    }
  };

  const remove = async (k, id) => {
    setError("");
    try {
      if (k === "expense") await api.delete(`/finance/expenses/${id}/`);
      else await api.delete(`/finance/incomes/${id}/`);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Delete failed");
    }
  };

  return (
    <div className="simple-page">
      <div className="page-head">
        <div>
          <h1>Transactions</h1>
          <p className="muted">Add, edit, and delete your incomes and expenses.</p>
        </div>

        <div className="toolbar">
          <button
            className={`btn ${tab === "expenses" ? "btn-primary" : "btn-ghost"}`}
            type="button"
            onClick={() => setTab("expenses")}
          >
            Expenses
          </button>

          <button
            className={`btn ${tab === "incomes" ? "btn-primary" : "btn-ghost"}`}
            type="button"
            onClick={() => setTab("incomes")}
          >
            Incomes
          </button>

          <button
            className={tab === "expenses" ? "btn btn-danger" : "btn btn-primary"}
            type="button"
            onClick={() => openCreate(tab === "expenses" ? "expense" : "income")}
          >
            + Add {tab === "expenses" ? "expense" : "income"}
          </button>
        </div>
      </div>

      {error && <p className="page-error">{error}</p>}

      {accounts.length === 0 ? (
        <div className="card">
          <p>You need at least one account before creating transactions.</p>
        </div>
      ) : (
        <div className="card">
          {tab === "expenses" ? (
            expenses.length === 0 ? (
              <p>No expenses yet.</p>
            ) : (
              <div className="table">
                <div className="table-head">
                  <div>Category</div>
                  <div>Account</div>
                  <div>Note</div>
                  <div className="right">Amount</div>
                  <div className="right">Actions</div>
                </div>

                {expenses.map((x) => (
                  <div className="table-row" key={`e-${x.id}`}>
                    <div className="strong">{expenseCatName(x.category)}</div>
                    <div className="muted">{accountName(x.account)}</div>
                    <div className="muted">{x.note || "—"}</div>
                    <div className="right strong negative">-{x.amount}</div>
                    <div className="right actions">
                      <button className="btn btn-ghost" type="button" onClick={() => openEdit("expense", x)}>
                        Edit
                      </button>
                      <button className="btn btn-danger" type="button" onClick={() => remove("expense", x.id)}>
                        Delete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )
          ) : incomes.length === 0 ? (
            <p>No incomes yet.</p>
          ) : (
            <div className="table">
              <div className="table-head">
                <div>Category</div>
                <div>Account</div>
                <div>Note</div>
                <div className="right">Amount</div>
                <div className="right">Actions</div>
              </div>

              {incomes.map((x) => (
                <div className="table-row" key={`i-${x.id}`}>
                  <div className="strong">{incomeCatName(x.category)}</div>
                  <div className="muted">{accountName(x.account)}</div>
                  <div className="muted">{x.note || "—"}</div>
                  <div className="right strong positive">+{x.amount}</div>
                  <div className="right actions">
                    <button className="btn btn-ghost" type="button" onClick={() => openEdit("income", x)}>
                      Edit
                    </button>
                    <button className="btn btn-danger" type="button" onClick={() => remove("income", x.id)}>
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {open && (
        <div className="modal">
          <div className="modal-box">
            <div className="modal-head">
              <h3 className="modal-title">
                {mode === "create" ? "Add" : "Edit"} {kind === "expense" ? "Expense" : "Income"}
              </h3>
              <button className="btn btn-ghost" type="button" onClick={() => setOpen(false)}>
                ✕
              </button>
            </div>

            <form onSubmit={submit}>
              <div className="form-group">
                <label className="form-label">Account</label>
                <select
                  className="form-input"
                  value={form.account}
                  onChange={(e) => setForm({ ...form, account: e.target.value })}
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
                  value={form.category}
                  onChange={(e) => setForm({ ...form, category: e.target.value })}
                >
                  {(kind === "expense" ? expenseCats : incomeCats).length === 0 ? (
                    <option value="">No categories</option>
                  ) : (
                    (kind === "expense" ? expenseCats : incomeCats).map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))
                  )}
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
                    value={form.amount}
                    onChange={(e) => setForm({ ...form, amount: e.target.value })}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Note</label>
                  <input
                    className="form-input"
                    placeholder="Optional"
                    value={form.note}
                    onChange={(e) => setForm({ ...form, note: e.target.value })}
                  />
                </div>
              </div>

              <div className="modal-actions">
                <button className={`btn ${kind === "expense" ? "btn-danger" : "btn-primary"}`} type="submit">
                  Save
                </button>
                <button className="btn btn-secondary" type="button" onClick={() => setOpen(false)}>
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




