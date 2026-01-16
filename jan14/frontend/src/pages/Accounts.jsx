import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../axios";

export default function Accounts() {
  const navigate = useNavigate();

  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [modalOpen, setModalOpen] = useState(false);
  const [mode, setMode] = useState("create");
  const [activeId, setActiveId] = useState(null);

  const [form, setForm] = useState({
    name: "",
    type: "CASH",
    currency: "USD",
    balance: "0",
    status: "ACTIVE",
  });

  const load = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await api.get("/accounts/accounts/");
      setItems(res.data || []);
    } catch {
      localStorage.removeItem("auth_token");
      navigate("/login");
    } finally {
      setLoading(false);
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
    setError("");
    setMode("create");
    setActiveId(null);
    setForm({ name: "", type: "CASH", currency: "USD", balance: "0", status: "ACTIVE" });
    setModalOpen(true);
  };

  const openEdit = (acc) => {
    setError("");
    setMode("edit");
    setActiveId(acc.id);
    setForm({
      name: acc.name || "",
      type: (acc.type || "CASH").toUpperCase(),
      currency: acc.currency || "USD",
      balance: String(acc.balance ?? "0"),
      status: (acc.status || "ACTIVE").toUpperCase(),
    });
    setModalOpen(true);
  };

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    const payload = {
      name: form.name,
      type: String(form.type || "CASH").toUpperCase(),
      currency: form.currency,
      balance: Number(form.balance || 0),
      status: String(form.status || "ACTIVE").toUpperCase(),
    };

    try {
      if (mode === "create") {
        await api.post("/accounts/accounts/", payload);
      } else {
        await api.patch(`/accounts/accounts/${activeId}/`, payload);
      }
      setModalOpen(false);
      await load();
    } catch (err) {
      const data = err.response?.data;
      const msg = data?.detail || data?.name?.[0] || "Save failed.";
      setError(msg);
    }
  };

  const remove = async (id) => {
    setError("");
    const ok = window.confirm("Delete this account?");
    if (!ok) return;

    try {
      await api.delete(`/accounts/accounts/${id}/`);
      await load();
    } catch (err) {
      const data = err.response?.data;
      const msg = data?.detail || "Delete failed.";
      setError(msg);
    }
  };

  return (
    <div className="simple-page">
      <div className="page-head">
        <div>
          <h1>Accounts</h1>
          <p className="muted">
            Total balance: <strong>{totalBalance}</strong>
          </p>
        </div>

        <div className="toolbar">
          <button type="button" className="btn btn-primary" onClick={openCreate}>
            + Add account
          </button>
        </div>
      </div>

      {error && <p className="page-error">{error}</p>}

      {loading ? (
        <div className="card">
          <p>Loading…</p>
        </div>
      ) : (
        <div className="card">
          {items.length === 0 ? (
            <p>No accounts yet.</p>
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
                    <button type="button" className="btn btn-ghost" onClick={() => openEdit(a)}>
                      Edit
                    </button>
                    <button type="button" className="btn btn-danger" onClick={() => remove(a.id)}>
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {modalOpen && (
        <div className="modal">
          <div className="modal-box">
            <div className="modal-head">
              <h3 className="modal-title">{mode === "create" ? "Add account" : "Edit account"}</h3>
              <button type="button" className="btn btn-ghost" onClick={() => setModalOpen(false)}>
                ✕
              </button>
            </div>

            <form onSubmit={submit}>
              <div className="form-group">
                <label className="form-label">Name</label>
                <input
                  className="form-input"
                  placeholder="e.g. Cash, Card"
                  value={form.name}
                  onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))}
                  required
                />
              </div>

              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Type</label>
                  <select
                    className="form-input"
                    value={form.type}
                    onChange={(e) => setForm((p) => ({ ...p, type: e.target.value }))}
                  >
                    <option value="CASH">Cash</option>
                    <option value="CARD">Card</option>
                    <option value="BANK">Bank</option>
                    <option value="WALLET">Wallet</option>
                    <option value="CURRENCY">Currency</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Currency</label>
                  <select
                    className="form-input"
                    value={form.currency}
                    onChange={(e) => setForm((p) => ({ ...p, currency: e.target.value }))}
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
                    onChange={(e) => setForm((p) => ({ ...p, balance: e.target.value }))}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Status</label>
                  <select
                    className="form-input"
                    value={form.status}
                    onChange={(e) => setForm((p) => ({ ...p, status: e.target.value }))}
                  >
                    <option value="ACTIVE">Active</option>
                    <option value="INACTIVE">Inactive</option>
                    <option value="ARCHIVED">Archived</option>
                  </select>
                </div>
              </div>

              <div className="modal-actions">
                <button type="submit" className="btn btn-primary">
                  Save
                </button>
                <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
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
