"""
Enhanced Lung Cancer Prediction Model Training Script
Uses Cancer Patients and Air Pollution Dataset (25 features)
Optimized with XGBoost
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import pickle
import pathlib
import os

print("=" * 70)
print("ENHANCED LUNG CANCER PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "lung_cancer.csv"

print(f"\n✅ Loading dataset from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
print(f"Dataset Shape: {df.shape}")

# Drop non-feature columns
drop_cols = ['index', 'Patient Id']
df = df.drop(columns=[c for c in drop_cols if c in df.columns])

# Encode Gender
if 'Gender' in df.columns:
    df['Gender'] = df['Gender'].map({1: 1, 2: 0}).fillna(df['Gender'])

# Encode target: Level -> 0 (Low), 1 (Medium), 2 (High)
le = LabelEncoder()
df['Level'] = le.fit_transform(df['Level'])
print(f"Target classes: {list(le.classes_)} -> {list(range(len(le.classes_)))}")
print(f"Class distribution:\n{pd.Series(df['Level']).value_counts()}")

# Save label encoder
model_dir = pathlib.Path(__file__).parent
with open(model_dir / "lung_cancer_label_encoder.pkl", 'wb') as f:
    pickle.dump(le, f)

X = df.drop('Level', axis=1)
y = df['Level']

print(f"\nFeatures ({X.shape[1]}): {list(X.columns)}")

# Save feature names for inference
with open(model_dir / "lung_cancer_features.pkl", 'wb') as f:
    pickle.dump(list(X.columns), f)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n🚀 Training OPTIMIZED models...")

models = {
    'Random Forest': RandomForestClassifier(
        n_estimators=300, max_depth=12,
        min_samples_split=3, random_state=42
    ),
    'XGBoost': XGBClassifier(
        n_estimators=300, max_depth=6,
        learning_rate=0.05, subsample=0.9,
        colsample_bytree=0.9, random_state=42,
        eval_metric='mlogloss', use_label_encoder=False
    )
}

results = {}
for name, model in models.items():
    print(f"\n🔄 Training {name}...")
    model.fit(X_train_scaled, y_train)
    acc = accuracy_score(y_test, model.predict(X_test_scaled))
    results[name] = {'model': model, 'accuracy': acc}
    print(f"   Accuracy: {acc*100:.2f}%")
    print(classification_report(y_test, model.predict(X_test_scaled),
                                 target_names=le.classes_))

best_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_name]['model']
print(f"\n🏆 Best Model: {best_name} ({results[best_name]['accuracy']*100:.2f}%)")

with open(model_dir / "lung_cancer_model.pkl", 'wb') as f:
    pickle.dump(best_model, f)
with open(model_dir / "lung_cancer_scaler.pkl", 'wb') as f:
    pickle.dump(scaler, f)

print("\n✅ Model saved successfully!")
print(f"📊 Final Accuracy: {results[best_name]['accuracy']*100:.2f}%")
