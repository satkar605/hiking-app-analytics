import duckdb

# Connect to your database
con = duckdb.connect('database/trekker.duckdb')

# Sample query: Show first 5 rows from the features table
result = con.execute("SELECT * FROM features LIMIT 5").fetchdf()

# Print the result
print(result)
