"""
Alzheimer's Risk Prediction Model Training Script
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
print("ALZHEIMER'S RISK PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "alzheimer.csv"

if not os.path.exists(DATA_PATH):
    print("\n⚠️  Creating sample dataset...")
    
    np.random.seed(42)
    sample_data = {
        'Age': np.random.randint(60, 95, 1500),
        'Gender': np.random.choice([0, 1], 1500),
        'EducationLevel': np.random.randint(0, 20, 1500),
        'MMSEScore': np.random.randint(0, 30, 1500),
        'FunctionalAssessment': np.random.randint(0, 30, 1500),
        'MemoryComplaints': np.random.choice([0, 1], 1500, p=[0.4, 0.6]),
        'BehavioralProblems': np.random.choice([0, 1], 1500, p=[0.6, 0.4]),
        'ADL': np.random.randint(0, 28, 1500),
        'IADL': np.random.randint(0, 8, 1500),
        'CDR': np.random.uniform(0, 3, 1500),
        'Diagnosis': np.random.choice([0, 1, 2], 1500, p=[0.4, 0.35, 0.25])
    }
    df = pd.DataFrame(sample_data)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Created sample dataset")
else:
    print(f"✅ Loading real dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # Preprocess real Alzheimer's dataset
    # Encode M/F to 0/1
    if 'M/F' in df.columns:
        df['M/F'] = df['M/F'].map({'M': 1, 'F': 0})
    
    # Handle missing values for numerical columns
    numeric_cols = ['Age', 'EDUC', 'SES', 'MMSE', 'eTIV', 'nWBV', 'ASF']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median())
    
    # Encode Group to numerical (0=Nondemented, 1=Demented, 2=Converted)
    if 'Group' in df.columns:
        df['Diagnosis'] = df['Group'].map({'Nondemented': 0, 'Demented': 1, 'Converted': 2})
        df = df.drop('Group', axis=1)
    
    # Drop CDR if it exists (it's a diagnosis indicator, would cause data leakage)
    if 'CDR' in df.columns:
        df = df.drop('CDR', axis=1)
    
    print(f"Preprocessed Alzheimer's dataset")

print(f"Dataset Shape: {df.shape}")

X = df.drop('Diagnosis', axis=1) if 'Diagnosis' in df.columns else df.iloc[:, :-1]
y = df['Diagnosis'] if 'Diagnosis' in df.columns else df.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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

with open(os.path.join(model_dir, 'alzheimers_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'alzheimers_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"✅ Best Model: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")
