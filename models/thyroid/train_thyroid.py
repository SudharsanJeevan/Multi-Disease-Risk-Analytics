"""
Thyroid Disorder Prediction Model Training Script
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle
import os
import pathlib

print("=" * 70)
print("THYROID DISORDER PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "thyroid.csv"

if not os.path.exists(DATA_PATH):
    print("\n⚠️  Creating sample dataset...")
    
    np.random.seed(42)
    sample_data = {
        'Age': np.random.randint(15, 85, 3000),
        'Sex': np.random.choice(['M', 'F'], 3000),
        'OnThyroxine': np.random.choice([0, 1], 3000, p=[0.9, 0.1]),
        'QueryOnThyroxine': np.random.choice([0, 1], 3000, p=[0.95, 0.05]),
        'ThyroidSurgery': np.random.choice([0, 1], 3000, p=[0.95, 0.05]),
        'Tumor': np.random.choice([0, 1], 3000, p=[0.98, 0.02]),
        'TSH': np.random.uniform(0, 15, 3000),
        'T3': np.random.uniform(0.5, 3.5, 3000),
        'TT4': np.random.uniform(50, 200, 3000),
        'T4U': np.random.uniform(0.5, 1.5, 3000),
        'FTI': np.random.uniform(50, 200, 3000),
        'ThyroidClass': np.random.choice(['negative', 'hypothyroid', 'hyperthyroid'], 3000, p=[0.92, 0.05, 0.03])
    }
    df = pd.DataFrame(sample_data)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Created sample dataset")
else:
    df = pd.read_csv(DATA_PATH)
    
    # Preprocess real dataset
    # Drop patient_id if present
    if 'patient_id' in df.columns:
        df = df.drop('patient_id', axis=1)
    
    # Convert boolean columns (f/t) to binary (0/1)
    boolean_cols = ['on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_meds', 'sick', 
                   'pregnant', 'thyroid_surgery', 'I131_treatment', 'query_hypothyroid',
                   'query_hyperthyroid', 'lithium', 'goitre', 'tumor', 'hypopituitary', 'psych',
                   'TSH_measured', 'T3_measured', 'TT4_measured', 'T4U_measured', 'FTI_measured', 'TBG_measured']
    for col in boolean_cols:
        if col in df.columns:
            df[col] = df[col].map({'f': 0, 't': 1, 'F': 0, 'T': 1}).fillna(0).astype(int)
    
    # Convert sex to binary
    if 'sex' in df.columns:
        df['sex'] = df['sex'].map({'F': 0, 'M': 1, 'f': 0, 'm': 1}).fillna(0).astype(int)
    
    # Fill numeric columns with median
    numeric_cols = ['age', 'TSH', 'T3', 'TT4', 'T4U', 'FTI', 'TBG']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].notna().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
    
    # Encode referral_source
    if 'referral_source' in df.columns:
        df['referral_source'] = pd.Categorical(df['referral_source']).codes
    
    # Convert target to binary (disorder vs no disorder)
    if 'target' in df.columns:
        # Map target: '-' means no disorder, any letter means disorder
        df['ThyroidClass'] = df['target'].apply(lambda x: 0 if str(x) == '-' else 1)
        df = df.drop('target', axis=1)

print(f"Dataset Shape: {df.shape}")

le = LabelEncoder()
if 'Sex' in df.columns:
    df['Sex'] = le.fit_transform(df[col].astype(str))

target_col = 'ThyroidClass' if 'ThyroidClass' in df.columns else df.columns[-1]
if target_col in df.columns and df[target_col].dtype == 'object':
    df[target_col] = le.fit_transform(df[target_col].astype(str))

X = df.drop(target_col, axis=1)
y = df[target_col]

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

with open(os.path.join(model_dir, 'thyroid_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'thyroid_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"✅ Best Model: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")
