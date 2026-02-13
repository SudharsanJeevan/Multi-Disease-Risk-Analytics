"""
Pneumonia Prediction Model Training Script
Synthetic dataset based on clinical symptoms
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
print("PNEUMONIA PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "pneumonia_dataset.csv"

print(f"\n✅ Loading dataset from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

print(f"Original dataset shape: {df.shape}")

# Encode categorical variables
from sklearn.preprocessing import LabelEncoder

# Drop PatientID
if 'PatientID' in df.columns:
    df = df.drop('PatientID', axis=1)

# Encode Gender (M/F -> 1/0)
le_gender = LabelEncoder()
if 'Gender' in df.columns:
    df['Gender'] = le_gender.fit_transform(df['Gender'].astype(str))

# Encode categorical symptom columns
categorical_cols = ['Cough', 'Fever', 'Shortness_of_breath', 'Chest_pain', 
                    'Fatigue', 'Confusion', 'Crackles', 'Sputum_color', 'Xray']

for col in categorical_cols:
    if col in df.columns:
        df[col] = LabelEncoder().fit_transform(df[col].fillna('None').astype(str))

# Handle numeric columns that may have '-' or missing values
numeric_cols = ['Age', 'Oxygen_saturation', 'WBC_count', 'Temperature']
for col in numeric_cols:
    if col in df.columns:
        # Replace '-' and 'NaN' string values with actual NaN
        df[col] = df[col].replace('-', np.nan)
        # Convert to numeric, coercing errors to NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Fill with median
        df[col] = df[col].fillna(df[col].median())

# Encode Diagnosis (Yes/No -> 1/0)
if 'Diagnosis' in df.columns:
    df['Diagnosis'] = LabelEncoder().fit_transform(df['Diagnosis'].astype(str))

print(f"Processed dataset shape: {df.shape}")

# Use 'Diagnosis' as target
X = df.drop('Diagnosis', axis=1)
y = df['Diagnosis']

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

with open(os.path.join(model_dir, 'pneumonia_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'pneumonia_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"✅ Best Model: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")
