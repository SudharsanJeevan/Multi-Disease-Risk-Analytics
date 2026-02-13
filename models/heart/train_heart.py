"""
Heart Disease Prediction Model Training Script
Optimized with XGBoost
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import pickle
import os

print("=" * 70)
print("HEART DISEASE PREDICTION MODEL TRAINING (OPTIMIZED)")
print("=" * 70)

import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "heart.csv"

print(f"\n✅ Loading dataset from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

print(f"\nDataset Shape: {df.shape}")
print(f"Features: {df.shape[1] - 1}")
print(f"Samples: {df.shape[0]}")

# Features and target (target column is usually the last column)
X = df.drop(df.columns[-1], axis=1)
y = df[df.columns[-1]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n🚀 Training OPTIMIZED models...")

# Train models with optimized parameters
models = {
    'Logistic Regression (Optimized)': LogisticRegression(
        max_iter=2000, 
        C=0.1,
        random_state=42
    ),
    'Random Forest (Optimized)': RandomForestClassifier(
        n_estimators=300, 
        max_depth=15, 
        min_samples_split=3,
        random_state=42
    ),
    'XGBoost (Optimized)': XGBClassifier(
        n_estimators=300, 
        max_depth=7, 
        learning_rate=0.05, 
        subsample=0.9, 
        colsample_bytree=0.9,
        gamma=0.1,
        random_state=42, 
        eval_metric='logloss'
    ),
}

results = {}
for name, model in models.items():
    print(f"\n🔄 Training {name}...")
    model.fit(X_train_scaled, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test_scaled))
    results[name] = {'model': model, 'accuracy': accuracy}
    print(f"   Accuracy: {accuracy*100:.2f}%")

best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_model_name]['model']

print(f"\n🏆 Best: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")

model_dir = os.path.dirname(__file__)
with open(os.path.join(model_dir, 'heart_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'heart_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Training completed!")
