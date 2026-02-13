"""
View Database Contents
Shows all users and predictions in the database
"""

import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('database.db')

print("=" * 70)
print("DATABASE CONTENTS - Multi-Disease Risk Analytics System")
print("=" * 70)

# Get tables
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\n📊 Tables in database: {[t[0] for t in tables]}\n")

# Show Users
print("=" * 70)
print("👥 USERS TABLE")
print("=" * 70)
users_df = pd.read_sql_query("SELECT user_id, username, email, full_name, age, gender, created_at FROM users", conn)
print(users_df.to_string(index=False))
print(f"\nTotal Users: {len(users_df)}")

# Show Predictions
print("\n" + "=" * 70)
print("🔮 PREDICTIONS TABLE")
print("=" * 70)
predictions_df = pd.read_sql_query(
    "SELECT prediction_id, user_id, disease_type, prediction_result, risk_probability, risk_level, prediction_date FROM predictions ORDER BY prediction_date DESC LIMIT 10", 
    conn
)

if len(predictions_df) > 0:
    print(predictions_df.to_string(index=False))
    print(f"\nTotal Predictions: {len(predictions_df)}")
else:
    print("No predictions yet.")

# Statistics
print("\n" + "=" * 70)
print("📈 STATISTICS")
print("=" * 70)

cursor.execute("SELECT COUNT(*) FROM users")
print(f"Total Users: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM predictions")
print(f"Total Predictions: {cursor.fetchone()[0]}")

cursor.execute("SELECT disease_type, COUNT(*) as count FROM predictions GROUP BY disease_type")
disease_counts = cursor.fetchall()
if disease_counts:
    print("\nPredictions by Disease:")
    for disease, count in disease_counts:
        print(f"  - {disease}: {count}")

conn.close()

print("\n" + "=" * 70)
print("Database location: c:\\Users\\Ranjith\\Final project\\database.db")
print("=" * 70)
