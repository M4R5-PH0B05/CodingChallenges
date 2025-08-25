# 💰 Personal Finance Dashboard

A local-first finance dashboard that helps you **import, analyse, and visualise your spending**.  
Start with CSV uploads, then expand to live bank sync via the **Plaid API**.  
Built with **Python, Flask, Dash, and SQLite**.

---

## ✨ Features
``
- 📂 **Transaction Import**
  - Connect bank accounts via **Plaid API** for live sync

- 📊 **Visual Dashboards**
  - Monthly income vs expenses
  - Category breakdown (donut chart)
  - Largest merchants this month
  - 6–12 month spending trends

- 📑 **Transaction Table**
  - Searchable, filterable table with category edits
  - Bulk recategorisation support

- 🏷 **Categories & Rules**
  - Auto-categorise transactions (e.g. "TESCO → Groceries")
  - Editable rules stored in DB

- 🔄 **Recurring Charge Detector** *(stretch goal)*
  - Detect subscriptions (Netflix, Spotify, etc.)

- 🔐 **Authentication**
  - Local login with password (Flask-Login + bcrypt)
  - Secrets managed with `.env` + `python-dotenv`

---

## 🏗 Tech Stack

**Backend**
- Python + Flask
- pandas (ETL for transactions)
- SQLAlchemy ORM
- Plaid API integration (optional)

**Database**
- SQLite (MVP, file-based)
- PostgreSQL (optional for cloud hosting)
- SQLCipher (optional encryption)

**Frontend**
- Dash (Plotly for charts + graphs)
- Dash DataTable for interactive tables
- Custom CSS (Bootstrap/Tailwind optional)

**Authentication**
- Flask-Login
- bcrypt for password hashing

**External Integrations**
- Plaid API (`/transactions/get`, `/accounts/get`)
- CSV upload for manual imports

---

# DATABASES

### USERS TABLE
userID primary (auto_incrementing key ), name, username, email, hashed password, plaid thing,
### BUDGET TABLE
User ID (compound key) Food, Travel, Entertainment, etc. -- all records store percentages e.g( Food:
50%, Travel:  20%, Entertainment: 15% )