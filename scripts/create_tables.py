import duckdb

# Connect to persistent DuckDB database
con = duckdb.connect("database/trekker.duckdb")

# Create 'features' table
con.execute("""
CREATE OR REPLACE TABLE features AS
SELECT * FROM 'data/features.csv';
""")

# Create 'plans' table
con.execute("""
CREATE OR REPLACE TABLE plans AS
SELECT * FROM 'data/plans.csv';
""")

# Create 'plan_features' table
con.execute("""
CREATE OR REPLACE TABLE plan_features AS
SELECT * FROM 'data/plan_features.csv';
""")

# Create 'customers' table
con.execute("""
CREATE OR REPLACE TABLE customers AS
SELECT * FROM 'data/customers.csv'
""")

# Create 'subscriptions' table
con.execute("""
CREATE OR REPLACE TABLE subscriptions AS
SELECT * FROM 'data/subscriptions.csv';
""")

# Show confirmation
print("All tables created successfully")

# See all tables in the database
print(con.execute("SHOW TABLES").fetchdf())