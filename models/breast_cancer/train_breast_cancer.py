"""
Breast Cancer Prediction Model Training Script
Uses built-in sklearn Wisconsin Breast Cancer Dataset
"""

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os

print("=" * 70)
print("BREAST CANCER PREDICTION MODEL TRAINING")
print("=" * 70)

# Load built-in dataset
print("\n✅ Loading Wisconsin Breast Cancer dataset from sklearn...")
data = load_breast_cancer()

# Use only mean features (first 10) to match our app
X = data.data[:, :10]  
y = data.target

print(f"Dataset Shape: {X.shape}")
print(f"Features: {data.feature_names[:10]}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nTraining models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(probability=True, random_state=42),
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test_scaled))
    results[name] = {'model': model, 'accuracy': accuracy}
    print(f"  {name}: {accuracy*100:.2f}%")

best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_model_name]['model']

print(f"\n🏆 Best: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")

model_dir = os.path.dirname(__file__)
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, 'breast_cancer_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'breast_cancer_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"\n✅ Model saved: breast_cancer_model.pkl")
print("✅ Training completed!")
