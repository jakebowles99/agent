# App Development & Roll-out (SOW008) / Midwich

## Updates

### 2026-02-09
- Teams troubleshooting indicates app may be pointing to **UAT** and using an **old DB**.
- Question raised whether **db-orders-1** is still the active database.
- **Confirmed:** `db-orders-1` is the UAT database (per Nandan Hegde).
- Yaz suggested waiting for **Hemanth/Vaishnavi** to confirm tomorrow; asked if issue is sorted.
- Timon investigating - found app pointing to UAT with old DB when opened.
- Timon working directly with Umar on the error.
- **Action for Vaishnavi:** Rename env var display name `synapx_ev_OrderManagementPOsqlDatabase` → `ev_OrderManagementPOsqlDatabase`.

## Open questions / actions
- Confirm correct environment (UAT vs Prod) and current active DB (db-orders-1 or otherwise).
- Check app configuration/connection references and correct if mispointed.
- Follow up with Hemanth and Vaishnavi for confirmation.
