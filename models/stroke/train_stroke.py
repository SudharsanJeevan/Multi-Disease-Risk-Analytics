"""
Stroke Risk Prediction Model Training Script
Uses Stroke Prediction Dataset from Kaggle
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import pickle
import os
import pathlib

print("=" * 70)
print("STROKE RISK PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "stroke.csv"

if not os.path.exists(DATA_PATH):
    print("\n⚠️  Creating sample dataset...")
    
    np.random.seed(42)
    sample_data = {
        'Gender': np.random.choice(['Male', 'Female'], 5000),
        'Age': np.random.randint(20, 90, 5000),
        'Hypertension': np.random.choice([0, 1], 5000, p=[0.9, 0.1]),
        'HeartDisease': np.random.choice([0, 1], 5000, p=[0.95, 0.05]),
        'EverMarried': np.random.choice(['Yes', 'No'], 5000, p=[0.7, 0.3]),
        'WorkType': np.random.choice(['Private', 'Self-employed', 'Govt_job'], 5000),
        'ResidenceType': np.random.choice(['Urban', 'Rural'], 5000),
        'AvgGlucoseLevel': np.random.uniform(50, 250, 5000),
        'BMI': np.random.uniform(15, 50, 5000),
        'SmokingStatus': np.random.choice(['never smoked', 'formerly smoked', 'smokes'], 5000),
        'stroke': np.random.choice([0, 1], 5000, p=[0.95, 0.05])
    }
    df = pd.DataFrame(sample_data)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Created sample dataset")
else:
    print(f"✅ Loading dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # Drop 'id' column if present
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    
    # Handle missing values in bmi
    if 'bmi' in df.columns:
        df['bmi'] = df['bmi'].fillna(df['bmi'].median())
    
    # Map real column names to expected names
    column_mapping = {
        'gender': 'Gender',
        'age': 'Age',
        'hypertension': 'Hypertension',
        'heart_disease': 'HeartDisease',
        'ever_married': 'EverMarried',
        'work_type': 'WorkType',
        'Residence_type': 'ResidenceType',
        'avg_glucose_level': 'AvgGlucoseLevel',
        'smoking_status': 'SmokingStatus'
    }
    df = df.rename(columns=column_mapping)

print(f"Dataset Shape: {df.shape}")

# Encode categorical variables
le = LabelEncoder()
for col in ['Gender', 'EverMarried', 'WorkType', 'ResidenceType', 'SmokingStatus']:
    if col in df.columns:
        df[col] = le.fit_transform(df[col].astype(str))
        
# Rename bmi if it exists
if 'bmi' in df.columns:
    df = df.rename(columns={'bmi': 'BMI'})

# Features and target
X = df.drop('stroke', axis=1) if 'stroke' in df.columns else df.iloc[:, :-1]
y = df['stroke'] if 'stroke' in df.columns else df.iloc[:, -1]

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
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
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

with open(os.path.join(model_dir, 'stroke_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'stroke_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"\n✅ Best Model: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")
print("✅ Models saved successfully!")
