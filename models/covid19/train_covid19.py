"""
COVID-19 Severity Prediction Model Training Script
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import os
import pathlib

print("=" * 70)
print("COVID-19 SEVERITY PREDICTION MODEL TRAINING")
print("=" * 70)

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "covid19.csv"

if not os.path.exists(DATA_PATH):
    print("\n⚠️  Creating sample dataset...")
    
    np.random.seed(42)
    sample_data = {
        'Age': np.random.randint(1, 100, 3000),
        'Gender': np.random.choice([0, 1], 3000),
        'COVIDContact': np.random.choice([0, 1], 3000, p=[0.7, 0.3]),
        'Fever': np.random.choice([0, 1], 3000, p=[0.4, 0.6]),
        'Cough': np.random.choice([0, 1], 3000, p=[0.3, 0.7]),
        'SoreThroat': np.random.choice([0, 1], 3000, p=[0.6, 0.4]),
        'ShortnessOfBreath': np.random.choice([0, 1], 3000, p=[0.7, 0.3]),
        'HeadAche': np.random.choice([0, 1], 3000, p=[0.5, 0.5]),
        'Diabetes': np.random.choice([0, 1], 3000, p=[0.85, 0.15]),
        'Hypertension': np.random.choice([0, 1], 3000, p=[0.8, 0.2]),
        'CardiovascularDisease': np.random.choice([0, 1], 3000, p=[0.9, 0.1]),
        'Obesity': np.random.choice([0, 1], 3000, p=[0.7, 0.3]),
        'ChronicPulmonary': np.random.choice([0, 1], 3000, p=[0.95, 0.05]),
        'Pneumonia': np.random.choice([0, 1], 3000, p=[0.8, 0.2]),
        'COVIDResult': np.random.choice([0, 1, 2], 3000, p=[0.6, 0.3, 0.1])  # 0=negative, 1=positive, 2=severe
    }
    df = pd.DataFrame(sample_data)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Created sample dataset")
else:
    print(f"✅ Loading dataset from: {DATA_PATH}")
    # Sample the dataset as it's very large (1M+ rows)
    df = pd.read_csv(DATA_PATH, nrows=50000)
    
    # Convert DATE_DIED to binary severity indicator
    # 9999-99-99 means patient didn't die (less severe), actual date means died (severe)
    if 'DATE_DIED' in df.columns:
        df['COVIDResult'] = df['DATE_DIED'].apply(lambda x: 0 if str(x) == '9999-99-99' else 1)
        df = df.drop('DATE_DIED', axis=1)
    
    # Select relevant feature columns
    feature_cols = ['SEX', 'PATIENT_TYPE', 'INTUBED', 'PNEUMONIA', 'AGE', 'PREGNANT',
                   'DIABETES', 'COPD', 'ASTHMA', 'INMSUPR', 'HIPERTENSION', 
                   'OTHER_DISEASE', 'CARDIOVASCULAR', 'OBESITY', 'RENAL_CHRONIC', 
                   'TOBACCO', 'ICU']
    
    # Keep only existing feature columns
    available_features = [col for col in feature_cols if col in df.columns]
    df = df[available_features + ['COVIDResult']]
    
    # Replace special codes with appropriate values
    # 97 = not specified/no data, 98 = not applicable, 99 = unspecified
    for col in available_features:
        if col in df.columns:
            # Replace 97, 98, 99 with mode or 0
            df[col] = df[col].replace([97, 98, 99], 0)
            # Convert to binary (1=yes becomes 1, 2=no becomes 0)
            if col not in ['AGE', 'PATIENT_TYPE']:
                df[col] = df[col].apply(lambda x: 1 if x == 1 else 0)
    
    print(f"Preprocessed dataset with {len(available_features)} features")

print(f"Dataset Shape: {df.shape}")

X = df.drop('COVIDResult', axis=1) if 'COVIDResult' in df.columns else df.iloc[:, :-1]
y = df['COVIDResult'] if 'COVIDResult' in df.columns else df.iloc[:, -1]

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

with open(os.path.join(model_dir, 'covid19_model.pkl'), 'wb') as f:
    pickle.dump(best_model, f)
with open(os.path.join(model_dir, 'covid19_scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print(f"✅ Best Model: {best_model_name} ({results[best_model_name]['accuracy']*100:.2f}%)")
