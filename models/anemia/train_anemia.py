"""
Anemia Prediction Model Training Script
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os
import pathlib

print("=" * 70)
print("ANEMIA PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "anemia.csv"

if not os.path.exists(DATA_PATH):
    print("\n⚠️  Creating sample dataset...")
    
    np.random.seed(42)
    sample_data = {
        'Gender': np.random.choice([0, 1], 1500),
        'Hemoglobin': np.random.uniform(8, 18, 1500),
        'MCH': np.random.uniform(20, 35, 1500),
        'MCHC': np.random.uniform(30, 38, 1500),
        'MCV': np.random.uniform(70, 100, 1500),
        'Result': np.random.choice([0, 1], 1500, p=[0.7, 0.3])
    }
    df = pd.DataFrame(sample_data)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Created sample dataset")
else:
    df = pd.read_csv(DATA_PATH)

print(f"Dataset Shape: {df.shape}")

X = df.drop('Result', axis=1) if 'Result' in df.columns else df.iloc[:, :-1]
y = df['Result'] if 'Result' in df.columns else df.iloc[:, -1]

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

with open(os.path.join(model_dir, 'anemia_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'anemia_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"✅ Best Model: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")
