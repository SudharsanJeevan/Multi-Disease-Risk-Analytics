"""
Kidney Disease Prediction Model Training Script
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import pickle
import os

print("=" * 70)
print("KIDNEY DISEASE PREDICTION MODEL TRAINING")
print("=" * 70)

import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "kidney.csv"

if not os.path.exists(DATA_PATH):
    print(f"\n⚠️  Dataset not found. Creating sample data...\n")
    
    np.random.seed(42)
    n_samples = 400
    
    sample_data = {
        'Age': np.random.randint(20, 90, n_samples),
        'BloodPressure': np.random.randint(50, 180, n_samples),
        'SpecificGravity': np.random.uniform(1.005, 1.025, n_samples),
        'Albumin': np.random.randint(0, 6, n_samples),
        'Sugar': np.random.randint(0, 6, n_samples),
        'RedBloodCells': np.random.randint(0, 2, n_samples),
        'PusCell': np.random.randint(0, 2, n_samples),
        'PusCellClumps': np.random.randint(0, 2, n_samples),
        'Bacteria': np.random.randint(0, 2, n_samples),
        'BloodGlucoseRandom': np.random.randint(70, 490, n_samples),
        'BloodUrea': np.random.randint(10, 190, n_samples),
        'SerumCreatinine': np.random.uniform(0.4, 15, n_samples),
        'Sodium': np.random.randint(4, 163, n_samples),
        'Potassium': np.random.uniform(2.5, 47, n_samples),
        'Hemoglobin': np.random.uniform(3.1, 17.8, n_samples),
        'PackedCellVolume': np.random.randint(9, 54, n_samples),
        'WhiteBloodCellCount': np.random.randint(2200, 26400, n_samples),
        'RedBloodCellCount': np.random.uniform(2.1, 8.0, n_samples),
        'CKD': np.random.randint(0, 2, n_samples)
    }
    df = pd.DataFrame(sample_data)
    
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Sample dataset created")
else:
    df = pd.read_csv(DATA_PATH)

print(f"Dataset Shape: {df.shape}")

X = df.drop('CKD' if 'CKD' in df.columns else df.columns[-1], axis=1)
y = df['CKD'] if 'CKD' in df.columns else df[df.columns[-1]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nTraining models...")

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(probability=True, random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=5),
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = {'model': model, 'accuracy': accuracy}
    print(f"  {name}: {accuracy*100:.2f}%")

best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_model_name]['model']

print(f"\n🏆 Best: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")

model_dir = os.path.dirname(__file__)
with open(os.path.join(model_dir, 'kidney_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'kidney_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Training completed!")
