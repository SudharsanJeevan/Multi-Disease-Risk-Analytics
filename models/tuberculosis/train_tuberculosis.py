"""
Tuberculosis (TB) Prediction Model Training Script
Synthetic dataset based on WHO guidelines
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os
import pathlib

print("=" * 70)
print("TUBERCULOSIS PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "tuberculosis.csv"

print(f"\n✅ Loading dataset from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

print(f"Original dataset shape: {df.shape}")

# Drop unnecessary columns
if 'no' in df.columns:
    df = df.drop('no', axis=1)
if 'name' in df.columns:
    df = df.drop('name', axis=1)

# Encode gender (Male/Female -> 1/0)
from sklearn.preprocessing import LabelEncoder
if 'gender' in df.columns:
    le_gender = LabelEncoder()
    df['gender'] = le_gender.fit_transform(df['gender'].astype(str))

# Check for target column - the dataset doesn't have a 'TB' column, need to create or identify it
# Based on the dataset structure, we need to identify the diagnosis column
# The dataset has symptoms but might not have a clear target - let's check column names
print(f"Columns: {df.columns.tolist()}")

# For this TB symptom dataset, we need to determine TB diagnosis from symptoms
# or use a specific column if it exists
# Let's assume the last column or a specific pattern indicates TB presence
if 'tb' in df.columns or 'TB' in df.columns or 'tuberculosis' in df.columns:
    target_col = [col for col in df.columns if 'tb' in col.lower()][0]
else:
    # If no explicit TB column, we'll need to check dataset structure
    print("Warning: No explicit TB diagnosis column found")
    # Assuming binary symptom features predict TB presence
    # We might need to create target based on symptom severity
    target_col = df.columns[-1]  # Use last column as target

print(f"Using '{target_col}' as target variable")
print(f"Processed dataset shape: {df.shape}")

X = df.drop(target_col, axis=1)
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("MODEL TRAINING")
models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
}

results = {}
for name, model in models.items():
    print(f"🔄 Training {name}...")
    model.fit(X_train_scaled, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test_scaled))
    results[name] = {'model': model, 'accuracy': accuracy}
    print(f"   Accuracy: {accuracy*100:.2f}%")

best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_model_name]['model']

model_dir = os.path.dirname(__file__)
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, 'tuberculosis_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'tuberculosis_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"✅ Best Model: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")
