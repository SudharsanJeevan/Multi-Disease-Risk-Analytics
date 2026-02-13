"""
Configuration File for Multi-Disease Risk Analytics System
"""

import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).parent

# Database Configuration
DATABASE_PATH = BASE_DIR / "database.db"

# Data Paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Model Paths
MODELS_DIR = BASE_DIR / "models"

MODEL_PATHS = {
    "diabetes": {
        "model": MODELS_DIR / "diabetes" / "diabetes_model.pkl",
        "scaler": MODELS_DIR / "diabetes" / "diabetes_scaler.pkl"
    },
    "heart": {
        "model": MODELS_DIR / "heart" / "heart_model.pkl",
        "scaler": MODELS_DIR / "heart" / "heart_scaler.pkl"
    },
    "kidney": {
        "model": MODELS_DIR / "kidney" / "kidney_model.pkl",
        "scaler": MODELS_DIR / "kidney" / "kidney_scaler.pkl"
    },
    "liver": {
        "model": MODELS_DIR / "liver" / "liver_model.pkl",
        "scaler": MODELS_DIR / "liver" / "liver_scaler.pkl"
    },
    "breast_cancer": {
        "model": MODELS_DIR / "breast_cancer" / "breast_cancer_model.pkl",
        "scaler": MODELS_DIR / "breast_cancer" / "breast_cancer_scaler.pkl"
    },
    "lung_cancer": {
        "model": MODELS_DIR / "lung_cancer" / "lung_cancer_model.pkl",
        "scaler": MODELS_DIR / "lung_cancer" / "lung_cancer_scaler.pkl"
    },
    "stroke": {
        "model": MODELS_DIR / "stroke" / "stroke_model.pkl",
        "scaler": MODELS_DIR / "stroke" / "stroke_scaler.pkl"
    },
    "parkinsons": {
        "model": MODELS_DIR / "parkinsons" / "parkinsons_model.pkl",
        "scaler": MODELS_DIR / "parkinsons" / "parkinsons_scaler.pkl"
    },
    "thyroid": {
        "model": MODELS_DIR / "thyroid" / "thyroid_model.pkl",
        "scaler": MODELS_DIR / "thyroid" / "thyroid_scaler.pkl"
    },
    "anemia": {
        "model": MODELS_DIR / "anemia" / "anemia_model.pkl",
        "scaler": MODELS_DIR / "anemia" / "anemia_scaler.pkl"
    },
    "pneumonia": {
        "model": MODELS_DIR / "pneumonia" / "pneumonia_model.pkl",
        "scaler": MODELS_DIR / "pneumonia" / "pneumonia_scaler.pkl"
    },
    "tuberculosis": {
        "model": MODELS_DIR / "tuberculosis" / "tuberculosis_model.pkl",
        "scaler": MODELS_DIR / "tuberculosis" / "tuberculosis_scaler.pkl"
    },
    "alzheimers": {
        "model": MODELS_DIR / "alzheimers" / "alzheimers_model.pkl",
        "scaler": MODELS_DIR / "alzheimers" / "alzheimers_scaler.pkl"
    },
    "covid19": {
        "model": MODELS_DIR / "covid19" / "covid19_model.pkl",
        "scaler": MODELS_DIR / "covid19" / "covid19_scaler.pkl"
    },
    "melanoma": {
        "model": MODELS_DIR / "melanoma" / "melanoma_model.pkl",
        "scaler": MODELS_DIR / "melanoma" / "melanoma_scaler.pkl"
    }
}

# Dataset URLs (Kaggle datasets - for reference)
DATASET_URLS = {
    "diabetes": "https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database",
    "heart": "https://www.kaggle.com/datasets/aavigan/cleveland-clinic-heart-disease-dataset",
    "kidney": "https://www.kaggle.com/datasets/mansoordaku/ckdisease",
    "liver": "https://www.kaggle.com/datasets/uciml/indian-liver-patient-records",
    "breast_cancer": "Built-in sklearn dataset",
    "lung_cancer": "https://www.kaggle.com/datasets/mysarahmadbhat/lung-cancer",
    "stroke": "https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset",
    "parkinsons": "https://www.kaggle.com/datasets/vikasukani/parkinsons-disease-data-set",
    "thyroid": "https://www.kaggle.com/datasets/emmanuelfwerr/thyroid-disease-data",
    "anemia": "https://www.kaggle.com/datasets/biswaranjanrao/anemia-dataset",
    "pneumonia": "Synthetic - based on clinical symptoms",
    "tuberculosis": "Synthetic - based on WHO guidelines",
    "alzheimers": "https://www.kaggle.com/datasets/brsdincer/alzheimer-features",
    "covid19": "https://www.kaggle.com/datasets/meirnizri/covid19-dataset",
    "melanoma": "https://www.kaggle.com/datasets/fanconic/skin-cancer-malignant-vs-benign"
}

# Report Configuration
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Assets
ASSETS_DIR = BASE_DIR / "assets"

# Application Settings
APP_TITLE = "Multi-Disease Risk Analytics System"
APP_ICON = "🏥"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Risk Level Thresholds
RISK_THRESHOLDS = {
    "low": 0.3,      # < 30% = Low Risk
    "high": 0.7      # > 70% = High Risk
                     # 30-70% = Moderate Risk
}

# Color Schemes
COLORS = {
    "low_risk": "#28a745",      # Green
    "moderate_risk": "#ffc107",  # Yellow/Orange
    "high_risk": "#dc3545",      # Red
    "primary": "#4e73df",
    "secondary": "#858796",
    "info": "#36b9cc",
    "warning": "#f6c23e",
    "danger": "#e74a3b",
    "success": "#1cc88a"
}

# Disease Information
DISEASE_INFO = {
    "diabetes": {
        "name": "Diabetes",
        "icon": "💉",
        "description": "Diabetes is a chronic condition that affects how your body processes blood sugar (glucose).",
        "features": [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age"
        ]
    },
    "heart": {
        "name": "Heart Disease",
        "icon": "❤️",
        "description": "Heart disease refers to various conditions that affect heart function.",
        "features": [
            "Age",
            "Sex",
            "ChestPainType",
            "RestingBP",
            "Cholesterol",
            "FastingBS",
            "RestingECG",
            "MaxHR",
            "ExerciseAngina",
            "Oldpeak",
            "ST_Slope"
        ]
    },
    "kidney": {
        "name": "Kidney Disease",
        "icon": "🫘",
        "description": "Chronic kidney disease involves gradual loss of kidney function.",
        "features": [
            "Age",
            "BloodPressure",
            "SpecificGravity",
            "Albumin",
            "Sugar",
            "RedBloodCells",
            "PusCell",
            "PusCellClumps",
            "Bacteria",
            "BloodGlucoseRandom",
            "BloodUrea",
            "SerumCreatinine",
            "Sodium",
            "Potassium",
            "Hemoglobin",
            "PackedCellVolume",
            "WhiteBloodCellCount",
            "RedBloodCellCount"
        ]
    },
    "liver": {
        "name": "Liver Disease",
        "icon": "🫀",
        "description": "Liver disease encompasses any condition that impairs liver function.",
        "features": [
            "Age",
            "Gender",
            "TotalBilirubin",
            "DirectBilirubin",
            "AlkalinePhosphatase",
            "AlamineAminotransferase",
            "AspartateAminotransferase",
            "TotalProteins",
            "Albumin",
            "AlbuminGlobulinRatio"
        ]
    },
    "breast_cancer": {
        "name": "Breast Cancer",
        "icon": "🎀",
        "description": "Breast cancer is cancer that forms in the cells of the breasts.",
        "features": [
            "MeanRadius",
            "MeanTexture",
            "MeanPerimeter",
            "MeanArea",
            "MeanSmoothness",
            "MeanCompactness",
            "MeanConcavity",
            "MeanConcavePoints",
            "MeanSymmetry",
            "MeanFractalDimension"
        ]
    },
    "lung_cancer": {
        "name": "Lung Cancer",
        "icon": "🫁",
        "description": "Lung cancer is a type of cancer that begins in the lungs, most commonly caused by smoking.",
        "features": [
            "Gender",
            "Age",
            "Smoking",
            "YellowFingers",
            "Anxiety",
            "PeerPressure",
            "ChronicDisease",
            "Fatigue",
            "Allergy",
            "Wheezing",
            "Alcohol",
            "Coughing",
            "ShortnessOfBreath",
            "SwallowingDifficulty",
            "ChestPain"
        ]
    },
    "stroke": {
        "name": "Stroke Risk",
        "icon": "🧠",
        "description": "Stroke occurs when blood flow to the brain is interrupted, causing brain cells to die.",
        "features": [
            "Gender",
            "Age",
            "Hypertension",
            "HeartDisease",
            "EverMarried",
            "WorkType",
            "ResidenceType",
            "AvgGlucoseLevel",
            "BMI",
            "SmokingStatus"
        ]
    },
    "parkinsons": {
        "name": "Parkinson's Disease",
        "icon": "🤝",
        "description": "Parkinson's disease is a progressive disorder affecting movement and coordination.",
        "features": [
            "MDVPFo",
            "MDVPFhi",
            "MDVPFlo",
            "MDVPJitter",
            "MDVPJitterAbs",
            "MDVPRAP",
            "MDVPPPQ",
            "JitterDDP",
            "MDVPShimmer",
            "MDVPShimmerdB",
            "ShimmerAPQ3",
            "ShimmerAPQ5",
            "MDVPAPQ",
            "ShimmerDDA",
            "NHR",
            "HNR",
            "RPDE",
            "DFA",
            "Spread1",
            "Spread2",
            "D2",
            "PPE"
        ]
    },
    "thyroid": {
        "name": "Thyroid Disorder",
        "icon": "🦋",
        "description": "Thyroid disorder affects the thyroid gland's ability to produce hormones.",
        "features": [
            "Age",
            "Sex",
            "OnThyroxine",
            "QueryOnThyroxine",
            "ThyroidSurgery",
            "Tumor",
            "TSH",
            "T3",
            "TT4",
            "T4U",
            "FTI"
        ]
    },
    "anemia": {
        "name": "Anemia",
        "icon": "🩸",
        "description": "Anemia occurs when you don't have enough healthy red blood cells to carry oxygen.",
        "features": [
            "Gender",
            "Hemoglobin",
            "MCH",
            "MCHC",
            "MCV"
        ]
    },
    "pneumonia": {
        "name": "Pneumonia",
        "icon": "😷",
        "description": "Pneumonia is an infection that inflames air sacs in one or both lungs.",
        "features": [
            "Age",
            "Gender",
            "Fever",
            "Cough",
            "ChestPain",
            "DifficultyBreathing",
            "Fatigue",
            "SputumProduction",
            "DurationOfSymptoms",
            "SmokingHistory"
        ]
    },
    "tuberculosis": {
        "name": "Tuberculosis",
        "icon": "🦠",
        "description": "Tuberculosis is a serious infectious disease that mainly affects the lungs.",
        "features": [
            "Age",
            "Gender",
            "CoughDuration",
            "NightSweats",
            "WeightLoss",
            "Fever",
            "ChestPain",
            "BloodInSputum",
            "HIVStatus",
            "PreviousTB",
            "BCGVaccination"
        ]
    },
    "alzheimers": {
        "name": "Alzheimer's Risk",
        "icon": "🧩",
        "description": "Alzheimer's is a progressive disease that destroys memory and thinking skills.",
        "features": [
            "Age",
            "Gender",
            "EducationLevel",
            "MMSEScore",
            "FunctionalAssessment",
            "MemoryComplaints",
            "BehavioralProblems",
            "ADL",
            "IADL",
            "CDR"
        ]
    },
    "covid19": {
        "name": "COVID-19 Severity",
        "icon": "🦠",
        "description": "COVID-19 is an infectious disease caused by the SARS-CoV-2 virus.",
        "features": [
            "Age",
            "Gender",
            "COVIDContact",
            "Fever",
            "Cough",
            "SoreThroat",
            "ShortnessOfBreath",
            "HeadAche",
            "Diabetes",
            "Hypertension",
            "CardiovascularDisease",
            "Obesity",
            "ChronicPulmonary",
            "Pneumonia"
        ]
    },
    "melanoma": {
        "name": "Skin Cancer (Melanoma)",
        "icon": "🎨",
        "description": "Melanoma is the most serious type of skin cancer that develops in melanocytes.",
        "features": [
            "Age",
            "Gender",
            "FamilyHistory",
            "SunExposure",
            "MolesCount",
            "MoleChanges",
            "IrregularBorders",
            "ColorVariation",
            "Diameter",
            "Evolution"
        ]
    }
}

# Session Settings
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# ML Model Settings
TEST_SIZE = 0.2
RANDOM_STATE = 42
CV_FOLDS = 5

# Algorithms to Compare
ML_ALGORITHMS = [
    "Logistic Regression",
    "Decision Tree",
    "Random Forest",
    "Support Vector Machine",
    "K-Nearest Neighbors",
    "Naive Bayes"
]

# Create necessary directories
for path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, ASSETS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Create model subdirectories
for disease in MODEL_PATHS.keys():
    (MODELS_DIR / disease).mkdir(parents=True, exist_ok=True)
