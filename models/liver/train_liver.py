"""
Liver Disease Prediction Model Training Script
Optimized with XGBoost
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import pickle
import os

print("=" * 70)
print("LIVER DISEASE PREDICTION MODEL TRAINING (OPTIMIZED)")
print("=" * 70)

import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "liver.csv"

if not os.path.exists(DATA_PATH):
    print(f"\n⚠️  Creating sample data...\n")
    
    np.random.seed(42)
    n_samples = 583
    
    sample_data = {
        'Age': np.random.randint(4, 90, n_samples),
        'Gender': np.random.randint(0, 2, n_samples),
        'TotalBilirubin': np.random.uniform(0.4, 75, n_samples),
        'DirectBilirubin': np.random.uniform(0.1, 19.7, n_samples),
        'AlkalinePhosphatase': np.random.randint(63, 2110, n_samples),
        'AlamineAminotransferase': np.random.randint(10, 2000, n_samples),
        'AspartateAminotransferase': np.random.randint(10, 4929, n_samples),
        'TotalProteins': np.random.uniform(2.7, 9.6, n_samples),
        'Albumin': np.random.uniform(0.9, 5.5, n_samples),
        'AlbuminGlobulinRatio': np.random.uniform(0.3, 2.8, n_samples),
        'LiverDisease': np.random.randint(0, 2, n_samples)
    }
    df = pd.DataFrame(sample_data)
    
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Sample dataset created")
else:
    df = pd.read_csv(DATA_PATH)

print(f"Dataset Shape: {df.shape}")

X = df.drop('LiverDisease' if 'LiverDisease' in df.columns else df.columns[-1], axis=1)
y = df['LiverDisease' if 'LiverDisease' in df.columns else df.columns[-1]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n🚀 Training OPTIMIZED models with XGBoost...")

# Train models with optimized parameters
models = {
    'Random Forest (Optimized)': RandomForestClassifier(
        n_estimators=300, 
        max_depth=15, 
        min_samples_split=3,
        min_samples_leaf=1,
        random_state=42
    ),
    'XGBoost (Optimized)': XGBClassifier(
        n_estimators=300, 
        max_depth=8, 
        learning_rate=0.05, 
        subsample=0.8, 
        colsample_bytree=0.8,
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
with open(os.path.join(model_dir, 'liver_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'liver_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Training completed!")
