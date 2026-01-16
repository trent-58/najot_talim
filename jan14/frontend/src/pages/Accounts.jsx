// Accounts.jsx
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Accounts() {
  const navigate = useNavigate();

  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState("create"); // create | edit
  const [activeId, setActiveId] = useState(null);

  const [form, setForm] = useState({
    name: "",
    type: "cash",
    currency: "USD",
    balance: "0",
    status: "active",
  });

  const load = async () => {
    setError("");
    try {
      const res = await api.get("/accounts/accounts/");
      setItems(res.data);
    } catch {
      localStorage.removeItem("auth_token");
      navigate("/login");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const totalBalance = useMemo(
    () => items.reduce((s, a) => s + Number(a.balance || 0), 0),
    [items]
  );

  const openCreate = () => {
    setMode("create");
    setActiveId(null);
    setForm({ name: "", type: "cash", currency: "USD", balance: "0", status: "active" });
    setOpen(true);
  };

  const openEdit = (acc) => {
    setMode("edit");
    setActiveId(acc.id);
    setForm({
      name: acc.name || "",
      type: acc.type || "cash",
      currency: acc.currency || "USD",
      balance: String(acc.balance ?? "0"),
      status: acc.status || "active",
    });
    setOpen(true);
  };

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    const payload = {
      ...form,
      balance: Number(form.balance || 0),
    };

    try {
      if (mode === "create") {
        await api.post("/accounts/accounts/", payload);
      } else {
        await api.patch(`/accounts/accounts/${activeId}/`, payload);
      }
      setOpen(false);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Save failed");
    }
  };

  const remove = async (id) => {
    setError("");
    try {
      await api.delete(`/accounts/accounts/${id}/`);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Delete failed");
    }
  };

  return (
    <div className="simple-page">
      <div className="page-head">
        <div>
          <h1>Accounts</h1>
          <p className="muted">Total balance: <strong>{totalBalance}</strong></p>
        </div>

        <div className="toolbar">
          <button className="btn btn-primary" type="button" onClick={openCreate}>
            + Add account
          </button>
        </div>
      </div>

      {error && <p className="page-error">{error}</p>}

      <div className="card">
        {items.length === 0 ? (
          <p>No accounts yet. Add one.</p>
        ) : (
          <div className="table">
            <div className="table-head">
              <div>Name</div>
              <div>Type</div>
              <div>Currency</div>
              <div className="right">Balance</div>
              <div className="right">Actions</div>
            </div>

            {items.map((a) => (
              <div className="table-row" key={a.id}>
                <div className="strong">{a.name}</div>
                <div className="muted">{a.type}</div>
                <div className="muted">{a.currency}</div>
                <div className="right strong">{a.balance}</div>
                <div className="right actions">
                  <button className="btn btn-ghost" type="button" onClick={() => openEdit(a)}>
                    Edit
                  </button>
                  <button className="btn btn-danger" type="button" onClick={() => remove(a.id)}>
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {open && (
        <div className="modal">
          <div className="modal-box">
            <div className="modal-head">
              <h3 className="modal-title">{mode === "create" ? "Add account" : "Edit account"}</h3>
              <button className="btn btn-ghost" type="button" onClick={() => setOpen(false)}>
                ✕
              </button>
            </div>

            <form onSubmit={submit}>
              <div className="form-group">
                <label className="form-label">Account name</label>
                <input
                  className="form-input"
                  placeholder="e.g. Cash, Bank, Card"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Type</label>
                  <select
                    className="form-input"
                    value={form.type}
                    onChange={(e) => setForm({ ...form, type: e.target.value })}
                  >
                    <option value="cash">Cash</option>
                    <option value="bank">Bank</option>
                    <option value="card">Card</option>
                    <option value="wallet">Wallet</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Currency</label>
                  <select
                    className="form-input"
                    value={form.currency}
                    onChange={(e) => setForm({ ...form, currency: e.target.value })}
                  >
                    <option value="USD">USD</option>
                    <option value="UZS">UZS</option>
                    <option value="EUR">EUR</option>
                    <option value="RUB">RUB</option>
                  </select>
                </div>
              </div>

              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Balance</label>
                  <input
                    className="form-input"
                    type="number"
                    step="0.01"
                    placeholder="0"
                    value={form.balance}
                    onChange={(e) => setForm({ ...form, balance: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Status</label>
                  <select
                    className="form-input"
                    value={form.status}
                    onChange={(e) => setForm({ ...form, status: e.target.value })}
                  >
                    <option value="active">Active</option>
                    <option value="archived">Archived</option>
                  </select>
                </div>
              </div>

              <div className="modal-actions">
                <button className="btn btn-primary" type="submit">
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




