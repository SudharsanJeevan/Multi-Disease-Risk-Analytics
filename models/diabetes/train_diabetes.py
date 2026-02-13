"""
Diabetes Prediction Model Training Script
Optimized with XGBoost
Uses PIMA Indian Diabetes Dataset
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import pickle
import os

print("=" * 70)
print("DIABETES PREDICTION MODEL TRAINING (OPTIMIZED)")
print("=" * 70)

import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "diabetes.csv"

if not os.path.exists(DATA_PATH):
    print("\n⚠️  Creating sample data...\n")
    
    np.random.seed(42)
    sample_data = {
        'Pregnancies': np.random.randint(0, 15, 768),
        'Glucose': np.random.randint(60, 200, 768),
        'BloodPressure': np.random.randint(50, 120, 768),
        'SkinThickness': np.random.randint(10, 60, 768),
        'Insulin': np.random.randint(0, 500, 768),
        'BMI': np.random.uniform(15, 50, 768),
        'DiabetesPedigreeFunction': np.random.uniform(0.0, 2.5, 768),
        'Age': np.random.randint(21, 81, 768),
        'Outcome': np.random.randint(0, 2, 768)
    }
    df = pd.DataFrame(sample_data)
    
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Created sample dataset")
else:
    print(f"\n✅ Loading dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

print(f"\nDataset Shape: {df.shape}")

X = df.drop('Outcome', axis=1)
y = df['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n🚀 Training OPTIMIZED models...")

# Train models with optimized parameters
models = {
    'SVM (Optimized)': SVC(kernel='rbf', C=1.5, gamma='scale', random_state=42),
    'Random Forest (Optimized)': RandomForestClassifier(
        n_estimators=300, 
        max_depth=12, 
        min_samples_split=4,
        random_state=42
    ),
    'XGBoost (Optimized)': XGBClassifier(
        n_estimators=300, 
        max_depth=6, 
        learning_rate=0.05, 
        subsample=0.9, 
        colsample_bytree=0.9,
        gamma=0.2,
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
with open(os.path.join(model_dir, 'diabetes_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'diabetes_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Training completed!")
