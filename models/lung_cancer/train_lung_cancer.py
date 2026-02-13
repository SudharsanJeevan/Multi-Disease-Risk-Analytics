"""
Lung Cancer Prediction Model Training Script
Uses Lung Cancer Dataset from Kaggle
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
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

print("=" * 70)
print("LUNG CANCER PREDICTION MODEL TRAINING")
print("=" * 70)

# Dataset URL
# https://www.kaggle.com/datasets/mysarahmadbhat/lung-cancer

# Check if dataset exists
import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "lung_cancer.csv"

if not os.path.exists(DATA_PATH):
    print("\n⚠️  ERROR: Dataset not found!")
    print(f"Please download the Lung Cancer Dataset from Kaggle:")
    print("https://www.kaggle.com/datasets/mysarahmadbhat/lung-cancer")
    print(f"And save it as: {DATA_PATH}")
    print("\nFor now, creating a demo model with sample data...\n")
    
    # Create sample data
    np.random.seed(42)
    sample_data = {
        'Gender': np.random.choice(['M', 'F'], 1000),
        'Age': np.random.randint(20, 90, 1000),
        'Smoking': np.random.randint(1, 3, 1000),
        'YellowFingers': np.random.randint(1, 3, 1000),
        'Anxiety': np.random.randint(1, 3, 1000),
        'PeerPressure': np.random.randint(1, 3, 1000),
        'ChronicDisease': np.random.randint(1, 3, 1000),
        'Fatigue': np.random.randint(1, 3, 1000),
        'Allergy': np.random.randint(1, 3, 1000),
        'Wheezing': np.random.randint(1, 3, 1000),
        'Alcohol': np.random.randint(1, 3, 1000),
        'Coughing': np.random.randint(1, 3, 1000),
        'ShortnessOfBreath': np.random.randint(1, 3, 1000),
        'SwallowingDifficulty': np.random.randint(1, 3, 1000),
        'ChestPain': np.random.randint(1, 3, 1000),
        'LungCancer': np.random.choice(['YES', 'NO'], 1000, p=[0.35, 0.65])
    }
    df = pd.DataFrame(sample_data)
    
    # Save sample data
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print("✅ Created sample dataset for demonstration")
else:
    print(f"\n✅ Loading dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

print(f"\nDataset Shape: {df.shape}")
print(f"Features: {df.shape[1] - 1}")
print(f"Samples: {df.shape[0]}")

# Normalize column names (handle case differences)
df.columns = df.columns.str.strip().str.replace(' ', '_').str.upper()

# Encode categorical variables (GENDER column)
le_gender = LabelEncoder()
if 'GENDER' in df.columns:
    df['GENDER'] = le_gender.fit_transform(df['GENDER'].astype(str))

# Encode target
target_col = None
if 'LUNG_CANCER' in df.columns:
    target_col = 'LUNG_CANCER'
elif 'LUNGCANCER' in df.columns:
    target_col = 'LUNGCANCER'
else:
    # Fallback to last column
    target_col = df.columns[-1]

le_target = LabelEncoder()
df[target_col] = le_target.fit_transform(df[target_col].astype(str))

# Features and target
X = df.drop(target_col, axis=1)
y = df[target_col]

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Positive class: {sum(y == 1)} ({sum(y == 1)/len(y)*100:.1f}%)")
print(f"Negative class: {sum(y == 0)} ({sum(y == 0)/len(y)*100:.1f}%)")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("✅ Data scaled using StandardScaler")

# Train multiple models
print("\n" + "=" * 70)
print("MODEL TRAINING & COMPARISON")
print("=" * 70)

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=5),
    'Naive Bayes': GaussianNB()
}

results = {}

for name, model in models.items():
    print(f"\n🔄 Training {name}...")
    
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    
    results[name] = {
        'model': model,
        'accuracy': accuracy,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }
    
    print(f"   Accuracy: {accuracy*100:.2f}%")
    print(f"   CV Score: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")

# Find best model
print("\n" + "=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)

best_model_name = max(results, key=lambda x: results[x]['accuracy'])
best_model = results[best_model_name]['model']
best_accuracy = results[best_model_name]['accuracy']

print("\n📊 Model Performance Comparison:\n")
for name, result in sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True):
    print(f"{name:25s} - Accuracy: {result['accuracy']*100:6.2f}% | CV: {result['cv_mean']*100:6.2f}%")

print(f"\n🏆 Best Model: {best_model_name} ({best_accuracy*100:.2f}%)")

# Save best model
print("\n" + "=" * 70)
print("SAVING MODEL")
print("=" * 70)

model_dir = os.path.dirname(__file__)
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, 'lung_cancer_model.pkl')
scaler_path = os.path.join(model_dir, 'lung_cancer_scaler.pkl')

with open(model_path, 'wb') as f:
    pickle.dump(best_model, f)

with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

print(f"✅ Model saved: {model_path}")
print(f"✅ Scaler saved: {scaler_path}")

print("\n" + "=" * 70)
print("✅ TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 70)
print(f"\nModel: {best_model_name}")
print(f"Accuracy: {best_accuracy*100:.2f}%")
