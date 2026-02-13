"""
Parkinson's Disease Prediction Model Training Script
Uses Parkinson's Dataset from Kaggle (voice measurements)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os
import pathlib

print("=" * 70)
print("PARKINSON'S DISEASE PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "parkinsons.csv"

if not os.path.exists(DATA_PATH):
    print("\n⚠️  Creating sample dataset...")
    
    np.random.seed(42)
    # Parkinson's uses voice measurements
    sample_data = {
        'MDVPFo': np.random.uniform(80, 260, 200),
        'MDVPFhi': np.random.uniform(100, 600, 200),
        'MDVPFlo': np.random.uniform(60, 240, 200),
        'MDVPJitter': np.random.uniform(0, 0.03, 200),
        'MDVPJitterAbs': np.random.uniform(0, 0.0003, 200),
        'MDVPRAP': np.random.uniform(0, 0.02, 200),
        'MDVPPPQ': np.random.uniform(0, 0.02, 200),
        'JitterDDP': np.random.uniform(0, 0.05, 200),
        'MDVPShimmer': np.random.uniform(0, 0.12, 200),
        'MDVPShimmerdB': np.random.uniform(0, 1.5, 200),
        'ShimmerAPQ3': np.random.uniform(0, 0.06, 200),
        'ShimmerAPQ5': np.random.uniform(0, 0.08, 200),
        'MDVPAPQ': np.random.uniform(0, 0.14, 200),
        'ShimmerDDA': np.random.uniform(0, 0.17, 200),
        'NHR': np.random.uniform(0, 0.3, 200),
        'HNR': np.random.uniform(5, 35, 200),
        'RPDE': np.random.uniform(0.2, 0.7, 200),
        'DFA': np.random.uniform(0.5, 0.8, 200),
        'Spread1': np.random.uniform(-8, -2, 200),
        'Spread2': np.random.uniform(0, 0.5, 200),
        'D2': np.random.uniform(1, 4, 200),
        'PPE': np.random.uniform(0, 0.6, 200),
        'status': np.random.choice([0, 1], 200, p=[0.25, 0.75])
    }
    df = pd.DataFrame(sample_data)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Created sample dataset")
else:
    print(f"✅ Loading dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # Drop 'name' column if present (patient identifier)
    if 'name' in df.columns:
        df = df.drop('name', axis=1)
        print("Dropped 'name' column from dataset")

print(f"Dataset Shape: {df.shape}")

# Features and target
X = df.drop('status', axis=1) if 'status' in df.columns else df.iloc[:, :-1]
y = df['status'] if 'status' in df.columns else df.iloc[:, -1]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n" + "=" * 70)
print("MODEL TRAINING")
print("=" * 70)

models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
}

results = {}
for name, model in models.items():
    print(f"\n🔄 Training {name}...")
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = {'model': model, 'accuracy': accuracy}
    print(f"   Accuracy: {accuracy*100:.2f}%")

best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_model_name]['model']

# Save model
model_dir = os.path.dirname(__file__)
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, 'parkinsons_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'parkinsons_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"\n✅ Best Model: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")
print("✅ Models saved successfully!")
