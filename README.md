# 🥾 Trail Trekker: DuckDB Analytics Warehouse Setup

This project was developed as part of the Data Pipeline Summer Challenge hosted by Learn Analytics Engineering. The challenge focuses on building a lightweight, cost‑effective analytics warehouse using DuckDB and raw CSV files, inspired by real‑world SaaS data architecture needs.

---

## 📦 Challenge Overview

**Goal:** Build a local analytics warehouse for a fictional hiking app called Trail Trekker. The app offers subscription‑based plans and features, and we aim to enable data‑driven decisions without relying on cloud data warehouses.

---

## 🧠 Why DuckDB?

DuckDB is an in‑process SQL OLAP database engine for analytical workloads. It supports:
- Fast reads over columnar storage
- No‑cost, local development
- File‑based persistence (`.duckdb`)
- Easy SQL querying and table creation from CSV

We use DuckDB to:
- Create persistent, queryable data models
- Explore usage metrics across plans and features
- Prepare for future integration with tools like SQLMesh

---

## 📁 Project Structure

```
trail_trekker/
├── data/           # All raw CSV files
├── database/       # Local DuckDB file (trekker.duckdb)
├── scripts/        # Python scripts for loading and querying data
└── notebooks/      # (Optional) Jupyter notebooks for exploration
```

---

## 🛠 Setup

### 1) Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install duckdb pandas
```

### 2) Ingest CSVs into DuckDB
Run the loader script to create tables from CSVs in `database/trekker.duckdb`.
```bash
python scripts/create_tables.py
```
What it does:
- Creates or replaces these tables: `features`, `plans`, `plan_features`, `customers`, `subscriptions`
- Stores them in `database/trekker.duckdb`
- Prints a list of tables for confirmation

### 3) Verify with a quick query
```bash
python scripts/query_features.py
```
Or run an ad‑hoc query from a Python shell:
```python
import duckdb
con = duckdb.connect('database/trekker.duckdb')
print(con.execute('SHOW TABLES').fetchdf())
print(con.execute('SELECT COUNT(*) FROM subscriptions').fetchdf())
```

---

## 🗂️ Data Model (Raw Layer)

Tables created directly from CSVs:
- `features(feature_id, feature_name, feature_description, feature_category)`
- `plans(plan_id, plan_name, plan_level, price, max_hikes_per_month, photo_storage_gb, description, created_at)`
- `plan_features(plan_feature_id, plan_id, feature_id, included)`
- `customers(customer_id, username, email, phone, first_name, last_name, ..., favorite_trail_type)`
- `subscriptions(subscription_id, customer_id, plan_id, billing_cycle, subscription_start_date, subscription_end_date, status, next_billing_date, payment_method)`

Known raw data nuances (loaded as‑is):
- `features.csv`: one id is `FTR06` (without the 0). Some mappings expect `FTR006`.
- `plan_features.csv`: uses `plan_id` without cycle suffix (e.g., `PLN001/PLN002`), while `plans.csv` uses suffixed ids (`PLN001M`, `PLN001A`, ...).
- `subscriptions.csv`: includes history rows and some customer ids not present in `customers.csv`.
- `plans.csv`: includes a placeholder `plan_id=000000` row.

These are intentional to mimic common raw data realities. Cleaning/normalization can be handled in a staging layer in future steps.

---

## 📊 Sample Insight

Subscribers by plan name:
```sql
SELECT 
  p.plan_name,
  COUNT(s.customer_id) AS total_subscribers
FROM subscriptions s
JOIN plans p 
  ON s.plan_id = p.plan_id
GROUP BY p.plan_name
ORDER BY total_subscribers DESC;
```
Example output:
```
plan_name      total_subscribers
Explorer       15
Trail Master   13
Adventurer     13
```

---

## 🧪 Scripts

- `scripts/create_tables.py`
  - Connects to `database/trekker.duckdb`
  - Creates `features`, `plans`, `plan_features`, `customers`, `subscriptions` from `data/*.csv`
  - Prints confirmation and tables list

- `scripts/query_features.py`
  - Connects to the same database
  - Runs a sample `SELECT * FROM features LIMIT 5`

---

## 🔭 What’s Next
- Add a staging layer to normalize plan ids and feature ids
- Analyze churn, revenue, and engagement by feature
- Integrate SQLMesh for versioned SQL models
- (Optional) Build a Streamlit dashboard

---

## 📝 Notes
- Built with a clean, script‑based workflow for reproducibility
- `database/trekker.duckdb` serves as a persistent local analytics store

---

## 🤝 Optional Add‑Ons
If helpful, we can add:
- `LICENSE`
- `requirements.txt` or `environment.yaml`
- Quarto/HTML formatted documentation